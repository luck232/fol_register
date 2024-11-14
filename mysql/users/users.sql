CREATE USER 'registro'@'localhost' IDENTIFIED BY 'contraseña';

GRANT EXECUTE ON PROCEDURE users.sp_create_user TO 'registro'@'localhost';
GRANT EXECUTE ON PROCEDURE  users.sp_exist_user TO 'registro'@'localhost';

FLUSH PRIVILEGES;

