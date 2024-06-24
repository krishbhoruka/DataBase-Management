create database retail_shop;
use retail_shop;

CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_pass VARCHAR(20) NOT NULL CHECK (
        LENGTH(admin_pass) BETWEEN 8 AND 20 
    ),
    admin_state VARCHAR(20) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS address (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    pincode INT NOT NULL CHECK (LENGTH(pincode) = 5),
    state VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS customer(
    customer_id INT PRIMARY KEY auto_increment,
    mail_id VARCHAR(50) NOT NULL UNIQUE,
    address_id INT,
    phone_number VARCHAR(10) NOT NULL UNIQUE,
    customer_pass VARCHAR(20) NOT NULL,
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    CHECK (CHAR_LENGTH(customer_pass) BETWEEN 8 AND 20),
    CHECK (CHAR_LENGTH(phone_number) = 10),
    CONSTRAINT CK_Password_Alphanumeric CHECK (customer_pass REGEXP '[0-9]' AND customer_pass REGEXP '[a-zA-Z]')
);


CREATE TABLE IF NOT EXISTS supplier(
supplier_id INT PRIMARY KEY auto_increment,
name VARCHAR(50) NOT NULL,
phone_number VARCHAR(10) NOT NULL unique,
CHECK (CHAR_LENGTH(phone_number) = 10)
);


CREATE TABLE IF NOT EXISTS Manager(
manager_id INT PRIMARY KEY auto_increment,
address_id INT,
admin_id INT,
name VARCHAR(50) NOT NULL,
password VARCHAR(20) NOT NULL ,
phone_number VARCHAR(10) NOT NULL unique,
FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
CHECK (CHAR_LENGTH(phone_number) = 10),
FOREIGN KEY (address_id) REFERENCES address(address_id),
CHECK (CHAR_LENGTH(password) BETWEEN 8 AND 20),
CONSTRAINT CK_Password_Alphanumeric_ CHECK (password REGEXP '[0-9]' AND password REGEXP '[a-zA-Z]')
);


CREATE TABLE IF NOT EXISTS partner(
partner_id INT PRIMARY KEY auto_increment,
address_id INT,
manager_id INT,
name VARCHAR(15) NOT NULL,
phone_number VARCHAR(10) NOT NULL unique,
CHECK (CHAR_LENGTH(phone_number) = 10),
status INT NOT NULL,
CHECK (CHAR_LENGTH(status) = 1),
FOREIGN KEY (address_id) REFERENCES address(address_id),
FOREIGN KEY (manager_id) REFERENCES manager(manager_id)
);

CREATE TABLE IF NOT EXISTS category(
category_id INT PRIMARY KEY auto_increment,
category_name VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS store(
store_id INT PRIMARY KEY auto_increment,
manager_id INT,
city VARCHAR(50) NOT NULL,
FOREIGN KEY (manager_id) REFERENCES manager(manager_id)
);


CREATE TABLE IF NOT EXISTS payment(
payment_id INT PRIMARY KEY auto_increment,
customer_id INT,
payment_type VARCHAR(20) NOT NULL,
payment_date DATE,
FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);


CREATE TABLE IF NOT EXISTS orders(
order_id INT PRIMARY KEY auto_increment,
partner_id INT,
customer_id INT,
payment_id INT,
order_date DATE NOT NULL,
amount INT,
FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
FOREIGN KEY (partner_id) REFERENCES partner(partner_id),
FOREIGN KEY (payment_id) REFERENCES payment(payment_id)
);


CREATE TABLE IF NOT EXISTS product(
product_id INT PRIMARY KEY auto_increment,
category_id INT,
supplier_id INT,
store_id INT,
name VARCHAR(50) NOT NULL,
price INT NOT NULL,
quantity INT,
FOREIGN KEY (category_id) REFERENCES category(category_id),
FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
FOREIGN KEY (store_id) REFERENCES store(store_id)
);


CREATE TABLE IF NOT EXISTS cart(
customer_id INT,
product_id INT,
quantity INT NOT NULL,
product_amount INT,
FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE cart_total_amount(
customer_id INT,
total_amount INT default 0,
FOREIGN KEY (customer_id) references customer(customer_id)
);


truncate TABLE payment;
truncate TABLE cart;
truncate TABLE orders;
truncate TABLE cart_total_amount;


SELECT * FROM orders;
SELECT * FROM payment;
SELECT * FROM cart;
SELECT * FROM cart_total_amount;
SELECT * FROM product;