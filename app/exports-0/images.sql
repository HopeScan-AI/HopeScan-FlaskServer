DROP TABLE IF EXISTS images;


CREATE TABLE images (
	id INTEGER NOT NULL, 
	file_name VARCHAR(255) NOT NULL, 
	file_path VARCHAR(500) NOT NULL, 
	diagnose VARCHAR(500), 
	comments TEXT, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME, 
	case_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES cases (id)
);

INSERT INTO images (id, file_name, file_path, diagnose, comments, created_at, updated_at, case_id) VALUES (1, 'WhatsApp_Image_2024-12-30_at_21.47.49.png', 'uploaded_images/5_18_1738573570.47', 'test diagnose', 'test comments', '2025-02-03 09:06:10', NULL, 18);
INSERT INTO images (id, file_name, file_path, diagnose, comments, created_at, updated_at, case_id) VALUES (2, 'WhatsApp_Image_2024-12-30_at_21.47.49_-_Copy.jpeg', 'uploaded_images/5_18_1738573582.47', 'test diagnose', 'test comments', '2025-02-03 09:06:22', NULL, 18);
