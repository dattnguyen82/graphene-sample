DROP SCHEMA IF EXISTS gql_sample CASCADE;
CREATE SCHEMA gql_sample;

DROP TABLE IF EXISTS gql_sample.enterprise;
CREATE TABLE gql_sample.enterprise (
  id serial PRIMARY KEY,
  name varchar(64) DEFAULT NULL,
  description varchar(256) DEFAULT NULL
);


DROP TABLE IF EXISTS gql_sample.site;
CREATE TABLE gql_sample.site (
  id serial PRIMARY KEY,
  name varchar(64) DEFAULT NULL,
  description varchar(256) DEFAULT NULL,
  enterprise_id integer DEFAULT NULL
);


DROP TABLE IF EXISTS gql_sample.segment;
CREATE TABLE gql_sample.segment (
  id serial PRIMARY KEY,
  name varchar(64) DEFAULT NULL,
  description varchar(256) DEFAULT NULL,
  site_id integer DEFAULT NULL
);


DROP TABLE IF EXISTS gql_sample.asset;
CREATE TABLE gql_sample.asset (
  id serial PRIMARY KEY,
  name varchar(64) DEFAULT NULL,
  description varchar(256) DEFAULT NULL,
  segment_id integer DEFAULT NULL
);