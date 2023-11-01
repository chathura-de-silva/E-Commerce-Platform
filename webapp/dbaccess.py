import mysql.connector
from .databaseConfig import get_db_config_data
from werkzeug.security import generate_password_hash,check_password_hash

config = get_db_config_data()


def get_mysql_connection():
    return mysql.connector.connect(**config)


# all of the following functions will be used to communicate with the database

# this function is used to generate a unique custom ID
# always remember to insert id's in numerical order
# the following functions will be used to generate uniqe ID's
def gen_custID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM registered_user ORDER BY user_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


# this function generates an order ID
def gen_orderID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id FROM order_item ORDER BY order_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


# this function generates ID for a single order item
def gen_order_item_ID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_item_id FROM order_item ORDER BY order_item_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


# this function generates ID for a delivary module
def gen_delivery_ID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT delivery_module_id FROM delivery_module ORDER BY order_item_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
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


# this function will be used to add a new user to the database
# it will return true if we are able to add a new user
def add_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    username = data["username"]
    # need to check if the username already exists
    cur.execute("SELECT * FROM registered_user WHERE username=%s", (username,))
    result = cur.fetchall()
    # if we already have a registered user from that username then we can't add another user
    if len(result) != 0:
        return False
    customer_id = gen_custID()
    tup = (customer_id, data["email"], generate_password_hash(data["password"], method='pbkdf2:sha256'), data["username"],)

    cur.execute("INSERT INTO registered_user (user_id,email, password, username) VALUES (%s, %s, %s, %s)", tup)

    conn.commit()
    conn.close()
    return True


# this function is used to authenticate the user

def auth_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    # extract the data from the data object
    username = data["username"]
    password = data["password"]

    # check if the user is already in the database
    cur.execute("SELECT user_id,username,password FROM registered_user WHERE username=%s", (username,))
  
    result = cur.fetchall()
    print("hello mofossssssssssssssssssssssssssss",result[0][2])
    conn.close()
    if not check_password_hash(result[0][2],password):
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
    # select all the subproducts related to the given category
    # Execute the SQL query
    query = """
            SELECT Category.category_name, Category.category_image,Category.category_id
            FROM Category
            WHERE Category.parent_category_id = (
                SELECT category_id FROM Category WHERE category_name = %s
            )
        """

    # Fetch the results
    cur.execute(query, (category,))
    results = cur.fetchall()

    return results


# this function will be used to get products from the database
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


def update_cart(user_id, variant_id, quantity):
    conn = get_mysql_connection()
    cur = conn.cursor()
    print("hello world")
    # Define the SQL statement using the INSERT ... ON DUPLICATE KEY UPDATE syntax
    # Define the SQL statement with an alias for VALUES
    query = """
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
        cur.execute(
            "SELECT variant.name,variant.price,variant.custom_attrbutes,variant.variant_image,variant.variant_id FROM variant WHERE product_id = %s",
            (product_id,))
        result = cur.fetchall()

    return result


def update_order_items(order_items, is_signedin, user_id):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    # create a transaction
    # inventry should be updated
    # we should handle this separately for logged in users and guest users

    # for a guest user his session cart should be emptied and for a logged in user his cart_item table should be updated
    # cart table should be inserted with a new entry
    try:
        # Start a transaction
        cursor.execute("START TRANSACTION")

        if is_signedin:
            order_item_id, order_id, variant_id, quantity, price = order_items[0]

            # INSERT INTO order_item
            insert_query = "INSERT INTO order_item (order_item_id, order_id, variant_id, quantity, price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (order_item_id, order_id, variant_id, quantity, price))

            # DELETE FROM cart_item
            delete_query = "DELETE FROM cart_item WHERE user_id = %s"
            cursor.execute(delete_query, (user_id,))

            # Reduce stock count in inventory
            update_query = "UPDATE inventory SET stock_count = stock_count - %s WHERE variant_id = %s"
            cursor.execute(update_query, (quantity, variant_id))

        # Commit the transaction
        cursor.execute("COMMIT")

    except Exception as e:
        # Handle any exceptions and possibly roll back the transaction
        cursor.execute("ROLLBACK")
        raise e
    finally:
        conn.close()


def update_order_table(order_table_details):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        order_id, date, delivery_method, payment_method, user_id = order_table_details

        insert_query = "INSERT INTO orders (order_id, date, delivery_method, payment_method, user_id) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(insert_query, (order_id, date, delivery_method, payment_method, user_id))

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


# this function will fetch variant details for a guest's cart
def get_guest_cart(variant_ids):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # Create a list to store the results
    result = []

    # Construct the SQL query using JOIN to fetch the required columns from both tables
    query = """
    SELECT p.title, v.name, v.price, v.variant_image,v.variant_id
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


def update_delivary_module(module):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # create a list of main cities 
    main_cities = ['Colombo', 'Panadura', 'Galle', 'Kandy']
    new_id = gen_delivery_ID()
    # stock_count,destination_city,new_ID
    tup = new_id, module[2], module[1]

    # checking if the stock count is greater than zero
    if module[0] > 0:

        if (module[1] in main_cities):
            # add fibve days to the end of the tuple

            tup = tup + (5,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)
        else:
            tup = tup + (7,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)

    else:
        if (module[1] in main_cities):
            tup = tup + (8,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)
        else:
            tup = tup + (10,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)

    conn.commit()


def get_details_for_delivery_module(order_item_ids):

    conn = get_mysql_connection()
    cursor = conn.cursor()
    # Create a list to store variant names
    variant_info = []

    try:
        for order_item_id in order_item_ids:
            # SQL query to fetch variant name and estimated days for a specific order item ID
            query = """
            SELECT variant.name, delivery_module.estimated_days
            FROM order_item
            INNER JOIN variant ON order_item.variant_id = variant.variant_id
            LEFT JOIN delivery_module ON order_item.order_item_id = delivery_module.order_item_id
            WHERE order_item.order_item_id = %s
            """
            # Execute the SQL query with the current order_item_id
            cursor.execute(query, (order_item_id,))

            # Fetch the variant name and estimated days and append them to the variant_info list
            result = cursor.fetchone()
            if result:
                variant_info.append(result)

        print(variant_info)
    
    except Exception as e:
        print("Error:", e)

    return variant_info



def remove_from_cart(custID, prodID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE custID=%s AND prodID=%s", (custID, prodID))
    conn.commit()


def Quarterly_sales(year):
    conn = get_mysql_connection()
    cur = conn.cursor()

    cur.execute(f'''CREATE VIEW year{year}orderitem AS
                    select v.price*oi.quantity as total_price , t23.date , oi.order_id, oi.variant_id
                    from order_item as oi
                    join (SELECT * FROM orders WHERE YEAR(date) = {year}) AS t23 on oi.order_id = t23.order_id
                    join variant as v on v.variant_id = oi.variant_id''')
    conn.commit()
    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (1,2,3);''')
    q1 = cur.fetchone()[0]
    q1 = int(q1) if q1 is not None else 0

    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (4,5,6);''')
    q2 = cur.fetchone()[0]
    q2 = int(q2) if q2 is not None else 0

    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (7,8,9);''')
    q3 = cur.fetchone()[0]
    q3 = int(q3) if q3 is not None else 0

    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (10,11,12);''')
    q4 = cur.fetchone()[0]
    q4 = int(q4) if q4 is not None else 0

    cur.execute(f'DROP VIEW IF EXISTS year{year}orderitem;')
    conn.commit()

    q_sale = [q1, q2, q3, q4]
    conn.close()
    return q_sale


def select_year():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute('''select distinct year(date) as year
                    from orders 
                    order by year(date) desc''')
    result = cur.fetchall()
    cur.execute('''select distinct year(date) as year
                    from orders 
                    order by year(date) desc''')
    year = cur.fetchone()[0]
    return (result, year)


def getProductQuantityList(from_year, to_year):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(F'''select LEFT(p.title, 20) as title, sum(oi.quantity) as quantity
                    from order_item oi
                    join orders o 
                    on o.order_id = oi.order_id
                    join variant v
                    on v.variant_id = oi.variant_id
                    join product p
                    on p.product_id = v.product_id
                    where year(date) between {from_year} and {to_year}
                    group by (p.title)''')
    result = cur.fetchall()
    product_list = []
    quantity_list = []
    for i, j in result:
        product_list.append(i)
        quantity_list.append(int(j))
   
    return product_list, quantity_list


def getCategoriesandOrders():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(F'''select c.category_name,count(oi.order_id)
                from order_item as oi
                right join variant as v
                on oi.variant_id = v.variant_id 
                join product as p 
                on p.product_id = v.product_id
                right join category as c
                on c.category_id = p.category_id
                group by c.category_id,c.category_name
                order by count(oi.order_id) asc;
                ; ''')
    result = cur.fetchall()
    category = []
    orders = []
    for i, j in result:
        category.append(i)
        orders.append(j)
    return category, orders


def product_list():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute('''select product_id , title
                    from product ;
                ''')
    result = cur.fetchall()
    return result


def get_product_sales(product_id):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # Parameterized SQL query
    cur.execute('''select count(oi.quantity), month(o.date)
                    from order_item as oi
                    inner join orders as o on o.order_id = oi.order_id
                    right join variant as v on v.variant_id = oi.variant_id
                    join product as p on p.product_id = v.product_id
                    where p.product_id = %s
                    group by month(o.date)
                    order by month(o.date);
                ''', (product_id,))

    result = cur.fetchall()

    # Initialize a dictionary with keys for each month (1-12) and default values of 0
    monthly_values = {month: 0 for month in range(1, 13)}

    # Update the dictionary with the actual sales data from the query
    for value, month in result:
        if month:  # Only update if month is not None
            monthly_values[month] = value

    # Convert the dictionary values to a list
    result_list = list(monthly_values.values())

    return result_list
