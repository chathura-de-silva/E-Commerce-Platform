ALTER TABLE product
ADD CONSTRAINT pk_product_id
PRIMARY KEY (product_id);

ALTER TABLE variant
ADD CONSTRAINT pk_variant_id
PRIMARY KEY (variant_id);