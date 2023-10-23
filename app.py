from flask import Flask, render_template, request, url_for, redirect, abort, session ,flash
from flask_session import Session
from dbaccess import *
from databaseConfig import database_connector
import os


#creating a global cursor
app = Flask(__name__)

sess = Session()

#users should not be logged in in order to use the platform


@app.route("/")
def home():
    #if the user is signed in load as signed in
    # use userid insted of id (a point to consider)

    signedin = False
    username = None
    
    if "userid" in session:
        signedin = True
        username = session.get("username")  # Assuming username is saved in session["username"]

    return render_template("home.html", signedin=signedin, username=username)

@app.route("/signup/", methods = ["POST", "GET"])
def signup():
    #we need to call the add user function here 
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

            #the following userid will be used throught out the full session
            session["userid"] = userdat[0]
            #define the username of the session
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

@app.route('/analytics')

def analytics():

    return render_template('login.html')

# we have to define a function to fetch trype of product separately..
# it would be good if we could make a function which takes product type as an arugment and bla bla 
@app.route('/electronics')
def get_electronics():
    #we need to get all the electrnoics items from our database 
    #for this we are going to get the primary key of the electronics category in the database and fetch all the data which has that value as the parent category id
    category_name = "ELECTRONIC PRODUCTS"  # The category name you want to display
    electronics  = get_categories("Electronics")
    return render_template('main_categories.html',products = electronics,category_name=category_name)


@app.route('/toys')
def get_toys():
    #we need to get all the electrnoics items from our database 
    #for this we are going to get the primary key of the electronics category in the database and fetch all the data which has that value as the parent category id
    category_name = "TOY PRODUCTS"
    toys = get_categories("Toys")
    return render_template('main_categories.html',products = toys,category_name=category_name)



#the following function will be used to get varients from the database
@app.route('/products/<product_id>', methods=['GET'])
def get_products(product_id):

    varients = get_products_from_database(product_id)

    return render_template('product_detail.html',products = varients)
  

# when someone clicked on a tile in the product page this function will be called 
@app.route("/product/<id>/")
def view_product(id):
    # if 'userid' not in session:
    #     return redirect(url_for('home'))
    # type = session["type"]
    tup = get_single_product_info(id)

    print(tup)
    return render_template('product_detail.html',product = tup)


# need to create a function to get varient details from the database
@app.route('/varients/<product_id>', methods=['GET'])
def get_varient(product_id):
    #need to write the business logic here

    tup = get_varient_info(product_id)
    signedin = False
    if "userid" in session:
        signedin = True

    return render_template('variants.html',variants = tup, signedin=signedin)


@app.route('/search', methods=['GET'])
def search_products():

    search_query = request.args.get('query')

    products = search_product(search_query)

    return render_template('search_results.html', products = products)



@app.route("/cart/", methods=["POST", "GET"])
def cart():
    # Check if the user is signed in
    
    signedin =  session['signedin']  
    if signedin is True:
        username = session['username']
        cart = get_cart(session['userid'])
        return render_template('cart.html', cart=cart, signedin=signedin,username = username)
    else:
        signedin = False
        session_cart = session.get('cart', {})
                #get a list of all the varient ID's that are added to the cart
        variant_ids_string = list(session_cart.keys())
        variant_ids = [int(i) for i in variant_ids_string]
                #need to implement the function to fetch values from the database for the given id's
        variant_details = get_guest_cart(variant_ids)
        return render_template('cart.html',guest_cart = variant_details , signedin = False , session_cart=session_cart)
        



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    variant_id = request.form.get('variant_id')
    quantity = int(request.form.get('quantity'))
    try:
        username = session['username']

        if username is not None:
            print('hi')
            # User is logged in, update the database cart
            user_id = session['userid']
            # Update the cart_items table in the database
            # user_id, variant_id, quantity 
            update_cart(user_id,variant_id,quantity)

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

    #get_cart()
    # if the user if not logged in he should be redirected to the login page 
    is_logged = session['signedin']
    if is_logged is True:
        return render_template('checkout.html')
    #also need to find the total price 
    else:
        flash('You are going to checkout as a guest. Some features may not be not available')
        return render_template('checkout.html')


@app.route('/checkout_successful', methods=['POST'])
def checkout_successful():
    if request.method == 'POST':
        # Here, you can process the form data as needed
        # For example, you can access form data using request.form
        full_name = request.form.get('firstname')
        email = request.form.get('email')
        # Process other form data here as necessary

        signedin =  session['signedin'] 
        order_id = gen_orderID()
        order_items = []
        if signedin:
            #get the user's cart
            cart = get_cart(session['userid'])
            #extract the variant ID's from the cart
            for item in cart:
                # ci.quantity AS quantity,
                # v.name AS name,
                # v.price AS price,
                # v.variant_image AS variant_image,
                # p.title AS title,
                # v.variant_id as variant_id
                new_ID = gen_order_item_ID()
                variant_Id = item[5]
                quantity = item[0]
                price = item[2]

                temp = []
                temp.append(new_ID,order_id,variant_Id,quantity,price)
                order_items.append(temp)
        
            print(order_items)

        else:
            #get the session cart
            

        # try to implement and transaction to finish the checkout functionality
        # After processing the form data, you can render a success page
            return render_template('login.html', full_name=full_name, email=email)


app.config['SECRET_KEY'] = os.urandom(17)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess.init_app(app)

if __name__ == '__main__':


    app.run(host='0.0.0.0', port=5007, debug=False)
connection_config = database_connector()

