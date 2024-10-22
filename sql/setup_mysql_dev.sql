-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS flash_quiz_dev_db;
CREATE USER IF NOT EXISTS 'flash_quiz_dev'@'localhost' IDENTIFIED BY 'flash_quiz_dev_pwd';
GRANT ALL PRIVILEGES ON `flash_quiz_dev_db`.* TO 'flash_quiz_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'flash_quiz_dev'@'localhost';
FLUSH PRIVILEGES;
