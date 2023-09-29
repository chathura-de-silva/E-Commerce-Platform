#  E-Commerce Platform for 'C'
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

# Implementation Details 
*   This project is using a SQL database to manage data. 
*   Backend is developed using Python with the `Flask` microframework.
*   This Project uses server side rendering to render the user interface.
*   As per the requirements this project doesn't use ORM anywhere and instead, always relies on vanilla SQL queries.
*   `Python version 3.11` or later recommended.
*   This project includes a python automation script which allows you to specify the initial database entirely by modifying some files without needing to write sql quries for everything.

## Getting started
*   As a prerequisite you should have your mysql environment set up  and server running.
  
To get started with the platform, follow these steps : 
1.  Clone this repository.
    ```plaintext
    https://github.com/chathura-de-silva/E-Commerce-Platform
    ```
2.  cd in to the project directory and Install the dependencies using following command.(Activate the Virutal Environment if you are using one. Itis recommended to use one.)
    ```plaintext
    $ pip install -r requirements.txt
    ```
3.  create `.env` file inside the `dbInitialData` directory including following environmental variables.(You are supposed to update variable values according to your sql environment. You can simply copy the text below, modify it and save in the specified path.)
    ```dotenv
    HOST=localhost
    USER=root
    PASSWORD=5059860
    DATABASE=EcomDB
    ```
4.  You can entirely alter the initial database as per your requirements without involving in any coding(sql queries will be required to specify the relations between tables and data types. But it is a simple process of modifying some text files.). For more info refer the later part of this document. 

5.  Run the Project. (app.py)
    *   This will initially create the database as you specified and will populate the data given. If database already exists directly the app will run.
## Additional information

This project was created as part of a 2<sup>nd</sup> year university project under the Database Systems module in the Department of Computer Science and Engineering at the University of Moratuwa.
