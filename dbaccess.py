import mysql.connector
from app import connection_config
#tried using the global connection object but it failed

# connection = databaseConfig.database_connector()
# # Create a function to establish a MySQL database connection
# def get_mysql_connection():

#     return connection

#creating another function to create the connection with the database everytime we want to communicate with it
def get_mysql_connection():
    config =  connection_config
    return mysql.connector.connect(**config)


#all of the following functions will be used to communicate with the database

#this function is used to generate a unique custom ID
#always remember to insert id's in numerical order
#the following functions will be used to generate uniqe ID's
def gen_custID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM registered_user ORDER BY user_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    #return the number which is 1 greater than the last entry 
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0

#this function generates an order ID
def gen_orderID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id FROM order_item ORDER BY order_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    #return the number which is 1 greater than the last entry 
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0
    
#this function generates ID for a single order item
def gen_order_item_ID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_item_id FROM order_item ORDER BY order_item_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    #return the number which is 1 greater than the last entry 
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0

def get_stock_count(variant_id):
    conn = get_mysql_connection()
    cur = conn.cursor()
    # Define the query with a placeholder for variant_id
    query = "SELECT stock_count FROM inventory WHERE variant_id = %s"

    # Execute the query with the provided variant_id
    cur.execute(query, (variant_id,))

    # Fetch the result
    result = cur.fetchone()

    print(result)

    if result:
        stock_count = result[0]
        return stock_count
    else:
        return None




#this function will be used to add a new user to the database
#it will return true if we are able to add a new user 
def add_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    username = data["username"]
    #need to check if the username already exists
    cur.execute("SELECT * FROM registered_user WHERE username=%s", (username,))
    result = cur.fetchall()
    #if we already have a registered user from that username then we can't add another user
    if len(result) != 0:
        return False
    customer_id = gen_custID()
    tup = (customer_id,data["email"], data["password"],data["username"],)
    
    cur.execute("INSERT INTO registered_user (user_id,email, password, username) VALUES (%s, %s, %s, %s)", tup)
    
    conn.commit()
    conn.close()
    return True

#this function is used to authenticate the user

def auth_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    #extract the data from the data object
    username = data["username"]
    password = data["password"]

    #check if the user is already in the database
    cur.execute("SELECT user_id,username FROM registered_user WHERE password=%s AND username=%s", (password,username))

    result = cur.fetchall()
    conn.close()
    if len(result) == 0:
        return False
    return result[0]


def search_product(search_query):
    conn = get_mysql_connection()
    cur = conn.cursor()

    sql_query = "SELECT * FROM product WHERE name LIKE %s"
    cur.execute(sql_query, ("%" + search_query + "%",))

    # Fetch the matching products
    matching_products = cur.fetchall()

    return matching_products


# we can use the below function to get all the main products related to a given category
# ex :- when we pass electronics as the parameter to this function we are fetching all the electronics sub products from the database 
def get_categories(category):

    conn = get_mysql_connection()
    cur = conn.cursor()
    #select all the subproducts related to the given category
        # Execute the SQL query
    query = """
            SELECT Category.category_name, Category.category_image,Category.category_id
            FROM Category
            WHERE Category.parent_category_id = (
                SELECT category_id FROM Category WHERE category_name = %s
            )
        """
    
        #Fetch the results
    cur.execute(query, (category,))
    results = cur.fetchall()

    return results

#this function will be used to get products from the database
def get_products_from_database(id):
    # use try catch statements to handle errors
    conn = get_mysql_connection()
    cur = conn.cursor()
    # query = "SELECT * FROM products WHERE category_id = %s", (id,)
    # cur.execute(query, (id,))

    query = "SELECT product.title,product.description,product.weight,product.product_image,product.product_id FROM product WHERE category_id = %s"
    cur.execute(query, (id,))  # Pass the integer id as a parameter

    results = cur.fetchall()
    return results
    


def get_product_info():
    conn = get_mysql_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    return products



def update_cart(user_id,variant_id,quantity):

    conn = get_mysql_connection()
    cur = conn.cursor()
    print("hello world")
    # Define the SQL statement using the INSERT ... ON DUPLICATE KEY UPDATE syntax
    # Define the SQL statement with an alias for VALUES
    query ="""
        INSERT INTO cart_item (user_id, variant_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = cart_item.quantity
        """
    # Execute the SQL statement with the provided user_id, variant_id, and quantity
    cur.execute(query, (user_id, variant_id, quantity))

    conn.commit()
    conn.close()
    return


def get_single_product_info(product_id):
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cur:
            # Run the query to get product details based on the product_id
            cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
            details = cur.fetchone()  # Use fetchone since we expect a single result
        return details
    except Exception as e:
        # Handle the exception (e.g., log the error or return an error message)
        return None  # Return None or an appropriate error indicator

def get_varient_info(product_id):

    conn = get_mysql_connection()
    with conn.cursor() as cur:
        
        cur.execute("SELECT variant.name,variant.price,variant.custom_attrbutes,variant.variant_image,variant.variant_id FROM variant WHERE product_id = %s", (product_id,))
        result =cur.fetchall()

    return result


def update_order_items(order_items):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        order_item_id, order_id, variant_id, quantity, price = order_items[0]
        # Assuming you have a table named 'order_item'
        insert_query = "INSERT INTO order_item (order_item_id, order_id, variant_id, quantity, price) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (order_item_id, order_id, variant_id, quantity, price))
    
        conn.commit()  # Commit the changes to the database
    except mysql.connector.Error as err:
        # Handle any potential errors here
        print("Error: {}".format(err))
    finally:
        cursor.close()
        conn.close()


def update_order_table(order_table_details):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        order_id, date, delivery_method, payment_method, user_id = order_table_details

        insert_query = "INSERT INTO orders (order_id, date, delivery_method, payment_method, user_id) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(insert_query, (order_id, date, delivery_method, payment_method, user_id) )

        conn.commit()

    except mysql.connector.Error as err:
        # Handle any potential errors here
        print("Error: {}".format(err))

def get_cart(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()

    sql_query = """
    SELECT
        ci.quantity AS quantity,
        v.name AS name,
        v.price AS price,
        v.variant_image AS variant_image,
        p.title AS title,
        v.variant_id as variant_id
    FROM
        cart_item AS ci
    JOIN
        variant AS v ON ci.variant_id = v.variant_id
    JOIN
        product AS p ON v.product_id = p.product_id
    WHERE
        ci.user_id = %s
    """
    cur.execute(sql_query, (custID,))
    result = cur.fetchall()
    conn.close()
    print(result)

    return result

#this function will fetch variant details for a guest's cart
def get_guest_cart(variant_ids):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # Create a list to store the results
    result = []

    # Construct the SQL query using JOIN to fetch the required columns from both tables
    query = """
    SELECT p.title, v.name, v.price, v.variant_image
    FROM product AS p
    JOIN variant AS v ON p.product_id = v.product_id
    WHERE 
        v.variant_id = %s
    """

    for variant_id in variant_ids:
        # Execute the query for each variant_id
        cur.execute(query, (variant_id,))
        rows = cur.fetchall()
        for row in rows:
            result.append(row)

    return result


def add_product_to_cart(prodID, custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO cart VALUES (%s, %s, 1)", (custID, prodID))
    conn.commit()
    conn.close()




def empty_cart(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE custID=%s", (custID,))
    conn.commit()

def remove_from_cart(custID, prodID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE custID=%s AND prodID=%s", (custID, prodID))
    conn.commit()
