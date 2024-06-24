START TRANSACTION;
INSERT INTO customer (mail_id, phone_number, customer_pass, address_id)
VALUES ('john.doe@example.com', '1234567890', 'Password123', 1);
-- This will fail because the mail ID or phone number already exists
INSERT INTO customer (mail_id, phone_number, customer_pass, address_id)
VALUES ('john.doe@example.com', '9876543210', 'Password456', 2);
COMMIT;


START TRANSACTION;
UPDATE product
SET quantity = 20
WHERE product_id = 1;
-- This will fail because the available quantity is less than the updated quantity
INSERT INTO cart(customer_id,product_id,quantity) value (1,1,50);
COMMIT;


START TRANSACTION;
INSERT INTO cart(customer_id,product_id,quantity) value (1,2,5);
-- This will fail because the available quantity is less than the updated quantity
INSERT INTO cart(customer_id,product_id,quantity) value (2,2,20);
COMMIT;


START TRANSACTION;
-- The partner_id = 1 is being allocated a order
UPDATE partner SET status = 1 WHERE partner_id = 1;
-- At the same time another order is being allocated to the same partner this is conflicting statement
UPDATE partner SET status = 1 WHERE partner_id = 1;
COMMIT;





-- NON CONFLICTING TRANSACTIONS
START TRANSACTION;
INSERT INTO customer (mail_id, phone_number, customer_pass, address_id)
VALUES ('john.doe@example.com', '1234567890', 'Password123', 1);
INSERT INTO address (city, pincode, state)
VALUES ('New York', 10001, 'NY');
COMMIT;


START TRANSACTION;
INSERT INTO product (category_id, supplier_id, store_id, name, price, quantity)
VALUES (1, 1, 1, 'Laptop', 1000, 10);
INSERT INTO category (category_name)
VALUES ('Electronics');
COMMIT;



START TRANSACTION;
INSERT INTO payment (customer_id, payment_type, payment_date)
VALUES (1, 'Debit Card', '2023-03-16');
INSERT INTO orders (customer_id, partner_id, order_date, amount)
VALUES (1, 1, '2023-03-16', 200);
COMMIT;


START TRANSACTION;
INSERT INTO supplier (name, phone_number) VALUES ('Supplier C', '9876543210');
INSERT INTO product (category_id, supplier_id, store_id, name, price, quantity) VALUES (3, LAST_INSERT_ID(), 3, 'Cold Coffee', 100, 200);
SELECT * FROM product WHERE supplier_id = LAST_INSERT_ID();
COMMIT;

