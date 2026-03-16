-- allow roles to use the public schema
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;

-- allow access to existing tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role;

-- allow access to sequences (for SERIAL / IDs)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated, service_role;

-- ensure future tables automatically inherit permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO anon, authenticated, service_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO anon, authenticated, service_role;