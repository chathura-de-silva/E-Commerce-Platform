from .databaseConfig import database_connector

database_connector()

from datetime import date
from flask import Flask, render_template, request, url_for, redirect, session, flash ,jsonify
from flask_session import Session
from .dbaccess import *
import os
from .dashapp import create_dash_application
from .dash_PvsQ import dash_productVStime
from .dash_CtvsOr import categories_Orders
from .dash_SalesvsMonth import sales_for_product

# creating a global cursor
app = Flask(__name__)
create_dash_application(app)
dash_productVStime(app)
categories_Orders(app)
sales_for_product(app)
sess = Session()


@app.context_processor
def inject_login_status():
    # Makes signedin/username available to every template's nav bar,
    # without every single route having to remember to pass them.
    return dict(signedin=session.get('signedin', False), username=session.get('username'))


# users should not be logged in in order to use the platform


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup/", methods=["POST", "GET"])
def signup():
    # we need to call the add user function here
    if request.method == "POST":
        data = request.form
        ok = add_user(data)
        if ok:
            session["user_authenticated"] = True
            return render_template("home.html")
        else:
            flash("Username already taken. Please choose another username.", "error")
        return render_template("signup.html", ok=ok)
    return render_template("signup.html", ok=True)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        userdat = auth_user(data)
        if userdat:
            session["user_authenticated"] = True

            # the following userid will be used throught out the full session
            session["userid"] = userdat[0]
            # define the username of the session
            session["username"] = userdat[1]

            session['signedin'] = True

            return redirect(url_for('home'))
        return render_template("login.html", err=True)
    return render_template("login.html", err=False)


@app.route("/logout/")
def logout():
    # Check if 'userid' and 'username' keys exist in the session
    if 'userid' in session:
        session.pop('userid')
    if 'username' in session:
        session.pop('username')  # Use 'username' instead of 'name'
    session['signedin'] = False
    # Redirect to the home route (assuming 'home' is the name of the route)
    return redirect(url_for('home'))


@app.route('/products')
def products():
    # Your products page logic
    #     Call the get_product_info function to fetch a product
    product = get_product_info()  # Replace 'your_product_id' with the actual product ID you want to fetch

    # Check if the product exists
    if product:
        # If the product exists, render the 'products.html' template with the product data
        return render_template('products.html', product=product)

    return render_template('products.html')


# we have to define a function to fetch trype of product separately..
# it would be good if we could make a function which takes product type as an arugment and bla bla 
@app.route('/electronics')
def get_electronics():
    # we need to get all the electrnoics items from our database
    # for this we are going to get the primary key of the electronics category in the database and fetch all the data which has that value as the parent category id
    category_name = "ELECTRONIC PRODUCTS"  # The category name you want to display
    electronics = get_categories("Electronics")
    return render_template('main_categories.html', products=electronics, category_name=category_name)


@app.route('/toys')
def get_toys():
    # we need to get all the electrnoics items from our database
    # for this we are going to get the primary key of the electronics category in the database and fetch all the data which has that value as the parent category id
    category_name = "TOY PRODUCTS"
    toys = get_categories("Toys")
    return render_template('main_categories.html', products=toys, category_name=category_name)


# the following function will be used to get varients from the database
@app.route('/products/<product_id>', methods=['GET'])
def get_products(product_id):
    varients = get_products_from_database(product_id)

    return render_template('product_detail.html', products=varients)


# when someone clicked on a tile in the product page this function will be called 
@app.route("/product/<id>/")
def view_product(id):
    # if 'userid' not in session:
    #     return redirect(url_for('home'))
    # type = session["type"]
    tup = get_single_product_info(id)

    print(tup)
    return render_template('product_detail.html', product=tup)


# need to create a function to get varient details from the database
@app.route('/varients/<product_id>', methods=['GET'])
def get_varient(product_id):
    # variant.name, variant.price, variant.custom_attrbutes, variant.variant_image,
    # variant.variant_id, variant's own stock_count
    tup = get_varient_info(product_id)

    return render_template('variants.html', variants=tup)


@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('query')

    products = search_product(search_query)

    return render_template('search_results.html', products=products)


@app.route("/cart/", methods=["POST", "GET"])
def cart():
    # Check if the user is signed in

    signedin = session.get('signedin', False)
    if signedin is True:
        username = session['username']
        cart = get_cart(session['userid'])
        return render_template('cart.html', cart=cart, signedin=signedin, username=username)
    else:
        signedin = False
        session_cart = session.get('cart', {})
        # get a list of all the varient ID's that are added to the cart
        variant_ids_string = list(session_cart.keys())
        variant_ids = [int(i) for i in variant_ids_string]
        # need to implement the function to fetch values from the database for the given id's
        variant_details = get_guest_cart(variant_ids)

        return render_template('cart.html', guest_cart=variant_details, signedin=False, session_cart=session_cart)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    variant_id = request.form.get('variant_id')
    quantity = int(request.form.get('quantity'))

    available_stock = get_stock_count(variant_id)
    if available_stock is not None and quantity > available_stock:
        flash(f'Only {available_stock} left in stock.', 'error')
        return redirect(url_for('cart'))

    try:
        username = session['username']

        if username is not None:
            print('hi')
            # User is logged in, update the database cart
            user_id = session['userid']
            # Update the cart_items table in the database
            # user_id, variant_id, quantity 
            update_cart(user_id, variant_id, quantity)

            return redirect(url_for('cart'))
    except KeyError:
        # User is not logged in, update the session cart
        if 'cart' not in session:
            session['cart'] = {}
        cart = session['cart']
        if variant_id in cart:
            cart[variant_id] += quantity
        else:
            cart[variant_id] = quantity
        session.modified = True  # Mark the session as modified

        return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    # need to show an estimated delivary time , total prices should be fetched from the cart
    # get_cart()

    is_logged = session.get('signedin', False)

    if is_logged is True:
        user_id = session['userid']
        # ci.quantity AS quantity,
        # v.name AS name,
        # v.price AS price,
        # v.variant_image AS variant_image,
        # p.title AS title,
        # v.variant_id as variant_id
        items = get_cart(user_id)
        # manipulating the tuple to meet our requirements 

        total_price = sum([(tup[0] * tup[2]) for tup in items])

        print(total_price)

        return render_template('checkout.html', total_price=total_price)
    else:
        session_cart = session.get('cart', {})
        variant_ids = [int(i) for i in session_cart.keys()]
        guest_items = get_guest_cart(variant_ids)
        # p.title, v.name, v.price, v.variant_image, v.variant_id
        total_price = sum(session_cart[str(item[4])] * item[2] for item in guest_items)

        flash('You are going to checkout as a guest. Some features may not be not available')
        return render_template('checkout.html', total_price=total_price)


@app.route('/checkout_successful', methods=['POST'])
def checkout_successful():
    if request.method == 'POST':
        city = request.form.get('city')  # Assuming 'city' is the name attribute of the city input field

        signedin = session.get('signedin', False)
        order_id = gen_orderID()

        # Get the current date
        current_date = date.today()
        # Format the current date as a string in 'YYYY-MM-DD' format
        formatted_date = current_date.strftime('%Y-%m-%d')

        # order_id, date, delivery_method, payment_method, user_id

        try:
            if signedin:

                user_id = session['userid']

                order_table_details = [order_id, formatted_date, 'Express', 'visa', user_id]
                update_order_table(order_table_details)

                # get the user's cart
                cart = get_cart(session['userid'])
                # extract the variant ID's from the cart
                order_item_ids = []
                for item in cart:
                    new_ID = gen_order_item_ID()
                    order_item_ids.append(new_ID)

                    variant_Id = item[5]
                    quantity = item[0]
                    price = item[2]

                    temp = []
                    temp.append((new_ID, order_id, variant_Id, quantity, price))

                    # update the delivary module
                    stock_count = get_stock_count(variant_Id)
                    destination_city = city
                    delivary_module = [stock_count, destination_city, new_ID]

                    # need to update the order item table from the above details
                    update_order_items(temp, signedin, user_id=user_id)

                    update_delivary_module(delivary_module)

                names = get_details_for_delivery_module(order_item_ids)

                return (render_template('checkout_succesful.html', names = names))

            else:
                # get the session cart
                # when updating the order tables we need a user_id and we don't have a user ID for a guest user

                # I AM GOING TO HARDCODE USERID *00000* FOR A GUEST USER
                user_id = 0
                order_table_details = [order_id, formatted_date, 'Express', 'visa', user_id]
                update_order_table(order_table_details)

                # p.title, v.name, v.price, v.variant_image,v.variant_id
                session_cart = session.get('cart', {})
                # get a list of all the varient ID's that are added to the cart
                variant_ids_string = list(session_cart.keys())
                variant_ids = [int(i) for i in variant_ids_string]
                # need to implement the function to fetch values from the database for the given id's
                guest_cart = get_guest_cart(variant_ids)

                order_item_ids = [] # we are using this for the delivery module
                for item in guest_cart:
                    new_ID = gen_order_item_ID()
                    order_item_ids.append(new_ID)

                    variant_Id = item[4]
                    # quantity is in the hashmap of the session cart
                    quantity = session_cart[str(variant_Id)]
                    price = item[2]

                    temp = []
                    temp.append((new_ID, order_id, variant_Id, quantity, price))

                    # update the delivary module
                    stock_count = get_stock_count(variant_Id)
                    destination_city = city
                    delivary_module = [stock_count, destination_city, new_ID]

                    update_order_items(temp, signedin, user_id=user_id)

                    update_delivary_module(delivary_module)

                names = get_details_for_delivery_module(order_item_ids)

                # clear the session cart
                session['cart'] = {}
                session.modified = True

                return (render_template('checkout_succesful.html', names = names))

        except InsufficientStockError as e:
            flash(f'Sorry, only {e.available} left in stock for one of the items in your cart. '
                  f'Please update the quantity and try again.', 'error')
            return redirect(url_for('checkout'))
        except Exception as e:
            print(f"Checkout failed: {e}")
            flash('Something went wrong while placing your order. Please try again.', 'error')
            return redirect(url_for('checkout'))


@app.route('/analytics')
def analytics():
    return render_template('analytics3.html')


app.config['SECRET_KEY'] = os.urandom(17)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess.init_app(app)
