/*
Indexing the foriegn keys
*/

ALTER TABLE category
ADD INDEX idx_category_id (category_id);

ALTER TABLE product
ADD INDEX idx_product_id (product_id);

ALTER TABLE variant
ADD INDEX idx_variant_id (variant_id);

ALTER TABLE registered_user
ADD INDEX idx_user_id (user_id);

ALTER TABLE orders
ADD INDEX idx_order_id (order_id);

ALTER TABLE order_item
ADD INDEX idx_order_item_id (order_item_id);

/*
product table keys
*/

ALTER TABLE product
ADD CONSTRAINT pk_product_id
PRIMARY KEY (product_id);

ALTER TABLE product
ADD CONSTRAINT fk_product
FOREIGN KEY (category_id)
REFERENCES category(category_id);

/*
category table keys
*/

ALTER TABLE category
ADD CONSTRAINT pk_category_id
PRIMARY KEY (category_id);

ALTER TABLE category
ADD CONSTRAINT fk_category
FOREIGN KEY (parent_category_id)
REFERENCES category(category_id);

/*
variant table keys
*/

ALTER TABLE variant
ADD CONSTRAINT pk_variant_id
PRIMARY KEY (variant_id);

ALTER TABLE variant
ADD CONSTRAINT fk_variant
FOREIGN KEY (product_id)
REFERENCES product(product_id);

/*
inventory table keys
*/

ALTER TABLE inventory
ADD CONSTRAINT pk_inventory_id
PRIMARY KEY (inventory_id);

ALTER TABLE inventory
ADD CONSTRAINT fk_inventory
FOREIGN KEY (variant_id)
REFERENCES  variant(variant_id);

/*
cart_item table keys
*/

ALTER TABLE cart_item
ADD CONSTRAINT pk_cart_item
PRIMARY KEY (user_ID,variant_id);

ALTER TABLE cart_item
ADD CONSTRAINT fk_cart_item0
FOREIGN KEY (user_ID)
REFERENCES registered_user(user_id);


ALTER TABLE cart_item
ADD CONSTRAINT fk_cart_item1
FOREIGN KEY (variant_id)
REFERENCES  variant(variant_id);

/*
orders table keys
*/

ALTER TABLE orders
ADD CONSTRAINT pk_order_id
PRIMARY KEY (order_id);

ALTER TABLE orders
ADD CONSTRAINT fk_order
FOREIGN KEY (user_ID)
REFERENCES  registered_user(user_ID);

/*
reg user table keys
*/

ALTER TABLE registered_user
ADD CONSTRAINT pk_user_id
PRIMARY KEY (user_id);

/*
order_item table keys
*/

ALTER TABLE order_item
ADD CONSTRAINT pk_order_item_id
PRIMARY KEY (order_item_id);

ALTER TABLE order_item
ADD CONSTRAINT fk_order_item0
FOREIGN KEY (order_id)
REFERENCES  orders(order_id);


ALTER TABLE order_item
ADD CONSTRAINT fk_order_item1
FOREIGN KEY (variant_id)
REFERENCES  variant(variant_id);


/*
delivery table keys
*/

ALTER TABLE delivery_module
ADD CONSTRAINT pk_delivery_module_id
PRIMARY KEY (delivery_module_id);

ALTER TABLE delivery_module
ADD CONSTRAINT fk_delivery_module
FOREIGN KEY (order_item_id)
REFERENCES  order_item(order_item_id);