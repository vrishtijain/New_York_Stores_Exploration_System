-- DROP DATABASE IF EXISTS project;
-- CREATE DATABASE project;

-- DROP USER IF EXISTS project;
-- CREATE USER project
-- WITH PASSWORD 'project';

-- GRANT ALL PRIVILEGES ON DATABASE project TO project;



drop table   if exists    retail_food_stores
;
CREATE TABLE retail_food_stores
(
    license VARCHAR(6) PRIMARY KEY,
    establishment_type VARCHAR(32),
    entity_name VARCHAR(150),
    DBA_name VARCHAR(256),
    street_number VARCHAR(32),
    street_name VARCHAR(64),

    -- this field is empty in each row, not sure whether  overall this should be 
    --part of schema or not. 
    -- address_line2 VARCHAR(64),
    -- address_line3 VARCHAR(64),
    city VARCHAR(32),
    state VARCHAR(2),
    operation_type VARCHAR(32),
    zip_code INTEGER CHECK ( zip_code <100000),
    square_footage INTEGER,
    FOREIGN KEY  ( zip_code ) REFERENCES global_county_zip_code(zip)
    --location is a string made up of street_number+street_name+city + state+ zipcode

);

drop table    if exists  authorised_liquor_store
CASCADE;
CREATE TABLE authorised_liquor_store
(
    serial_number INTEGER PRIMARY KEY,
    -- county VARCHAR(20),
    license_type_code VARCHAR(2),
    license_class_code INTEGER CHECK (license_class_code >99 and license_class_code < 1000),
    certificate_number INTEGER ,
    premise_name VARCHAR(100),
    DBA VARCHAR(256),
    license_issued_date DATE,
    license_expiration_date DATE,
    method_of_operation VARCHAR(256)

);


drop table   if exists liquor_address
;
CREATE TABLE liquor_address
(
    -- as mostly the add2 was empty. 
    serial_number INTEGER,
    premise_address VARCHAR(128),
    city VARCHAR(32),
    state VARCHAR(2),
    premise_zip_code INTEGER CHECK ( premise_zip_code <100000),
    -- removed this premise_address2 VARCHAR(128),
    georeferences VARCHAR(64),
    FOREIGN KEY  ( serial_number ) REFERENCES authorised_liquor_store(serial_number),
    FOREIGN KEY  ( premise_zip_code ) REFERENCES global_county_zip_code(zip)

);




-- 3rd dataset
drop table   if exists farmers_market;
CREATE TABLE farmers_market
(
    market_name VARCHAR(256) PRIMARY KEY,
    -- county VARCHAR(20),
    address_line1 VARCHAR(256),
    city VARCHAR(64),
    zip INTEGER CHECK (zip <100000),
    contact VARCHAR(64),
    state VARCHAR(2),
    phone VARCHAR(32),
    marklet_link VARCHAR(256),
    operation_hours VARCHAR(150),
    operation_season VARCHAR(150),
    operation_month VARCHAR(10),
    fnmp VARCHAR(1),
    snap VARCHAR(1),
    fcc_issued VARCHAR(1),
    fcc_accepted VARCHAR(1),
    latitude DECIMAL,
    longitude DECIMAL,
    FOREIGN KEY  (zip) REFERENCES global_county_zip_code(zip) ON UPDATE CASCADE ON DELETE SET NULL
);


drop table   if exists global_county_zip_code
CASCADE;
CREATE TABLE global_county_zip_code
(

    zip INTEGER CHECK ( zip <100000) PRIMARY KEY,
    county VARCHAR(20)


);




