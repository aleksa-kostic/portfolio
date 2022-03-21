select count(*) from tokens;

select count(f)
from (select distinct(fullpath) from tokens) as f;

select count(distinct(fullpath)) from tokens;

select count(fullpath)
from tokens
where token like '%child%';

select count(f)
from (select distinct(fullpath)
    from tokens
    where token like '%child%') as f;

select token, dir, file, frequency
from tokens
where token like 'child';

select fullpath, frequency from tokens where token like 'child';



select token, dir, file, frequency
from tokens
where token like 'fdsafdsafdsafdsfasdfdasf';

COPY tokens TO 'C:\Users\aKost\Desktop\2021-2022\WINTER 2022\CS 121 - Information Retrieval\project3\tokens.csv' DELIMITER ',' CSV HEADER;
