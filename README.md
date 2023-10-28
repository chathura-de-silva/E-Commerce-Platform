
# E-Commerce Platform for 'C'
<p align="center">
    <picture>
      <source 
        srcset="./banner.png"
        media="(prefers-color-scheme: dark)"
      />
      <img 
        src="https://github.com/Chathura-De-Silva/E-Commerce-Platform/blob/master/banner.png" 
        alt="Academease Preview"
        width="800"
       />
    </picture>
  </p>



This repository contains the database design and implementation for a single vendor e-commerce platform for C, a local chain retailer in Texas with a simple UI. The platform supports the following features:

* Product management: The platform allows users to create, manage, and track products, including their variants, categories, and inventory.
* Order management: The platform allows users to place orders, track their orders, and manage their payments.
* Reporting: The platform provides a variety of reports to help administrators to track the performance of their e-commerce business.

# Index
1.  [Implementation Details](#implementation-details)
2.  [Getting Started](#getting-started)
3.  [Configuration of Initial Database](#configuration-of-initial-database)
    * [Overview](#overview)
    * [Tables](#tables)
    * [Column Identifiers](#column-identifiers)
    * [Data Entries](#data-entries)
    * [Sample Table in CSV](#sample-table---productcsv)
    * [Table Relations](#table-relations)
    * [Configuration of environmental variables](#configuration-of-env-file)
4.  [Requirments](#requirments)
5.  [User Guide And How To Instructions](#User-Guide-And-How-To-Instructions)
    * [Getting Started](#Getting-Started)
    * [Browsing and Shopping](#Browsing-and-Shopping)
    * [Checkout and Paymen](#Checkout-and-Payment)
    * [Managing Your Account](#Managing-Your-Account)
    * [Analytics](#Analytics)
    * [Contacting Support](#Contacting-Support)

6.  [About](#about)

# Implementation Details 
*   This project is using a SQL database to manage data. 
*   Backend is developed using Python with the `Flask` microframework.
*   This Project uses Server Side Rendering to render the user interface.
*   As per the requirements this project doesn't use an ORM anywhere and instead, always relies on vanilla SQL queries.
*   `Python version 3.11` or later recommended.
*   This project includes a python automation script which allows you to specify the initial database entirely by modifying some files without needing to write sql quries for everything.


## Getting started
*   As prerequisites you should have,
    *    your mysql environment set up  and server running.
    *    Python environment with `Python version 3.11` or higher.

To get started with the platform, follow these steps : 
1.  Clone this repository.
    ```plaintext
    https://github.com/chathura-de-silva/E-Commerce-Platform
    ```
2.  cd in to the project directory and Install the dependencies using following command.(Activate the Virutal Environment if you are using one. It's recommended to use one.)
    ```plaintext
    $ pip install -r requirements.txt
    ```
<a name="env_setup"></a>

3.  create `.env` file inside the `dbInitialData` directory including following environmental variables.(You are supposed to update variable values according to your sql environment. You can simply copy the text below, modify it and save at the specified path as a `.env` file.)
    ```dotenv
    HOST=<hostname (defaults to "localhost")>
    USER=<MySql server username (defaults to "root")>
    PASSWORD=<your password (no defaults. You Must specify)>
    DATABASE=<Database name (deaults to "ecomdb")>
    ```
4.  You can entirely alter the initial database as per your requirements without involving in any coding (sql queries will be required only to specify the relations between tables and data types. Even it is a simple process of modifying some text files.). For more info refer the [later part](#configuration-of-initial-database) of this document.

5.  Run the Project.
    *   `app.py` is the main file.
    *   This will initially create the database as you specified and will populate the data given. Thereafter it will run the app itself. If database already exists directly the app will run without reinitiating the database.
# Configuration of Initial Database

## Overview
Everything you have to modify to create the initial database you wish to have is located inside `/dbInitialData/` directory.

* `database_relations.sql` holds 'ALTER' queries which creates the relations between tables of the database. 
* All the `.csv` files, each represents a table in the initial database.
* `.env` file (should be created by you as mentioned) contains environmental variables related to your MySQL environment.

## Tables
  Every `.csv` file will generate a separate table in the database.
  
  Table name will be the same as the csv file's name.
  * Ex - `product.csv` creates a table in the database called `product`. So you can create or rename the csv files as per your requirement.

  You can either use something like Microsoft Excel or a plain text editor like Notepad for the purpose of creation and editing of CSV files.
  
**Make sure to use double quotes(`"`) as the quotechar and comma(`,`) as the delimiter. Otherwise the project will fail to initiate the database properly.**
* If you are editing csvs' in Excel make sure that the delimiter and quotechar is set as specified. If you are using a text editor, you have to explicitly use the quotechar and delimiter wherever required. Using Excel is the preffered way.

### Column Identifiers
In each coloumn name, only the first word should be the column identifier. There after you have to specify the Data type starting from the next word. 

**Do Not enter anything other than the "\<column_identifier\> \<data type\>".**

### Data Entries
Fill the CSV file with records in the regular way. But data have to be in accordance with the data type of the respective column.
 
### Sample Table - product.csv

#### Table view
| product_id INT | title VARCHAR(255) | description TEXT          | weight DECIMAL(10, 2) | category_id INT | product_image TEXT |
| -------------- | ------------------ | ------------------------- |---------------------- | --------------- | ------------------ |
| 101            | Samsung galaxy S21 | Samsung Galaxy S21, 128GB |0.35                   | 3               | /assets/s21u.jpeg  |
| 202            | Dennim Jeans       | Classic denim jeans       |0.6                    | 6               | /assets/jean.jpeg  | 
#### Text View
```csv
product_id INT,title VARCHAR(255),description TEXT,"weight DECIMAL(10,2)",category_id INT,product_image TEXT
101,Samsung galaxy S21,"Samsung Galaxy S21, 128GB",0.35,3,/assets/s21u.jpeg
202,Dennim Jeans,Classic denim jeans,0.6,6,/assets/jean.jpeg
```

## Table relations
You have to write `ALTER` SQL queries for the referencing inside `dbInitialData/database_relations.sql`.

Keep an empty line between each SQL query. 
You can add comments if you want to. But it is recommended to avoid comments.

Ex -     
  ```sql
    ALTER TABLE product
    ADD CONSTRAINT pk_product_id
    PRIMARY KEY (product_id);

    ALTER TABLE variant
    ADD CONSTRAINT pk_variant_id
    PRIMARY KEY (variant_id);
  ```
## Configuration of `.env` file.
*  Refer the [Getting Started](#getting-started) segment of this document.

## Requirments

#### Python Package Dependencies

These are essential Python libraries and packages that your project relies on to operate successfully. They provide various functionalities and services to help you develop your application. Below is a list of these packages.

- ansi2html
- blinker
- cachelib
- certifi
- charset-normalizer
- click
- colorama
- dash
- dash-core-components
- dash-html-components
- dash-table
- Flask
- Flask-Session
- idna
- importlib-metadata
- itsdangerous
- Jinja2
- MarkupSafe
- mysql-connector-python
- nest-asyncio
- numpy
- packaging
- pandas
- plotly
- protobuf
- python-dateutil
- python-dotenv
- pytz
- requests
- retrying
- six
- tenacity
- typing_extensions
- tzdata
- urllib3
- Werkzeug
- zipp

## User Guide And How To Instructions

### Getting Started

1. *Creating an Account*: To get started with our e-commerce platform, you'll need to create an account. Click on the "Sign Up" button on the homepage, and provide your details, including your name, email address, and a secure password.

2. *Logging In*: If you already have an account, simply click on the "Log In" button on the homepage. Enter your registered email and password to access your account.


<p align="center">
    <picture>
      <source 
        srcset="./banner.png"
        media="(prefers-color-scheme: dark)"
      />
      <img 
        src="https://github.com/Chathura-De-Silva/E-Commerce-Platform/blob/master/banner.png" 
        alt="Academease Preview"
        width="500"
        height="400"
       />
    </picture>
  </p>

### Browsing and Shopping

3. *Exploring Products*: Browse through our wide range of products by clicking on the various categories displayed on the homepage. You can also use the search bar to find specific items.

      
       Ex - Electronic product 

            Toy product

4. *Product Details*: Click on a product to view its details. This includes the product's name, description, price, and any available variants. You can also see images of the product.

5. **Adding to Cart*: When you've found an item you'd like to purchase, click the "Add to Cart" button. You can specify the quantity and select variants, if applicable.

6. *Shopping Cart*: To review your selected items, click on the shopping cart icon at the top of the page. Here, you can make any necessary adjustments to your order.

7. *Proceed to Checkout*: Once you're satisfied with your selections, click "Proceed to Checkout" to complete your purchase.

### Checkout and Payment

8. *Delivery Information*: Provide the necessary delivery information, including your shipping address. If you have an account, this information may already be saved.

9. *Payment*: Select your preferred payment method (e.g., credit card, PayPal). Enter your payment details securely. 

10. *Review Order*: Take a moment to review your order, including the items, shipping address, and payment details. Confirm that everything is correct.

11. *Place Order*: When you're ready, click "Place Order." You'll receive an order confirmation, and we'll start processing your order.

### Managing Your Account

12. *User Dashboard*: As a registered user, you can access your user dashboard. Here, you can view your order history, manage your personal information, and update your password.

13. *Logging Out*: To log out of your account, simply click the "Log Out" button. It's important to log out, especially if you're using a shared computer.

### Analytics


14. *Total Quarterly Sales Over the Years*: This section provides information about our total sales for each quarter over the years. It gives you an overview of our sales performance.

15. *Product Sales Quantities*: Here, you can explore data related to product sales quantities. It helps you understand which products are the most popular among our customers.

16. *Trending Categories*: Discover the product categories that are currently trending on our platform. This data can be helpful for making informed shopping decisions.

17. *Sales Throughout the Year*: Get insights into how our sales perform throughout the year. It can help you plan your shopping based on seasonal trends and discounts.



### Contacting Support

18. *Need Help*: If you encounter any issues or have questions about our products or services, you can reach out to our customer support team. Click on the "Contact Us" link to find our contact details.

19. *Feedback*: We value your feedback! If you have suggestions or comments about your shopping experience, please feel free to share your thoughts with us.

That's it! You're now ready to explore and shop on our e-commerce platform. If you have any further questions or need assistance, don't hesitate to reach out to our friendly customer support team. Happy shopping!

## About

This project was created as part of a 2<sup>nd</sup> year university project under the Database Systems module in the Department of Computer Science and Engineering at the University of Moratuwa. Any contributions are welcome!

[Go to the Top](#e-commerce-platform-for-c)