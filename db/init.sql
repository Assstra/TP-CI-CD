CREATE TABLE city (
    id SERIAL PRIMARY KEY,
    department_code character varying(255) NOT NULL,
    insee_code character varying(255),
    zip_code character varying(255),
    name character varying(255) NOT NULL,
    lat float NOT NULL,
    lon float NOT NULL 
);