DROP TABLE IF EXISTS alembic_version;


CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INSERT INTO alembic_version (version_num) VALUES ('5d594cf24bd0');
