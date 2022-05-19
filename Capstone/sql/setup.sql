--- TABLES
CREATE TABLE t_table (
    "t975" double precision
);

CREATE TABLE submissions (
    "submission_id" VARCHAR(6),
    "title" TEXT,
    "url" TEXT,
    "date" DATE,
    "upvotes" BIGINT
);

CREATE TABLE submissions_champions_arrays (
    "submission_id" VARCHAR(6),
    "comment_text" TEXT,
    "topic_champion" TEXT
);

CREATE TABLE submissions_champions (
    "submission_id" VARCHAR(6),
    "topic_champion" TEXT
);

CREATE TABLE submission_vectors (
    "submission_id" VARCHAR(6),
    "0" double precision, "1" double precision, "2" double precision, "3" double precision, "4" double precision, "5" double precision, "6" double precision, "7" double precision, "8" double precision, "9" double precision, "10" double precision,  "11" double precision, "12" double precision, "13" double precision, "14" double precision, "15" double precision, "16" double precision, "17" double precision, "18" double precision, "19" double precision, "20" double precision, "21" double precision, "22" double precision, "23" double precision, "24" double precision, "25" double precision, "26" double precision, "27" double precision, "28" double precision, "29" double precision, "30" double precision, "31" double precision, "32" double precision, "33" double precision, "34" double precision, "35" double precision, "36" double precision, "37" double precision, "38" double precision, "39" double precision, "40" double precision, "41" double precision, "42" double precision, "43" double precision, "44" double precision, "45" double precision, "46" double precision, "47" double precision, "48" double precision, "49" double precision, "50" double precision, "51" double precision, "52" double precision, "53" double precision, "54" double precision, "55" double precision, "56" double precision, "57" double precision, "58" double precision, "59" double precision, "60" double precision, "61" double precision, "62" double precision, "63" double precision, "64" double precision, "65" double precision, "66" double precision, "67" double precision, "68" double precision, "69" double precision, "70" double precision, "71" double precision, "72" double precision, "73" double precision, "74" double precision, "75" double precision, "76" double precision, "77" double precision, "78" double precision, "79" double precision, "80" double precision, "81" double precision, "82" double precision, "83" double precision, "84" double precision, "85" double precision, "86" double precision, "87" double precision, "88" double precision, "89" double precision, "90" double precision, "91" double precision, "92" double precision, "93" double precision, "94" double precision, "95" double precision, "96" double precision, "97" double precision, "98" double precision, "99" double precision
);

CREATE TABLE playrates (
    "date" DATE,
    "champion" TEXT,
    "playrate" DOUBLE PRECISION
);


--- CONSTRAINTS
ALTER TABLE submissions_champions_arrays
    ADD CONSTRAINT submission_champions_arrays_pk
    PRIMARY KEY ("submission_id");

ALTER TABLE submission_vectors
    ADD CONSTRAINT submissions_pk
    PRIMARY KEY ("submission_id");

ALTER TABLE submission_vectors
    ADD CONSTRAINT submissions_fk
    FOREIGN KEY ("submission_id")
        REFERENCES submissions("submission_id");

ALTER TABLE submissions_champions
    ADD CONSTRAINT submissions_champions_pk
    PRIMARY KEY ("submission_id");

ALTER TABLE submissions_champions
    ADD CONSTRAINT submission_fk
    FOREIGN KEY ("submission_id")
        REFERENCES submissions("submission_id");

ALTER TABLE submissions
    ADD PRIMARY KEY ("submission_id");

ALTER TABLE playrates
    ADD CONSTRAINT playrates_pk
    PRIMARY KEY ("date", "champion");


--- INDEXING
--- submission_champions_arrays
CREATE INDEX submission_champ_arrays_id_idx
    ON submissions_champions_arrays("submission_id");

--- submission_champions
CREATE INDEX submission_champion_idx
    ON submissions_champions("topic_champion");

CREATE INDEX submission_id_champion_idx
    ON submissions_champions("submission_id", "topic_champion");

CREATE INDEX submissions_id_idx
    ON submissions_champions("submission_id");

--- submissions
CREATE INDEX submissions_id_idx
    ON submissions("submission_id");

CREATE INDEX submissions_date_idx
    ON submissions("date");

--- submission_vectors
CREATE INDEX ix_submission_vectors_submission_id
    ON submission_vectors("submission_id");

--- playrates
CREATE INDEX date_idx
    ON playrates ("Date");







