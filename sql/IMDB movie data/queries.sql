
SET check_function_bodies = off;

CREATE FUNCTION question3a()
RETURNS BIGINT
LANGUAGE SQL
AS $$

	SELECT COUNT(tconst)
	FROM titleBasics;
$$;

CREATE FUNCTION question3b()
RETURNS TABLE(
	startYear 		titleBasics.startYear%TYPE,
	count 			BIGINT
)
LANGUAGE SQL
AS $$
	SELECT startYear, COUNT(tconst)
    FROM titlebasics
    GROUP BY startYear;
$$;

CREATE FUNCTION question3c()
RETURNS TABLE(
	startYear 		titleBasics.startYear%TYPE,
	count 			BIGINT,
	min 			DOUBLE PRECISION,
	max				DOUBLE PRECISION,
	avg 			DOUBLE PRECISION
)
LANGUAGE SQL
AS $$
	SELECT startYear,
       COUNT(tconst),
       MIN(CAST(runtimeminutes AS DOUBLE PRECISION)),
       MAX(CAST(runtimeminutes AS DOUBLE PRECISION)),
       AVG(CAST(runtimeminutes AS DOUBLE PRECISION))
    FROM titlebasics
    WHERE startYear >= 2016
    GROUP BY startYear;
$$;

CREATE FUNCTION question3d()
RETURNS TABLE(
	primaryTitle 	titleBasics.primaryTitle%TYPE,
	startYear 		titleBasics.startYear%TYPE
)
LANGUAGE SQL
AS $$
	SELECT primaryTitle, startYear
    FROM titlebasics
    WHERE startYear >= 2022
    ORDER BY startYear;
$$;
/*
 The reason for some entries having start years in the future may be
 because these are intended releases for those years
 Other entries like where primarytitle = '100 Years' is either a typo,
 with its year being 2115, or it's actually a long time project movie
 that is filming continuously from the year 2015 to 2115.
 */

CREATE FUNCTION question3e()
RETURNS TABLE(
	titleType 		titleBasics.titleType%TYPE,
	primaryTitle 	titleBasics.primaryTitle%TYPE,
	startYear 		titleBasics.startYear%TYPE,
	endYear 		titleBasics.endYear%TYPE,
	runtimeMinutes 	titleBasics.runtimeMinutes%TYPE,
	genres 			titleBasics.genres%TYPE
)
LANGUAGE SQL
AS $$
	SELECT titleType,
       primaryTitle,
       startYear,
       endYear,
       runtimeMinutes,
       genres
    FROM titlebasics
    WHERE CAST(runtimeminutes AS INT) = (SELECT MAX(CAST(runtimeminutes AS INT)) FROM titlebasics);
$$;

CREATE FUNCTION question3f_distinctvalues()
RETURNS BIGINT
LANGUAGE SQL
AS $$
	SELECT COUNT(DISTINCT(genres)) FROM titlebasics;
$$;

CREATE FUNCTION question3f_limitclause()
RETURNS TABLE(
	genres 			titleBasics.genres%TYPE
)
LANGUAGE SQL
AS $$
	SELECT genres FROM titlebasics LIMIT 200;
$$;

CREATE FUNCTION question3g()
RETURNS TABLE(
	tconst 			titleBasics.tconst%TYPE,
	primaryTitle 	titleBasics.primaryTitle%TYPE,
	genres 			TEXT[]
)
LANGUAGE SQL
AS $$
	SELECT tconst, primarytitle, string_to_array(genres,',')
    FROM titlebasics
    WHERE CAST(runtimeminutes as INT) = 900;
$$;

CREATE FUNCTION question3h()
RETURNS TABLE(
	tconst 			titleBasics.tconst%TYPE,
	primaryTitle 	titleBasics.primaryTitle%TYPE,
	genre 			titleBasics.genres%TYPE
)
LANGUAGE SQL
AS $$
	SELECT tconst, primarytitle, UNNEST(string_to_array(genres,',')) AS genre
    FROM titlebasics
    WHERE CAST(runtimeminutes as INT) = 900
    ORDER BY tconst;
$$;

CREATE FUNCTION question3i()
RETURNS BIGINT
LANGUAGE SQL
AS $$
	SELECT COUNT(DISTINCT(x))
    FROM (SELECT UNNEST(string_to_array(genres,','))
    FROM titlebasics) as x;
$$;

CREATE FUNCTION question3j()
RETURNS TABLE(
	genre 			titleBasics.genres%TYPE,
	count 			BIGINT
)
LANGUAGE SQL
AS $$
	SELECT genre, COUNT(genre)
    FROM titlebasics, UNNEST(string_to_array(genres,',')) as genre
    GROUP BY genre
    ORDER BY COUNT(genre);
$$;

CREATE FUNCTION question3k()
RETURNS TABLE(
	primaryName 		nameBasics.primaryName%TYPE,
	birthYear 			nameBasics.birthYear%TYPE,
	deathYear 			nameBasics.deathYear%TYPE,
	primaryProfession 	nameBasics.primaryProfession%TYPE,
	knownForTitles 		nameBasics.knownForTitles%TYPE
)
LANGUAGE SQL
AS $$
	SELECT primaryName,
       birthYear,
       deathYear,
       primaryProfession,
       knownfortitles
    FROM namebasics
    WHERE primaryname LIKE 'Trump %' OR primaryname LIKE '% Trump';
$$;

CREATE FUNCTION question3l()
RETURNS TABLE(
	primaryName 	nameBasics.primaryName%TYPE,
	titleType 		titleBasics.titleType%TYPE,
	primaryTitle 	titleBasics.primaryTitle%TYPE,
	startYear 		titleBasics.startYear%TYPE
)
LANGUAGE SQL
AS $$
	SELECT primaryname,
       tb.titletype,
       tb.primarytitle,
       tb.startyear
    FROM titlebasics as tb JOIN (
        SELECT primaryname,birthyear,UNNEST(string_to_array(knownfortitles,',')) as tconst
        FROM namebasics
        WHERE CAST(birthyear AS INT) <= 1970 AND primaryname LIKE 'Trump %' OR primaryname LIKE '% Trump') AS nst ON tb.tconst = nst.tconst;
$$;

CREATE FUNCTION question3m()
RETURNS TABLE(
	primaryTitle 		titleBasics.primaryTitle%TYPE,
	originalTitle 		titleBasics.originalTitle%TYPE,
	isAdult 			titleBasics.isAdult%TYPE,
	startYear 			titleBasics.startYear%TYPE,
	endYear 			titleBasics.endYear%TYPE,
	runtimeMinutes 		titleBasics.runtimeMinutes%TYPE,
	genres 				titleBasics.genres%TYPE
)
LANGUAGE SQL
AS $$
	SELECT primaryTitle,
	       originalTitle,
	       isAdult,
	       startYear,
	       endYear,
	       runtimeMinutes,
	       genres
    FROM titlebasics
    WHERE primarytitle = 'Spider-Man' AND titletype = 'movie';
$$;

/*

---INDEX CREATION AND TIME COMPARISONS---


CREATE INDEX spiderman ON titlebasics (primarytitle, titletype, startyear);
CREATE INDEX
Time: 35571.781 ms (00:35.572)

SELECT primaryTitle,
    originalTitle,
    isAdult,
    startYear,
    endYear,
    runtimeMinutes,
    genres
FROM titlebasics
WHERE primarytitle = 'Spider-Man' AND titletype = 'movie';
 primarytitle | originaltitle | isadult | startyear | endyear | runtimeminutes |         genres
--------------+---------------+---------+-----------+---------+----------------+-------------------------
 Spider-Man   | Spider-Man    |       0 |      2002 |         | 121            | Action,Adventure,Sci-Fi
(1 row)


Time: 2.231 ms


--- COMPARING THE TIME WHEN THE INDEX IS REMOVED ---


DROP INDEX spiderman;
DROP INDEX
Time: 39.402 ms
SELECT primaryTitle,
    originalTitle,
    isAdult,
    startYear,
    endYear,
    runtimeMinutes,
    genres
FROM titlebasics
WHERE primarytitle = 'Spider-Man' AND titletype = 'movie';
 primarytitle | originaltitle | isadult | startyear | endyear | runtimeminutes |         genres
--------------+---------------+---------+-----------+---------+----------------+-------------------------
 Spider-Man   | Spider-Man    |       0 |      2002 |         | 121            | Action,Adventure,Sci-Fi
(1 row)


Time: 582.474 ms

*/

CREATE FUNCTION question3n()
RETURNS TABLE(
	primaryName 		nameBasics.primaryName%TYPE,
	birthYear 			nameBasics.birthYear%TYPE,
	primaryProfession 	nameBasics.primaryProfession%TYPE
)
LANGUAGE SQL
AS $$
    SELECT primaryname, birthyear, primaryprofession
    FROM namebasics, UNNEST(string_to_array(knownfortitles,',')) AS ttcode JOIN titlebasics as tb
    ON ttcode = tb.tconst
    WHERE tb.primarytitle = 'Spider-Man' and primaryprofession = 'actress';
$$;

CREATE FUNCTION question3o()
RETURNS TABLE(
	birthYear 		nameBasics.birthYear%TYPE,
	count 			BIGINT
)
LANGUAGE SQL
AS $$
	SELECT birthYear, COUNT(prof = 'actress')
    FROM namebasics,
         UNNEST(string_to_array(knownfortitles,',')) AS ttcode,
         UNNEST(string_to_array(primaryprofession,',')) AS prof
    WHERE ttcode = (SELECT tconst from titlebasics where primarytitle = 'Spider-Man' and titletype = 'movie')
    GROUP BY birthYear;
$$;
/*
 The data is very much incomplete. 1503 actresses who have been in spider man (2002)
 do not have a birth year listed.
 */
