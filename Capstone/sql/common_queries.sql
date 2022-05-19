--- Get size of DB and tables
SELECT pg_size_pretty( pg_database_size('postgres') ) as "DB size",
pg_size_pretty( pg_total_relation_size('playrates') ) as "playrates size",
pg_size_pretty( pg_total_relation_size('submission_vectors') ) as "submission_vectors size",
pg_size_pretty( pg_total_relation_size('submissions') ) as "submissions size",
pg_size_pretty( pg_total_relation_size('submissions_champions') ) as "submissions_champions size",
pg_size_pretty( pg_total_relation_size('submissions_champions_arrays') ) as "submissions_champions_arrays size",
pg_size_pretty( pg_total_relation_size('t_table') ) as "t_table size";

--- Get whether there was a significant change in
--- playrate after this date using a two-sample
--- t-test. Example arguments given.
SELECT t_sample_t_test("ahri", "2022-02-01");

--- Get a table of submission_id, upvotes, date, and the
--- 100-value vector (100 columns) of the average word2vec
--- vector of the submission. This table to be used in
--- model building in Python using PyTorch.
SELECT model_parameters();