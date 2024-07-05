CREATE TABLE imagenes (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    caracteristicas FLOAT8[]
);

CREATE OR REPLACE FUNCTION cosine_distance(a double precision[], b double precision[])
 RETURNS double precision
 LANGUAGE plpgsql
 IMMUTABLE
AS $function$
DECLARE
    dot_product FLOAT8 = 0;
    norm_a FLOAT8 = 0;
    norm_b FLOAT8 = 0;
    cosine_similarity FLOAT8;
    i INT;
BEGIN
    IF array_length(a, 1) <> array_length(b, 1) THEN
        RAISE EXCEPTION 'Arrays must be of the same length';
    END IF;

    FOR i IN 1..array_length(a, 1) LOOP
        dot_product := dot_product + (a[i] * b[i]);
        norm_a := norm_a + (a[i] * a[i]);
        norm_b := norm_b + (b[i] * b[i]);
    END LOOP;

    IF norm_a = 0 OR norm_b = 0 THEN
        RETURN 1;
    END IF;

    cosine_similarity := dot_product / (sqrt(norm_a) * sqrt(norm_b));
    RETURN 1 - cosine_similarity;
END;
$function$
