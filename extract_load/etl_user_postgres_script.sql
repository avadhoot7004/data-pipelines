-- Database: AdventureWorks

CREATE DATABASE "AdventureWorks"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

--create etl user
CREATE USER etl WITH PASSWORD 'demopass';
--grant connect
GRANT CONNECT ON DATABASE "AdventureWorks" TO etl;
--grant table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO etl;

SELECT datname
FROM pg_database;

SELECT datname, pg_catalog.pg_get_userbyid(datdba)
FROM pg_database
WHERE datname = 'AdventureWorks';

SELECT current_user;

SELECT usename FROM pg_catalog.pg_user;

ALTER DATABASE "AdventureWorks" OWNER TO etl;
GRANT ALL PRIVILEGES ON DATABASE "AdventureWorks" TO etl;