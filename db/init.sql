use shop;
CREATE TABLE product(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price FLOAT);
INSERT INTO product (name, price) VALUES ('jouet', 15), ('pc', 250);