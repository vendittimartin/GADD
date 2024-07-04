CREATE TABLE imagenes (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    caracteristicas FLOAT8[]
);

CREATE OR REPLACE FUNCTION euclidean_distance(a FLOAT8[], b FLOAT8[])
RETURNS FLOAT8 AS $$
DECLARE
    sum FLOAT8 = 0;
    i INT;
BEGIN
    IF array_length(a, 1) <> array_length(b, 1) THEN
        RAISE EXCEPTION 'Arrays must be of the same length';
    END IF;

    FOR i IN 1..array_length(a, 1) LOOP
        sum := sum + (a[i] - b[i]) * (a[i] - b[i]);
    END LOOP;

    RETURN sqrt(sum);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION obtener_similares(input_features FLOAT8[])
RETURNS TABLE(result_url TEXT, distancia FLOAT8) AS $$
BEGIN
    RETURN QUERY
    SELECT url, 
           euclidean_distance(caracteristicas, input_features) AS distancia
    FROM imagenes
    ORDER BY distancia
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;
