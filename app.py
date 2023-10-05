from flask import Flask, render_template, request, url_for, redirect, abort, session,flash
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
    if "id" in session:
        return render_template("home.html", signedin=True, id=session['id'])
    return render_template("home.html", signedin=False)

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
            session["userid"] = userdat[0]
            return redirect(url_for('home'))
        return render_template("login.html", err=True)
    return render_template("login.html", err=False)

@app.route("/logout/")
def logout():
    session.pop('userid')
    session.pop('name')
    session.pop('type')
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


# when someone clicked on a tile in the product page this function will be called 
@app.route("/product/<id>/")
def view_product(id):
    # if 'userid' not in session:
    #     return redirect(url_for('home'))
    # type = session["type"]
    tup = get_single_product_info(id)

    return render_template('product_detail.html',product = tup)

@app.route('/search', methods=['GET'])
def search_products():

    search_query = request.args.get('query')

    products = search_product(search_query)

    return render_template('search_results.html', products = products)


@app.route("/buy/", methods=["POST", "GET"])
def buy():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if request.method=="POST":
        data = request.form
        srchBy = data["search method"]
        category = None if srchBy=='by keyword' else data["category"]
        keyword = data["keyword"]
        results = search_products(srchBy, category, keyword)
        return render_template('search_products.html', after_srch=True, results=results)
    return render_template('search_products.html', after_srch=False)


@app.route("/buy/cart/", methods=["POST", "GET"])
def my_cart():

    #user need to be logged in in order to view the cart
    if 'userid' not in session:
        return redirect(url_for('home'))
    # if session['type']=="Seller":
    #     abort(403)
    cart = get_cart(session['userid'])
    if request.method=="POST":
        data = request.form
        qty = {}
        for i in data:
            if i.startswith("qty"):
                qty[i[3:]]=data[i]      #qty[prodID]=quantity
        update_cart(session['userid'], qty)
        return redirect("/buy/cart/confirm/")
    return render_template('my_cart.html', cart=cart)

@app.route("/buy/<id>/", methods=['POST', 'GET'])
def buy_product(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Seller":
        abort(403)
    ispresent, tup = get_product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if request.method=="POST":
        data = request.form
        total = int(data['qty'])*float(sell_price)
        return redirect(url_for('buy_confirm', total=total, quantity=data['qty'], id=id))
    return render_template('buy_product.html', name=name, category=category, desp=desp, quantity=quantity, price=sell_price)


@app.route("/buy/myorders/")
def my_orders():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Seller":
        abort(403)
    res = cust_orders(session['userid'])
    return render_template('my_orders.html', orders=res)


@app.route("/buy/purchases/")
def my_purchases():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Seller":
        abort(403)
    res = cust_purchases(session['userid'])
    return render_template('my_purchases.html', purchases=res)


@app.route("/sell/sales/")
def my_sales():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Customer":
        abort(403)
    res = sell_sales(session['userid'])
    return render_template('my_sales.html', sales=res)


@app.route("/buy/cart/confirm/", methods=["POST", "GET"])
def cart_purchase_confirm():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Seller":
        abort(403)
    if request.method=="POST":
        choice = request.form['choice']
        if choice=="PLACE ORDER":
            cart_purchase(session['userid'])
            return redirect(url_for('my_orders'))
        elif choice=="CANCEL":
            return redirect(url_for('my_cart'))
    cart = get_cart(session['userid'])
    items = [(i[1], i[3], float(i[2])*float(i[3])) for i in cart]
    total = 0
    for i in cart:
        total += float(i[2])*int(i[3])
    return render_template('buy_confirm.html', items=items, total=total)

@app.route("/buy/cart/<prodID>/")
def add_to_cart(prodID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    add_product_to_cart(prodID, session['userid'])
    return redirect(url_for('view_product', id=prodID))

@app.route("/buy/cart/delete/")
def delete_cart():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['userid']=="Seller":
        abort(403)
    empty_cart(session['userid'])
    return redirect(url_for('my_cart'))

@app.route("/buy/cart/delete/<prodID>/")
def delete_prod_cart(prodID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['userid']=="Seller":
        abort(403)
    remove_from_cart(session['userid'], prodID)
    return redirect(url_for('my_cart'))


app.config['SECRET_KEY'] = os.urandom(17)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess.init_app(app)

if __name__ == '__main__':


    app.run(host='0.0.0.0', port=5007, debug=False)
connection_config = database_connector()

