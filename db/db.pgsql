DO $$
BEGIN
    IF NOT EXISTS (SELECT * FROM pg_extension WHERE extname='postgis') THEN
        CREATE EXTENSION postgis;
    END IF;
    IF NOT EXISTS (SELECT * FROM pg_extension WHERE extname='pgcrypto') THEN
        CREATE EXTENSION pgcrypto;
    END IF;
END$$;


CREATE TABLE IF NOT EXISTS apartments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    no_bed INT NOT NULL,
    no_bath INT NOT NULL,
    no_toilets INT NOT NULL,
    price FLOAT NOT NULL,
    url VARCHAR(350) NOT NULL,
    agent_phone VARCHAR(350) NOT NULL,
    agent_name VARCHAR(350) NOT NULL,
    date_added TIMESTAMPTZ NOT NULL,
    latLng GEOGRAPHY(Point)
);