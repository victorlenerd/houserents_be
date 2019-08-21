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
    address VARCHAR(350) NOT NULL,
    description TEXT NOT NULL,
    source VARCHAR(350) NOT NULL,
    date_added TIMESTAMPTZ NOT NULL,
    latLng GEOGRAPHY(Point) NOT NULL
);

CREATE TABLE IF NOT EXISTS roomies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    firstname VARCHAR(350) NOT NULL,
    lastname VARCHAR(350) NOT NULL,
    occupation VARCHAR(350) NOT NULL,
    school VARCHAR(350) NOT NULL,
    sex VARCHAR(350) NOT NULL,
    smokes BOOLEAN NOT NULL,
    pets BOOLEAN NOT NULL,
    dob VARCHAR(100) NOT NULL,
    photo VARCHAR(350) NOT NULL,
    email VARCHAR(350) NOT NULL,
    budget FLOAT NOT NULL,
    firstloc GEOGRAPHY(Point) NOT NULL,
    secondloc GEOGRAPHY(Point) NOT NULL,
    thirdloc GEOGRAPHY(Point) NULL,
    no_bed INT NOT NULL,
    no_bath INT NOT NULL,
    no_toilets INT NOT NULL
);


ALTER TABLE apartments ADD COLUMN IF NOT EXISTS views INT DEFAULT 0;