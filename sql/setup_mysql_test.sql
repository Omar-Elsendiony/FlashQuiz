-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS flash_quiz_test_db;
CREATE USER IF NOT EXISTS 'flash_quiz_test'@'localhost' IDENTIFIED BY 'flash_quiz_test_pwd';
GRANT ALL PRIVILEGES ON `flash_quiz_test_db`.* TO 'flash_quiz_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'flash_quiz_test'@'localhost';
FLUSH PRIVILEGES;
