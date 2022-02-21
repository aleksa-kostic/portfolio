/*

	Queries : Project 3 M1

*/

-- NUMBER OF DOCUMENTS
SELECT COUNT(DISTINCT t.fullPath)
FROM Tokens t;

-- NUMBER OF UNIQUE WORDS

SELECT COUNT(DISTINCT t.token)
FROM Tokens t;

--- INDEX SIZE ---
select pg_indexes_size('Tokens');

-- QUERIES --

-- "Informatics" query

SELECT *
FROM Tokens t
WHERE t.token = 'informatics'
ORDER BY t.Frequency DESC
LIMIT 20;

	-- COUNT
SELECT COUNT(t.token)
FROM Tokens t
WHERE t.token = 'informatics'
GROUP BY t.token;


-- "Mondego" query

SELECT *
FROM Tokens t
WHERE t.token = 'mondego'
ORDER BY t.Frequency DESC
LIMIT 20;


	-- COUNT
SELECT COUNT(t.token)
FROM Tokens t
WHERE t.token = 'mondego'
GROUP BY t.token;


-- "Irvine" query

SELECT *
FROM Tokens t
WHERE t.token = 'irvine'
ORDER BY t.Frequency DESC
LIMIT 20;

	-- COUNT
SELECT COUNT(t.token)
FROM Tokens t
WHERE t.token = 'irvine'
GROUP BY t.token;


-- "artificial intelligence" query

SELECT *
FROM Tokens t
WHERE t.token = 'artificial' OR t.token = 'intelligence'
ORDER BY t.frequency DESC
LIMIT 20;


-- COUNT
SELECT COUNT(t.token)
FROM Tokens t
WHERE t.token = 'artificial' OR t.token = 'intelligence'
GROUP BY t.token;


-- "computer science" query

SELECT *
FROM Tokens t
WHERE t.token = 'computer' OR t.token = 'science'
ORDER BY t.frequency DESC
LIMIT 20;


-- COUNT
SELECT COUNT(t.token)
FROM Tokens t
WHERE t.token = 'computer' OR t.token = 'science'
GROUP BY t.token;


