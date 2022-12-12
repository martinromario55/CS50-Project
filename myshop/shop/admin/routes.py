from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
import os


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    products = Addproduct.query.all()


    return render_template('admin/index.html', products=products)


@app.route('/brands')
def brands():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    brands = Brand.query.order_by(Brand.id.desc()).all()

    return render_template('admin/brands.html', brands=brands)


@app.route('/category')
def category():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    categories = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/brands.html', categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f"{form.name.data} Registered Successfully", 'success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get Login email and password
        user = User.query.filter_by(email = form.email.data).first()
        # Check for password match from the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Save email to session
            session['email'] = form.email.data
            
            flash('Login Successful', 'success')

            return redirect(request.args.get('next') or url_for('admin'))

        else:
            # If user input is incorrect
            flash('Invalid email or password', 'danger')


    return render_template('admin/login.html', form=form)