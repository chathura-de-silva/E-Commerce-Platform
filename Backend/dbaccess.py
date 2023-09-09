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

def gen_custID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET custnum = custnum + 1")
    conn.commit()
    cur.execute("SELECT custnum FROM metadata")
    custnum = str(cur.fetchone()[0])
    conn.close()
    id = "CID" + "0" * (7 - len(custnum)) + custnum
    return id


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
    email = data["email"]
    if data['type'] == "Customer":
        cur.execute("SELECT * FROM customer WHERE email=%s", (email,))
    elif data['type'] == "Seller":
        cur.execute("SELECT * FROM seller WHERE email=%s", (email,))
    result = cur.fetchall()
    if len(result) != 0:
        return False
    tup = (data["name"], data["email"], data["phone"], data["area"], data["locality"], data["city"],
           data["state"], data["country"], data["zip"], data["password"])
    if data['type'] == "Customer":
        cur.execute("INSERT INTO customer (custID, name, email, phone, area, locality, city, state, country, zipcode, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (gen_custID(), *tup))
    elif data['type'] == "Seller":
        cur.execute("INSERT INTO seller (sellID, name, email, phone, area, locality, city, state, country, zipcode, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (gen_sellID(), *tup))
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

def fetch_details(userid, type):
    conn = get_mysql_connection()
    cur = conn.cursor()
    if type == "Customer":
        cur.execute("SELECT * FROM customer WHERE custID=%s", (userid,))
        result_a = cur.fetchall()
        b = []
    elif type == "Seller":
        cur.execute("SELECT * FROM seller WHERE sellID=%s", (userid,))
        result_a = cur.fetchall()
        cur.execute("SELECT DISTINCT(category) from product WHERE sellID=%s", (userid,))
        result_b = cur.fetchall()
        b = [i[0] for i in result_b]
    conn.close()
    return result_a, b

def search_users(search, srch_type):
    conn = get_mysql_connection()
    cur = conn.cursor()
    search = "%" + search + "%"
    if srch_type == "Customer":
        cur.execute("SELECT custID, name, email, phone, area, locality, city, state, country, zipcode FROM customer WHERE LOWER(name) like %s", (search.lower(),))
    elif srch_type == "Seller":
        cur.execute("SELECT sellID, name, email, phone, area, locality, city, state, country, zipcode FROM seller WHERE LOWER(name) like %s", (search.lower(),))
    result = cur.fetchall()
    conn.close()
    return result

def update_details(data, userid, type):
    conn = get_mysql_connection()
    cur = conn.cursor()
    if type == "Customer":
        cur.execute("UPDATE customer SET phone=%s, area=%s, locality=%s, city=%s, state=%s, country=%s, zipcode=%s where custID=%s", (data["phone"], data["area"], data["locality"], data["city"], data["state"], data["country"], data["zip"], userid))
    elif type == "Seller":
        cur.execute("UPDATE seller SET phone=%s, area=%s, locality=%s, city=%s, state=%s, country=%s, zipcode=%s where sellID=%s", (data["phone"], data["area"], data["locality"], data["city"], data["state"], data["country"], data["zip"], userid))
    conn.commit()
    conn.close()

def check_psswd(psswd, userid, type):
    conn = get_mysql_connection()
    cur = conn.cursor()
    if type == "Customer":
        cur.execute("SELECT password FROM customer WHERE custID=%s", (userid,))
    elif type == "Seller":
        cur.execute("SELECT password FROM seller WHERE sellID=%s", (userid,))
    real_psswd = cur.fetchone()[0]
    conn.close()
    return psswd == real_psswd

def set_psswd(psswd, userid, type):
    conn = get_mysql_connection()
    cur = conn.cursor()
    if type == "Customer":
        cur.execute("UPDATE customer SET password=%s WHERE custID=%s", (psswd, userid))
    elif type == "Seller":
        cur.execute("UPDATE seller SET password=%s WHERE sellID=%s", (psswd, userid))
    conn.commit()
    conn.close()

def add_prod(sellID, data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    prodID = gen_prodID()
    tup = (prodID, data["name"], data["qty"], data["category"], data["price"], data["price"], data["desp"], sellID)
    cur.execute("INSERT INTO product (prodID, name, quantity, category, cost_price, sell_price, description, sellID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", tup)
    conn.commit()
    conn.close()

def get_categories(sellID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(category) from product where sellID=%s", (sellID,))
    categories = [i[0] for i in cur.fetchall()]
    conn.close()
    return categories

def search_myproduct(sellID, srchBy, category, keyword):
    conn = get_mysql_connection()
    cur = conn.cursor()
    keyword = ['%' + i + '%' for i in keyword.split()]
    if len(keyword) == 0:
        keyword.append('%%')
    if srchBy == "by category":
        cur.execute("SELECT prodID, name, quantity, category, cost_price FROM product WHERE category=%s AND sellID=%s", (category, sellID))
        result = cur.fetchall()
    elif srchBy == "by keyword":
        result = []
        for word in keyword:
            cur.execute("SELECT prodID, name, quantity, category, cost_price FROM product WHERE (name LIKE %s OR description LIKE %s OR category LIKE %s) AND sellID=%s", (word, word, word, sellID))
            result += cur.fetchall()
        result = list(set(result))
    elif srchBy == "both":
        result = []
        for word in keyword:
            cur.execute("SELECT prodID, name, quantity, category, cost_price FROM product WHERE (name LIKE %s OR description LIKE %s) AND sellID=%s AND category=%s", (word, word, sellID, category))
            result += cur.fetchall()
        result = list(set(result))
    conn.close()
    return result

def get_product_info(id):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT p.name, p.quantity, p.category, p.cost_price, p.sell_price, p.sellID, p.description, s.name FROM product p JOIN seller s WHERE p.sellID=s.sellID AND p.prodID=%s", (id,))
    result = cur.fetchall()
    conn.close()
    if len(result) == 0:
        return False, result
    return True, result[0]

def update_product(data, id):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("UPDATE product SET name=%s, quantity=%s, category=%s, cost_price=%s, sell_price=(SELECT profit_rate from metadata)*%s, description=%s where prodID=%s", (data['name'], data['qty'], data['category'], data['price'], data['price'], data['desp'], id))
    conn.commit()
    conn.close()

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

def get_seller_products(sellID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT prodID, name, category, sell_price FROM product WHERE sellID=%s AND quantity!=0", (sellID,))
    result = cur.fetchall()
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

def sell_orders(sellID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT o.orderID, o.prodID, p.name, o.quantity, p.quantity, o.cost_price, o.date, o.status FROM orders o JOIN product p WHERE o.prodID=p.prodID AND p.sellID=%s AND o.status!='RECEIVED' ORDER BY o.date DESC", (sellID,))
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
