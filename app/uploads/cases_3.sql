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

INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (14, 'testsss', '2025-02-01', 'sasas', '2025-02-01 19:43:36', '2025-02-17 13:47:46', NULL, 1, NULL, NULL, 1, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (15, 'Admin', '2025-02-02', '', '2025-02-02 17:35:15', '2025-02-02 17:35:15', NULL, NULL, NULL, NULL, 2, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (16, 'Admin', '2025-02-02', '', '2025-02-02 17:36:34', '2025-02-02 17:36:34', NULL, NULL, NULL, NULL, 2, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (17, 'asd', '2025-02-02', '', '2025-02-02 17:37:28', '2025-02-02 17:37:28', NULL, NULL, NULL, NULL, 2, 1);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (18, 'Amal', '2025-02-03', 'Hi', '2025-02-03 09:03:42', '2025-02-03 09:03:42', NULL, NULL, NULL, NULL, 5, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (19, 'Alaa', '2025-02-03', 'Normal', '2025-02-03 09:04:17', '2025-02-03 09:04:17', NULL, NULL, NULL, NULL, 5, 6);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (23, 'user test', '2025-02-04', '', '2025-02-04 05:31:49', '2025-02-06 20:11:19', NULL, NULL, NULL, NULL, 2, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (30, 'fayez maliha', '2025-02-05', '', '2025-02-05 19:42:00', '2025-02-06 20:00:18', NULL, NULL, NULL, NULL, 2, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (31, 'test case', '2025-02-17', 'sasasa', '2025-02-17 12:51:21', '2025-02-17 12:51:21', NULL, NULL, NULL, NULL, 8, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (32, 'assa', '2025-02-07', 'asas', '2025-02-17 13:10:01', '2025-02-17 13:10:01', NULL, NULL, NULL, NULL, 8, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (33, 'saassa', '2025-02-07', 'assasa', '2025-02-17 13:10:13', '2025-02-17 13:10:13', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (34, 'sddsds', '2025-02-13', 'dsdsds', '2025-02-17 13:12:15', '2025-02-17 13:12:15', NULL, NULL, NULL, NULL, 9, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (35, 'cc', '2025-02-03', 'sddsds', '2025-02-17 13:12:31', '2025-02-17 13:12:31', NULL, NULL, NULL, NULL, 9, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (36, 'xx', '2025-02-26', 'xx', '2025-02-17 13:15:59', '2025-02-17 13:15:59', NULL, NULL, NULL, NULL, 9, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (37, '1', '2025-02-19', '1', '2025-02-17 13:24:01', '2025-02-17 13:24:01', NULL, NULL, NULL, NULL, 9, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (38, '2', '2025-02-06', '2', '2025-02-17 13:24:31', '2025-02-17 13:24:31', NULL, NULL, NULL, NULL, 9, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (39, '3', '2025-02-05', '3', '2025-02-17 13:29:10', '2025-02-17 13:29:10', NULL, NULL, NULL, NULL, 8, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (40, '4', '2025-02-20', '4', '2025-02-17 13:29:44', '2025-02-17 13:29:44', NULL, NULL, NULL, NULL, 9, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (41, '5', '2025-02-17', '5', '2025-02-17 13:30:21', '2025-02-17 13:30:21', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (42, '6', '2025-02-19', '6', '2025-02-17 13:30:31', '2025-02-17 13:30:31', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (43, '7', '2025-02-12', '7', '2025-02-17 13:34:57', '2025-02-17 13:34:57', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (44, '8', '2025-02-12', '8', '2025-02-17 13:42:33', '2025-02-17 13:42:33', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (45, '9', '2025-02-05', '9', '2025-02-17 13:42:48', '2025-02-17 13:42:48', NULL, NULL, NULL, NULL, 8, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (46, '10', '2025-02-17', 'cc', '2025-02-17 13:43:32', '2025-02-17 13:43:32', NULL, NULL, NULL, NULL, 9, 9);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (47, '11', '2025-02-05', 'cc', '2025-02-17 13:43:45', '2025-02-17 13:43:45', NULL, NULL, NULL, NULL, 8, 9);
