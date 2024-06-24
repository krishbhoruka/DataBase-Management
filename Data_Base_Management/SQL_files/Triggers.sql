use retail_shop;

DELIMITER $$
CREATE TRIGGER cart_item_add
BEFORE INSERT
ON cart
FOR EACH ROW
BEGIN
    -- Calculate product_amount for the newly inserted row in cart
    SET NEW.product_amount = (
        SELECT P.price * NEW.quantity
        FROM product P
        WHERE P.product_id = NEW.product_id
    );
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER cart_total_amount_update
AFTER INSERT
ON cart
FOR EACH ROW
BEGIN
    -- Update total_amount in cart_total_amount table
    UPDATE cart_total_amount CTA
    SET total_amount = (
        SELECT SUM(product_amount)
        FROM cart
        WHERE cart.customer_id = NEW.customer_id
    )
    WHERE CTA.customer_id = NEW.customer_id;
END $$
DELIMITER ;



DELIMITER $$
CREATE TRIGGER customer_analysis_update
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update in customer_analysis table
    UPDATE customer_analysis CA
    SET total_amount_order = total_amount_order + (
            SELECT total_amount
            FROM cart_total_amount
            WHERE cart_total_amount.customer_id = NEW.customer_id
        ),
        no_of_orders = no_of_orders + 1,
        average_order_value = (total_amount_order/no_of_orders)
    WHERE CA.customer_id = NEW.customer_id;
END $$
DELIMITER ;



DELIMITER $$
CREATE TRIGGER customer_analysis_insertion
AFTER INSERT ON customer
FOR EACH ROW
BEGIN
    INSERT INTO customer_analysis (customer_id)
    VALUES (NEW.customer_id);
END $$
DELIMITER ;



DELIMITER $$
CREATE TRIGGER cart_total_amount_reduce
AFTER DELETE ON cart
FOR EACH ROW
BEGIN
    -- Update total_amount in cart_total_amount table
    UPDATE cart_total_amount CTA
    SET total_amount = (
        SELECT SUM(product_amount)
        FROM cart
        WHERE cart.customer_id = OLD.customer_id
    )
    WHERE CTA.customer_id = OLD.customer_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER check_product_quantity_in_stock
AFTER INSERT
ON cart
FOR EACH ROW
BEGIN
    DECLARE available_quantity INT;

    -- Get the available quantity of the product in stock
    SELECT quantity INTO available_quantity
    FROM product
    WHERE product_id = NEW.product_id;

    -- If the product quantity in stock is less than the quantity added to the cart, rollback the transaction
    IF available_quantity < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product quantity in stock is insufficient';
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER update_stock_quantity
AFTER INSERT ON cart
FOR EACH ROW
BEGIN
    UPDATE product
    SET quantity = quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
END;
$$
DELIMITER ;



DELIMITER $$
CREATE TRIGGER update_CTA_table
AFTER INSERT ON customer
FOR EACH ROW
BEGIN
    INSERT INTO cart_total_amount
    VALUES (NEW.customer_id, 0);
END;
$$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER insert_order_after_payment
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE order_amount DECIMAL(10,2);
    DECLARE free_partner_id INT;

    -- Fetching amount from cart_total_amount table
    SELECT total_amount INTO order_amount
    FROM cart_total_amount
    WHERE customer_id = NEW.customer_id;

    -- Finding a free partner
    SELECT partner_id INTO free_partner_id
    FROM partner
    WHERE status = 0
    LIMIT 1;

    -- If a free partner is found, update their status to busy (1)
    IF free_partner_id IS NOT NULL THEN
        UPDATE partner
        SET status = 1
        WHERE partner_id = free_partner_id;
        
        -- Inserting values into orders table with the allocated partner
        INSERT INTO orders (payment_id,customer_id, order_date, amount, partner_id)
        VALUES (NEW.payment_id,NEW.customer_id, NEW.payment_date, order_amount, free_partner_id);
    ELSE
        -- Inserting values into orders table without partner allocation
        INSERT INTO orders (payment_id,customer_id, order_date, amount)
        VALUES (NEW.payment_id,NEW.customer_id, NEW.payment_date, order_amount);
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER update_partner_status_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE partner
    SET status = 0
    WHERE partner_id = NEW.partner_id;
END $$
DELIMITER ;


DELIMITER $$



-- DROP TRIGGER update_quantity_after_deletion;
-- DROP TRIGGER clear_cart_after_order;


DELIMITER $$

CREATE TRIGGER clear_cart_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Disable the update_quantity_after_deletion trigger temporarily
    SET @disable_trigger = 1;

    DELETE FROM cart WHERE customer_id = NEW.customer_id;
    
    UPDATE cart_total_amount
    SET total_amount = 0
    WHERE customer_id = NEW.customer_id;

    -- Re-enable the update_quantity_after_deletion trigger
    SET @disable_trigger = NULL;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER update_quantity_after_deletion
AFTER DELETE ON cart
FOR EACH ROW
BEGIN
    -- Check if the trigger should be disabled
    IF @disable_trigger IS NULL THEN
        UPDATE product
        SET quantity = quantity + OLD.quantity
        WHERE product_id = OLD.product_id;
    END IF;
END $$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER prevent_double_assignment
BEFORE UPDATE ON partner
FOR EACH ROW
BEGIN
    IF OLD.status = 1 AND NEW.status = 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot assign status 1 to a partner already with status 1';
    END IF;
END$$

DELIMITER ;



