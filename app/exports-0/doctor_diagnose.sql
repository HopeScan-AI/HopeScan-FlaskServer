DROP TABLE IF EXISTS doctor_diagnose;


CREATE TABLE doctor_diagnose (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	image_drive_id VARCHAR(50) NOT NULL, 
	diagnose VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(image_drive_id) REFERENCES drive_image (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO doctor_diagnose (id, user_id, image_drive_id, diagnose) VALUES (1, 1, '1--FlDvu5JqzzwSAdUJszODkqTtYd7Rpm', 'benign');
INSERT INTO doctor_diagnose (id, user_id, image_drive_id, diagnose) VALUES (2, 1, '1--hOcEB2eGq2QJqi-jmBKu1XTw2qcxfN', 'normal');
