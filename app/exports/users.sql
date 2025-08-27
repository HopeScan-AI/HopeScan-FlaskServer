DROP TABLE IF EXISTS users;


CREATE TABLE users (
	id INTEGER NOT NULL, 
	name VARCHAR(50), 
	email VARCHAR(100), 
	password VARCHAR(255), 
	role VARCHAR(10), 
	verification_code VARCHAR(10), 
	is_verified BOOLEAN, 
	provider VARCHAR(20), 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	deleted_at DATETIME, 
	created_by INTEGER, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (1, 'Admin', 'admin@admin.com', '$2b$12$Z0Kte0AlD1VSkdINvwYsCOF2xzQldNhwVo5ScK0ikVAiHBmEFCi6e', 'admin', '929170', True, 'email', '2025-01-30 19:49:47', '2025-02-01 19:01:32', NULL, NULL, NULL);
INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (2, 'User', 'user@user.com', '$2b$12$RWI6qtfR0l2tcndzcbgHd.b793YMRZuMxpe3EsMddakiEmzRd874q', 'user', NULL, True, 'email', '2025-01-30 19:56:19', '2025-01-31 12:41:30', NULL, NULL, NULL);
INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (3, 'Institution', 'institution@institution.com', '$2b$12$Bq.7uO.SAz1WAFPtOMT7CO6s900.BNI6xhtr55f5UT8vXdcgwTbRS', 'institution', NULL, True, 'email', '2025-01-30 19:56:48', '2025-01-30 19:56:48', NULL, NULL, NULL);
INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (4, 'Annotator', 'annotator@annotator.com', '$2b$12$YkQukrXNKLUvhwELbuj4n.OX/QgDa3/URBefMJR.1kR8S/8ynCnaC', 'annotator', NULL, True, 'email', '2025-01-30 19:57:29', '2025-01-31 07:34:16', NULL, NULL, NULL);
INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (5, 'Raed S. Rasheed', 'raed.rasheed@gmail.com', '$2b$12$IcuwCYn3cD8qu/zoTVYytuhHZ5KqBps6ExXTC603Gmhpbwux0c9Me', 'user', '883927', True, 'email', '2025-01-31 07:38:33', '2025-01-31 07:39:17', NULL, NULL, NULL);
INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (6, 'Raed S. Rasheed', 'raed.rasheed@yahoo.com', '$2b$12$cNqvozejypSXyTeKi8YBFuOkIYseiDzNvCUxrpncyU3w5kzVX4.li', 'institution', '317271', True, 'email', '2025-01-31 07:40:03', '2025-01-31 07:40:56', NULL, NULL, NULL);
INSERT INTO users (id, name, email, password, role, verification_code, is_verified, provider, created_at, updated_at, deleted_at, created_by, deleted_by) VALUES (7, 'Ahmed S. Ghorab', 'aghorab.2022@gmail.com', '$2b$12$d4eM1ELG1nzoaAejSwV8CuEfhy4.RsT6MPvvyYy.HW7Puq2DEd9xG', 'admin', NULL, True, 'email', '2025-02-02 10:51:03', '2025-02-02 10:51:03', NULL, NULL, NULL);
