CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          VARCHAR(20)  NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work (creation_date);

CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    person_id    uuid         NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id uuid         NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role         VARCHAR(32) NOT NULL,
    created      timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    genre_id     uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created      timestamp with time zone
);


CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.genre_film_work (film_work_id, genre_id);
