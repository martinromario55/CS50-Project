from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response, jsonify
from shop import db, app, photos, search, bcrypt, login_manager
from flask_login import login_required, current_user, login_user, logout_user
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder
import secrets, os
from shop.products.routes import brands, categories
import pdfkit
import stripe

publishable_key = 'pk_test_51MF97vDBC1bqubIpHryUXZoGgvVuPiUQsAlqV0Ku6TVspWyVXUiI9GMgFLK84zAzlwhbMJSpE8T27PDyEF25W0ns00VMYHiY2w'
stripe.api_key = 'sk_test_51MF97vDBC1bqubIpUBoRB0UQmxxxHh3nCBVZ5FYrH2xRnjOtasmzFx8QTsZKamnpGHXRc3tKwPhCqcFzg97iTcwj00Ka7JWlmF'




@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
            city=form.city.data,
            country=form.country.data,
            contact=form.contact.data,
            address=form.address.data,
        )

        db.session.add(register)
        
        flash('Registration successful', 'success')

        db.session.commit()

        return redirect(url_for('login'))

    return render_template('customer/register.html', form=form, brands=brands(), categories=categories())


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()

    if form.validate_on_submit():
        
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)

            flash('Login successful', 'success')

            next = request.args.get('next')

            return redirect(next or url_for('home'))

        flash('Incorrect email or password', 'danger')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form, brands=brands(), categories=categories())


@app.route('/cutomer/logout')
def customer_logout():
    logout_user()

    flash('You are logged out', 'info')
    return redirect(url_for('home'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)

        try:
            order = CustomerOrder(
                invoice=invoice,
                customer_id=customer_id,
                orders=session['Shoppingcart']
            )
            
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent', 'success')
            
            return redirect(url_for('orders', invoice=invoice))

        except Exception as e:
            print(e)
            flash('Somthing went wrong', 'danger')

            return redirect(url_for('getCart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()

        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100 * float(product['price']))
            subTotal = float(product['price'] * int(product['quantity']))
            subTotal -= discount
            tax = ("%.2f" % (.02 * float(subTotal)))
            grandTotal = ("%.2f" % (1.02 * float(subTotal)))
            

    else:
        return redirect(url_for('customerLogin'))

    
    return render_template('customer/order.html', invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal, customer=customer, orders=orders)



@app.route('/payment')
@login_required
def payment():

    return render_template('customer/thanks.html')
