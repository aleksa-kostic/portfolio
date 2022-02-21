/*
SET CLIENT_ENCODING TO 'utf8';

--- TEMPLATE FOR THE ORDER OF THINGS

--- START DATA LOADING ITERATION
CREATE TABLE <table_name> (
    --- Populate table attributes with constraints and data types
);
--- DO THIS IF NECESSARY
CREATE INDEX <index_name> ON <table_name>(<primary_key>);

--- Read data from the data files

COPY <table_name> --- <table_name> is the same as above
    FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/<FILENAME>.tsv' --- REPLACE <FILENAME>
        DELIMITER E'\t' --- These tsv files and delimited with '\t'
        QUOTE E'\b'
        NULL AS '\N' --- Null spaces typically filled with '\N'
        CSV HEADER; --- Indicate that there is, in fact, a header in the files
*/
--- END DATA LOADING ITERATION

SET CLIENT_ENCODING TO 'utf8';

--- TITLEBASICS
CREATE TABLE titleBasics (
    tconst VARCHAR (20) PRIMARY KEY NOT NULL,
    titleType VARCHAR (20),
    primaryTitle VARCHAR (500) NOT NULL,
    originalTitle VARCHAR (500),
    isAdult SMALLINT,
    startYear SMALLINT,
    endYear SMALLINT,
    runtimeMinutes VARCHAR(100),
    genres VARCHAR (100)
);

COPY titleBasics
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/title.basics.tsv'
DELIMITER E'\t'
QUOTE AS E'\b'
NULL AS '\N'
CSV HEADER;

--- TITLERATINGS
CREATE TABLE titleRatings(
    tconst VARCHAR(20) REFERENCES titleBasics(tconst) PRIMARY KEY NOT NULL,
    averageRating REAL,
    numVotes INTEGER
);

COPY titleRatings
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/title.ratings.tsv'
DELIMITER E'\t'
QUOTE AS E'\b'
NULL AS '\N'
CSV HEADER;

--- TITLECREW
CREATE TABLE titleCrew(
    tconst VARCHAR(20) REFERENCES titleBasics(tconst) PRIMARY KEY NOT NULL,
    directors TEXT,
    writers TEXT
);

COPY titleCrew
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/title.crew.tsv'
DELIMITER E'\t'
QUOTE AS E'\b'
NULL AS '\N'
CSV HEADER;



--- TITLEEPISODE
CREATE TABLE titleEpisode(
    tconst VARCHAR(20) REFERENCES titleBasics(tconst) PRIMARY KEY NOT NULL,
    parentTconst VARCHAR(20),
    seasonNumber SMALLINT,
    episodeNumber INTEGER
);

COPY titleEpisode
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/title.episode.tsv'
DELIMITER E'\t'
QUOTE AS E'\b'
NULL AS '\N'
CSV HEADER;

--- TITLEPRINCIPALS
CREATE TABLE titlePrincipals (
    tconst VARCHAR(20) NOT NULL,
    ordering SMALLINT,
    principalCast TEXT,
    category VARCHAR(50),
    job TEXT,
    characters TEXT,
    PRIMARY KEY (tconst, ordering)
);
CREATE INDEX tprn_idx ON titlePrincipals(tconst, ordering);

COPY titlePrincipals
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/title.principals.tsv'
DELIMITER E'\t'
QUOTE E'\b'
NULL AS '\N'
CSV HEADER;



--- TITLEAKAS
CREATE TABLE titleAkas (
    titleId VARCHAR(20) NOT NULL,
    ordering SMALLINT,
    title TEXT,
    region VARCHAR(20),
    language VARCHAR(20),
    types TEXT,
    attributes TEXT,
    isOriginalTitle SMALLINT,
    PRIMARY KEY (titleId, ordering)
);
CREATE INDEX taks_idx ON titleAkas(titleId, ordering);

COPY titleAkas
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/title.akas.tsv'
DELIMITER E'\t'
QUOTE E'\b'
NULL AS '\N'
CSV HEADER;

--- NAMEBASICS
CREATE TABLE nameBasics (
    nconst VARCHAR(20) PRIMARY KEY NOT NULL,
    primaryName VARCHAR(200),
    birthYear SMALLINT,
    deathYear SMALLINT,
    primaryProfession VARCHAR(100),
    knownForTitles TEXT
);

COPY nameBasics
FROM 'D:/2021-2022/WINTER 2022/capstone170a/HW1/data/name.basics.tsv'
DELIMITER E'\t'
QUOTE E'\b'
NULL AS '\N'
CSV HEADER;
