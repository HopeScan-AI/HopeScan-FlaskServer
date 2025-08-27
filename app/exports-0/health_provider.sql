DROP TABLE IF EXISTS health_provider;


CREATE TABLE health_provider (
	id INTEGER NOT NULL, 
	provider_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(provider_id) REFERENCES users (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO health_provider (id, provider_id, user_id, status) VALUES (2, 5, 6, 'accepted');
INSERT INTO health_provider (id, provider_id, user_id, status) VALUES (4, 2, 1, 'accepted');
INSERT INTO health_provider (id, provider_id, user_id, status) VALUES (5, 2, 3, 'declined');
