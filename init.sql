CREATE DATABASE IF NOT EXISTS rabbitmqdata;
USE rabbitmqdata;
CREATE TABLE IF NOT EXISTS customer ( id INT AUTO_INCREMENT,username VARCHAR(30), password VARCHAR(30), PRIMARY KEY (id));

