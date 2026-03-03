-- ========================================
-- KNOWLEDGE ASSISTANT DATABASE SCHEMA
-- ========================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ========================================
-- ENUM TYPES
-- ========================================

CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
CREATE TYPE document_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE action_type AS ENUM ('login', 'logout', 'upload_document', 'delete_document', 'search', 'export');

-- ========================================
-- USERS TABLE
-- ========================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    keycloak_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    role user_role NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_keycloak_id ON users(keycloak_id);
CREATE INDEX idx_users_role ON users(role);

-- ========================================
-- DOCUMENTS TABLE
-- ========================================

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(512) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- 'pdf', 'txt', 'docx', etc.
    status document_status DEFAULT 'pending',
    content_hash VARCHAR(255), -- SHA256 hash for deduplication
    metadata JSONB, -- Additional metadata like page count, etc.
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_documents_owner_id ON documents(owner_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);
CREATE INDEX idx_documents_content_hash ON documents(content_hash);

-- ========================================
-- DOCUMENT CHUNKS TABLE
-- Stores parsed document sections for better search
-- ========================================

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_length INTEGER,
    embedding vector(1536), -- Vector embeddings (1536 dimensions for typical embedding models)
    metadata JSONB, -- page number, section, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_document_chunks_document_id ON document_chunks(document_id);
CREATE INDEX idx_document_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- ========================================
-- SEARCH QUERIES TABLE
-- Audit trail and analytics
-- ========================================

CREATE TABLE search_queries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    results_count INTEGER DEFAULT 0,
    response_time_ms INTEGER,
    is_satisfied BOOLEAN, -- Thumbs up/down feedback
    feedback_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_search_queries_user_id ON search_queries(user_id);
CREATE INDEX idx_search_queries_created_at ON search_queries(created_at DESC);

-- ========================================
-- AUDIT LOG TABLE
-- Track all important actions
-- ========================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action action_type NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    details JSONB,
    ip_address VARCHAR(45),
    user_agent VARCHAR(512),
    status_code INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- ========================================
-- CONVERSATION SESSIONS TABLE
-- Store multi-turn Q&A conversations
-- ========================================

CREATE TABLE conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    is_archived BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversation_sessions_user_id ON conversation_sessions(user_id);
CREATE INDEX idx_conversation_sessions_created_at ON conversation_sessions(created_at DESC);

-- ========================================
-- CONVERSATION MESSAGES TABLE
-- Individual messages in a conversation
-- ========================================

CREATE TABLE conversation_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tokens_used INTEGER,
    referenced_documents JSONB, -- List of document IDs used for this response
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversation_messages_session_id ON conversation_messages(session_id);
CREATE INDEX idx_conversation_messages_created_at ON conversation_messages(created_at DESC);

-- ========================================
-- PERMISSIONS TABLE
-- Fine-grained access control
-- ========================================

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    permission_type VARCHAR(50) NOT NULL, -- 'view', 'edit', 'delete', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, document_id, permission_type)
);

CREATE INDEX idx_permissions_user_id ON permissions(user_id);
CREATE INDEX idx_permissions_document_id ON permissions(document_id);

-- ========================================
-- CREATE MATERIALIZED VIEWS FOR ANALYTICS
-- ========================================

CREATE MATERIALIZED VIEW user_statistics AS
SELECT
    u.id,
    u.email,
    u.role,
    COUNT(DISTINCT d.id) as total_documents,
    COUNT(DISTINCT sq.id) as total_queries,
    MAX(sq.created_at) as last_query_date,
    COUNT(DISTINCT cs.id) as total_conversations
FROM users u
LEFT JOIN documents d ON u.id = d.owner_id
LEFT JOIN search_queries sq ON u.id = sq.user_id
LEFT JOIN conversation_sessions cs ON u.id = cs.user_id
GROUP BY u.id, u.email, u.role;

CREATE INDEX idx_user_statistics_id ON user_statistics(id);

-- ========================================
-- FUNCTIONS
-- ========================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE
ON users FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for documents table
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE
ON documents FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for conversation_sessions table
CREATE TRIGGER update_conversation_sessions_updated_at BEFORE UPDATE
ON conversation_sessions FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- INITIAL DATA
-- ========================================

-- Insert admin user (you'll link this to Keycloak)
INSERT INTO users (keycloak_id, email, full_name, role, is_active)
VALUES ('admin-keycloak-id', 'admin@knowledge-assistant.local', 'Administrator', 'admin', true)
ON CONFLICT (keycloak_id) DO NOTHING;
