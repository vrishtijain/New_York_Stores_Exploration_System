-- CREATE DATABASE dbms_final_project;
-- CREATE USER dbms_project_user WITH PASSWORD 'dbms_password';
-- GRANT ALL PRIVILEGES ON DATABASE dbms_final_project TO dbms_project_user;

DROP DATABASE IF EXISTS project;
CREATE DATABASE project;

DROP USER IF EXISTS project;
CREATE USER project WITH PASSWORD 'project';

GRANT ALL PRIVILEGES ON DATABASE project TO project;
