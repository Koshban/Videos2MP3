CREATE USER 'auth_user'@'locahost' IDENTIFIED BY 'Auth123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* to 'auth_user'@'locahost';

USE auth;

CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user(email, password) VALUES ( 'kaushik.banerjee77@gmail.com', 'Admin123');

show databases; 