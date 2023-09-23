import mysql.connector
import databaseConfig

#tried using the global connection object but it failed

# connection = databaseConfig.database_connector()
# # Create a function to establish a MySQL database connection
# def get_mysql_connection():

#     return connection

#creating another function to create the connection with the database everytime we want to communicate with it
def get_mysql_connection():
    config = {
        'user': 'root',
        'password': 'SaviYa1000!!',
        'host': 'localhost',
        'database': 'loginapp',
    }

    return mysql.connector.connect(**config)


#all of the following functions will be used to communicate with the database

#this function is used to generate a unique custom ID
#always remember to insert id's in numerical order
#the following functions will be used to generate uniqe ID's
def gen_custID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM accounts ORDER BY id DESC LIMIT 1")
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

def gen_prodID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET prodnum = prodnum + 1")
    conn.commit()
    cur.execute("SELECT prodnum FROM metadata")
    prodnum = str(cur.fetchone()[0])
    conn.close()
    id = "PID" + "0" * (7 - len(prodnum)) + prodnum
    return id

def gen_orderID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET ordernum = ordernum + 1")
    conn.commit()
    cur.execute("SELECT ordernum FROM metadata")
    ordernum = str(cur.fetchone()[0])
    conn.close()
    id = "OID" + "0" * (7 - len(ordernum)) + ordernum
    return id


#this function will be used to add a new user to the database
def add_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    username = data["username"]
    #need to check if the username already exists
    cur.execute("SELECT * FROM accounts WHERE username=%s", (username,))
    result = cur.fetchall()
    if len(result) != 0:
        return False
    customer_id = gen_custID()
    tup = (customer_id,data["username"], data["email"], data["password"])
    
    cur.execute("INSERT INTO accounts (id, username, email, password) VALUES (%s, %s, %s, %s)", tup)
    
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
    cur.execute("SELECT id FROM accounts WHERE password=%s AND username=%s", (password,username))

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
            SELECT Category.name, Category.category_image
            FROM Category
            WHERE Category.parent_category_id = (
                SELECT category_id FROM Category WHERE name = %s
            )
        """
    
        #Fetch the results
    cur.execute(query, (category,))
    results = cur.fetchall()

    return results



def get_product_info():
    conn = get_mysql_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    return products

# def get_single_product_info(product_id):

#     conn = get_mysql_connection()
#     cur = conn.cursor()
#     #run the query to get all the details based on the user ID
#     cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
#     details = cur.fetchall()
#     return details 

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


def search_products(srchBy, category, keyword):
    conn = get_mysql_connection()
    cur = conn.cursor()
    keyword = ['%' + i + '%' for i in keyword.split()]
    if len(keyword) == 0:
        keyword.append('%%')
    if srchBy == "by category":
        cur.execute("SELECT prodID, name, category, sell_price FROM product WHERE category=%s AND quantity!=0", (category,))
        result = cur.fetchall()
    elif srchBy == "by keyword":
        result = []
        for word in keyword:
            cur.execute("SELECT prodID, name, category, sell_price FROM product WHERE (name LIKE %s OR description LIKE %s OR category LIKE %s) AND quantity!=0", (word, word, word))
            result += cur.fetchall()
        result = list(set(result))
    elif srchBy == "both":
        result = []
        for word in keyword:
            cur.execute("SELECT prodID, name, category, sell_price FROM product WHERE (name LIKE %s OR description LIKE %s) AND quantity!=0 AND category=%s", (word, word, category))
            result += cur.fetchall()
        result = list(set(result))
    conn.close()
    return result



def place_order(prodID, custID, qty):
    conn = get_mysql_connection()
    cur = conn.cursor()
    orderID = gen_orderID()
    cur.execute("INSERT INTO orders (orderID, custID, prodID, quantity, date, cost_price, sell_price, status) SELECT %s, %s, %s, %s, NOW(), cost_price*%s, sell_price*%s, 'PLACED' FROM product WHERE prodID=%s", (orderID, custID, prodID, qty, qty, qty, prodID))
    conn.commit()
    conn.close()

def cust_orders(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT o.orderID, o.prodID, p.name, o.quantity, o.sell_price, o.date, o.status FROM orders o JOIN product p WHERE o.prodID=p.prodID AND o.custID=%s AND o.status!='RECEIVED' ORDER BY o.date DESC", (custID,))
    result = cur.fetchall()
    conn.close()
    return result


def get_order_details(orderID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT o.custID, p.sellID, o.status FROM orders o JOIN product p WHERE o.orderID=%s AND o.prodID=p.prodID", (orderID,))
    result = cur.fetchall()
    conn.close()
    return result

def change_order_status(orderID, new_status):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=%s WHERE orderID=%s", (new_status, orderID))
    if new_status == 'DISPATCHED':
        cur.execute("UPDATE product SET quantity=quantity-(SELECT quantity FROM orders WHERE orderID=%s) WHERE prodID=(SELECT prodID FROM orders WHERE orderID=%s)", (orderID, orderID))
    conn.commit()
    conn.close()

def cust_purchases(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT o.prodID, p.name, o.quantity, o.sell_price, o.date FROM orders o JOIN product p WHERE o.prodID=p.prodID AND o.custID=%s AND o.status='RECEIVED' ORDER BY o.date DESC", (custID,))
    result = cur.fetchall()
    conn.close()
    return result

def sell_sales(sellID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT o.prodID, p.name, o.quantity, o.sell_price, o.date, o.custID, c.name FROM orders o JOIN product p JOIN customer c WHERE o.prodID=p.prodID AND o.custID=c.custID AND p.sellID=%s AND o.status='RECEIVED' ORDER BY o.date DESC", (sellID,))
    result = cur.fetchall()
    conn.close()
    return result

def add_product_to_cart(prodID, custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO cart VALUES (%s, %s, 1)", (custID, prodID))
    conn.commit()
    conn.close()

def get_cart(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT p.prodID, p.name, p.sell_price, c.sum_qty, p.quantity FROM (SELECT custID, prodID, SUM(quantity) AS sum_qty FROM cart GROUP BY custID, prodID) c JOIN product p WHERE p.prodID=c.prodID AND c.custID=%s", (custID,))
    result = cur.fetchall()
    conn.close()
    return result

def update_cart(custID, qty):
    conn = get_mysql_connection()
    cur = conn.cursor()
    for prodID in qty:
        cur.execute("DELETE FROM cart WHERE prodID=%s AND custID=%s", (prodID, custID))
        cur.execute("INSERT INTO cart VALUES (%s, %s, %s)", (custID, prodID, qty[prodID]))
    conn.commit()
    conn.close()

def cart_purchase(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cart = get_cart(custID)
    for item in cart:
        orderID = gen_orderID()
        prodID = item[0]
        qty = item[3]
        cur.execute("INSERT INTO orders (orderID, custID, prodID, quantity, date, cost_price, sell_price, status) SELECT %s, %s, %s, %s, NOW(), cost_price*%s, sell_price*%s, 'PLACED' FROM product WHERE prodID=%s", (orderID, custID, prodID, qty, qty, qty, prodID))
        cur.execute("DELETE FROM cart WHERE custID=%s AND prodID=%s", (custID, prodID))
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
