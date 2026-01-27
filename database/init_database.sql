-- Crée un utilisateur pour l'application
CREATE USER root_admin WITH PASSWORD 'root_admin';

-- Crée la base pour l'application
CREATE DATABASE goodcollect_ocr
WITH OWNER = root_admin
ENCODING 'UTF8'
LC_COLLATE = 'fr_FR.UTF-8'
LC_CTYPE = 'fr_FR.UTF-8'
TEMPLATE template0;

-- Donne tous les privilèges sur la base
GRANT ALL PRIVILEGES ON DATABASE goodcollect_ocr TO root_admin;

-- Se connecter à la base
\c goodcollect_ocr

-- Activer l'extension trigram pour fuzzy search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- PROIVDER TABLE
CREATE TABLE IF NOT EXISTS providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
    email VARCHAR(255) NOT NULL
    phone VARCHAR(255) NOT NULL
    address VARCHAR(255) NOT NULL
    city VARCHAR(255) NOT NULL
    state VARCHAR(255) NOT NULL
    zip VARCHAR(255) NOT NULL
    country VARCHAR(255) NOT NULL
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-
CREATE