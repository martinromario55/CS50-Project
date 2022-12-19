# CS50 My Shop
> This is my CS50 final project
> This is an ecommerce website where customers can create an account, then login and buy products on the website. The site contains different features like the categories feature where by a customer can sort out products according to their category. There is also a brand feature where a customer can sort products using their brand. The search input field on the navbar can be used to search for a product or related product description.

## Technologies
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)

## How the webpage works
When you visit the home page, you can see the products and also navigate around the categories and brands section. You can also see the products description. However, you cannot add products to the cart. Here you need to login or register first.

To register, you need to fill in some information like:
- First name
- Last name
- Username
- Email
- Password
- City
- Country
- Phone Number
- Address
- Photo
All these fields are required except the photo field which comes with a default value

Once you're registered, you can login using your:
- Email Address
- Password

Once you're logged in, then you can add products to cart.
The cart field will increment whenever you add more products.
You can visit the cart page by clicking on the cart element.

### Routing

You can navigate around most routes without logging into the site. However, you cannot add content to cart or view orders, without authentication. Each route checks if the user is authenticated using the `current_user.is_authenticated` property of Flask-Login. It means if correct mail and password were supplied and what role it has.

### Sessions

The webpage uses sessions to confirm that user is registered. Once the user logins, his credentials are checked with bcrypt and his email checked in the database. Once everything passes a session is created (serialized and deserialized) and stored in the cookies. The server attaches user to subsequent requests, so the back-end can easily access the details.

### Database

Database stores all users,products, orders, brands and categories. Tables, like `customer_orders` use foreign keys to relate customers to their orders. Moreover.

### Administration
You can visit the `/admin` route to access the administration section. You may need to login first if you have an account or register using the `/register` route.
Once you login, you will see all the available products in the database.
- You can add, delete, and update products in this section.
- You can edit the price, name, images, description, discount, etc., of the products
- You can also add more brands and categories by clicking on the services section on the nav-bar
- The products you add in this section are the products that the customer will view and buy.


## Possible improvements

As all applications this one can also be improved. Possible improvements:
- Ability to change account details
- Add a payment method where a customer can make payments
- Notificaitons to email about a purchase
- View cutomer orders in the admin section
- Customer to view their previous orders and purchases

## How to launch application

1. Clone the code: `https://github.com/martinromario55/CS50-Project.git`
2. Navigate into the myshop repository
3. Activate virtual environment
5. Install all the required dependecies in the requirements.txt file `pip install -r requirements.txt`
6. Run `Flask --app run run`
7. Open `http://127.0.0.1:5000` (Press CTRL+C to quit)

## Demonstration on youtube
For the CS50 final project you have to make a video showning your project,
[My Final Project presentation](https://youtu.be/sBSQePTZIQw)
