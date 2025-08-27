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

INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (14, 'test', '2025-02-01', '', '2025-02-01 19:43:36', '2025-02-12 13:21:23', NULL, 1, NULL, NULL, 2, 13);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (15, 'Admin', '2025-02-02', '', '2025-02-02 17:35:15', '2025-02-12 12:34:08', NULL, NULL, NULL, NULL, 2, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (16, 'Admin', '2025-02-02', '', '2025-02-02 17:36:34', '2025-02-12 13:21:54', NULL, NULL, NULL, NULL, 8, 13);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (17, 'asd', '2025-02-02', '', '2025-02-02 17:37:28', '2025-02-12 12:34:29', NULL, NULL, NULL, NULL, 2, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (18, 'Amal', '2025-02-03', 'Hi', '2025-02-03 09:03:42', '2025-02-12 13:20:58', NULL, NULL, NULL, NULL, 2, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (19, 'Alaa', '2025-02-03', 'Normal', '2025-02-03 09:04:17', '2025-02-12 13:21:32', NULL, NULL, NULL, NULL, 8, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (21, 'fayez maliha', '2025-02-04', '', '2025-02-04 05:17:30', '2025-02-04 05:17:30', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (22, 'Admin', '2025-02-04', '', '2025-02-04 05:19:44', '2025-02-12 13:22:15', NULL, NULL, NULL, NULL, 8, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (23, 'user test', '2025-02-04', '', '2025-02-04 05:31:49', '2025-02-06 20:11:19', NULL, NULL, NULL, NULL, 2, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (24, 'asd', '2025-02-04', '', '2025-02-04 05:33:46', '2025-02-05 19:34:43', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (25, 'test1', '2025-02-04', '', '2025-02-04 18:09:53', '2025-02-12 13:24:11', NULL, NULL, NULL, NULL, 8, 13);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (26, 'aaaaaaaa', '2025-02-04', '', '2025-02-04 18:35:58', '2025-02-12 13:24:35', NULL, NULL, NULL, NULL, 8, 13);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (27, 'bbbbbbbb', '2025-02-04', '', '2025-02-04 18:36:35', '2025-02-05 19:30:25', NULL, NULL, NULL, NULL, 8, 8);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (28, 'Admin', '2025-02-05', '', '2025-02-05 19:24:22', '2025-02-12 12:44:37', NULL, NULL, NULL, NULL, 3, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (29, 'fayez maliha', '2025-02-05', '', '2025-02-05 19:38:17', '2025-02-12 13:25:01', NULL, NULL, NULL, NULL, 2, 13);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (30, 'fayez maliha', '2025-02-05', '', '2025-02-05 19:42:00', '2025-02-06 20:00:18', NULL, NULL, NULL, NULL, 2, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (31, 'buildIn', '2025-02-05', '', '2025-02-05 19:43:00', '2025-02-06 19:37:51', NULL, NULL, NULL, NULL, 8, 3);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (32, 'ttt', '2025-02-09', 'cc', '2025-02-09 16:31:22', '2025-02-09 16:31:22', NULL, NULL, NULL, NULL, 1, 0);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (33, 'ccc', '2025-02-05', 'cc', '2025-02-09 17:36:43', '2025-02-09 17:36:43', NULL, NULL, NULL, NULL, 1, 0);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (34, 'test case', '2025-02-06', 'cc', '2025-02-09 17:45:37', '2025-02-09 17:45:37', NULL, NULL, NULL, NULL, 1, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (35, 'nn1', '2025-02-09', 'cc', '2025-02-09 17:46:19', '2025-02-09 17:46:19', NULL, NULL, NULL, NULL, 1, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (36, 'حالة جديدة تعديل ', '2025-02-27', 'تعليق  تعديل ', '2025-02-12 09:53:19', '2025-02-12 10:44:00', NULL, NULL, NULL, NULL, 7, 7);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (37, 'Admin cases', '2025-02-21', 'Admin case comment', '2025-02-21 15:33:52', '2025-03-24 13:44:52', NULL, NULL, NULL, NULL, 2, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (38, 'asasx', '2025-03-24', 'sas', '2025-03-24 13:35:36', '2025-03-24 13:47:15', NULL, NULL, NULL, NULL, 2, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (39, 'ssasa', '2025-03-24', 'aass', '2025-03-24 13:47:37', '2025-03-24 13:52:56', NULL, NULL, NULL, NULL, 2, 2);
INSERT INTO cases (id, name, create_date, comments, created_at, updated_at, deleted_at, created_by, deleted_by, updated_by, creator_id, owner_id) VALUES (40, 'fffff', '2025-03-24', 'ffff', '2025-03-24 13:53:33', '2025-03-24 13:53:33', NULL, NULL, NULL, NULL, 1, 1);
