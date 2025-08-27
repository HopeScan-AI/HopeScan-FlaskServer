DROP TABLE IF EXISTS notifications;


CREATE TABLE notifications (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	is_read BOOLEAN, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	action_url VARCHAR(255), 
	title VARCHAR(255), 
	message VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (1, 2, True, '2025-01-30 20:10:43', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (2, 2, True, '2025-01-30 21:13:29', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (3, 2, True, '2025-01-30 21:20:05', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (4, 2, True, '2025-01-30 21:20:30', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (5, 2, True, '2025-01-30 21:21:41', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (6, 5, True, '2025-01-31 07:41:32', '/provider/join-institution/6', 'Invite to institution', 'Institution Raed S. Rasheed is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (7, 5, True, '2025-01-31 07:50:02', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (8, 2, True, '2025-02-02 16:43:42', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (9, 2, True, '2025-02-02 16:43:44', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (10, 2, True, '2025-02-02 16:46:04', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (11, 2, True, '2025-02-02 16:48:52', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (12, 2, True, '2025-02-02 16:51:13', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (13, 2, True, '2025-02-02 16:51:34', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (14, 2, True, '2025-02-02 16:52:00', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (15, 2, True, '2025-02-02 16:52:34', '/provider/join-institution/1', 'Invite to institution', 'Institution Admin is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (16, 2, True, '2025-02-02 17:05:46', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (17, 2, True, '2025-02-02 17:05:55', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (18, 2, True, '2025-02-02 17:51:31', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (19, 2, True, '2025-02-02 17:51:39', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (20, 2, True, '2025-02-02 17:53:21', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (21, 2, True, '2025-02-02 17:53:49', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
INSERT INTO notifications (id, user_id, is_read, created_at, action_url, title, message) VALUES (22, 2, True, '2025-02-02 17:54:08', '/provider/join-institution/3', 'Invite to institution', 'Institution Institution is inviting you to join them');
