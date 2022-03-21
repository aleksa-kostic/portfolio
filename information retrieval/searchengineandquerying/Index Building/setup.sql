SET CLIENT_ENCODING = "utf8";

DROP TABLE IF EXISTS Tokens;
CREATE TABLE IF NOT EXISTS Tokens
(
    token         TEXT,
    isKeyword    BOOLEAN,
    fullPath    TEXT,
    dir            VARCHAR(5),
    file        VARCHAR(5),
    frequency    INTEGER,
    PRIMARY KEY (Token, fullPath)
);

CREATE EXTENSION IF NOT EXISTS pg_trgm ;
CREATE INDEX IF NOT EXISTS tkn_trgm_idx ON Tokens USING gin(token gin_trgm_ops);
