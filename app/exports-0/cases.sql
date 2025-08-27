DROP TABLE IF EXISTS cases;


CREATE TABLE cases (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	create_date DATE NOT NULL, 
	comments TEXT, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	deleted_at DATETIME, 
	created_by INTEGER, 
	deleted_by INTEGER, 
	updated_by INTEGER, 
	creator_id INTEGER NOT NULL, 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator_id) REFERENCES users (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);

INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (14, 'test', '2025-02-01', '', '2025-02-01 19:43:36', '2025-02-01 19:43:36', NULL, 1, NULL, NULL, 1, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (15, 'Admin', '2025-02-02', '', '2025-02-02 17:35:15', '2025-02-02 17:35:15', NULL, NULL, NULL, NULL, 2, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (16, 'Admin', '2025-02-02', '', '2025-02-02 17:36:34', '2025-02-02 17:36:34', NULL, NULL, NULL, NULL, 2, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (17, 'asd', '2025-02-02', '', '2025-02-02 17:37:28', '2025-02-02 17:37:28', NULL, NULL, NULL, NULL, 2, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (18, 'Amal', '2025-02-03', 'Hi', '2025-02-03 09:03:42', '2025-02-03 09:03:42', NULL, NULL, NULL, NULL, 5, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (19, 'Alaa', '2025-02-03', 'Normal', '2025-02-03 09:04:17', '2025-02-03 09:04:17', NULL, NULL, NULL, NULL, 5, 6);
