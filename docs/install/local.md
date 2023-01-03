# Base de datos

Procedemos a crear una base de datos

    CREATE DATABASE www_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Crear un usuario que tenga permisos a acceder a esta base de datos. Para omitir el root

    GRANT ALL PRIVILEGES ON www_test.* TO 'www_test'@'localhost' IDENTIFIED BY 'www_test' WITH GRANT OPTION;
    FLUSH PRIVILEGES;   