from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import current_user
from shop import db, app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories


def MergerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        return False



@app.route('/addcart', methods=['GET', 'POST'])
def AddCart():
    if current_user.is_authenticated:
        try:
            product_id = request.form.get('product_id')
            quantity = int(request.form.get('quantity'))
            color = request.form.get('colors')
            product = Addproduct.query.filter_by(id=product_id).first()
            
            if request.method == 'POST' and quantity and product_id and color:
                DictItems = {
                    product_id:{
                    'name': product.name,
                    'price': float(product.price),
                    'discount': product.discount,
                    'color': color,
                    'quantity': quantity,
                    'image': product.image_1,
                    'colors': product.colors
                    } 
                }

                if 'Shoppingcart' in session:
                    print(session['Shoppingcart'])
                    if product_id in session['Shoppingcart']:
                        for key, item in session['Shoppingcart'].items():
                            if int(key) == int(product_id):
                                session.modified = True
                                item['quantity'] += 1
                        
                    else:
                        session['Shoppingcart'] = MergerDicts(session['Shoppingcart'], DictItems)
                        return redirect(request.referrer)

                else:
                    session['Shoppingcart'] = DictItems
                    return redirect(request.referrer)

        except Exception as e:
            print(e)
        finally:
            return redirect(request.referrer)

    flash('You need to login first', 'warning')
    return redirect(url_for('customerLogin'))

@app.route('/carts')
def getCart():
    if current_user.is_authenticated:
        if 'Shoppingcart' not in session or len(session['Shoppingcart']) < 1:
            return redirect(url_for('home'))
        
        subtotal = 0
        grandtotal = 0
        for key, product in session['Shoppingcart'].items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.02 * subtotal))
            grandtotal = float("%.2f" % (1.02 * float(subtotal)))

        return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, brands=brands(), categories=categories())
    
    flash('You need to login first', 'warning')
    return redirect(url_for('customerLogin'))


@app.route('/updatecart<int:code>', methods=['POST'])
def Updatecart(code):
    if current_user.is_authenticated:
        if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
            return redirect(url_for('home'))

        if request.method == 'POST':
            quantity = request.form.get('quantity')
            color = request.form.get('color')

            try:
                session.modified = True
                for key, item in session['Shoppingcart'].items():
                    if int(key) == code:
                        item['color'] = color
                        item['quantity'] = quantity

                        flash('Item has been updated', 'success')

                        return redirect(url_for('getCart'))
            

            except Exception as e:
                print(e)
                return redirect(url_for('getCart'))
    
    flash('You need to login first', 'warning')
    return redirect(url_for('customerLogin'))


@app.route('/delete/<int:id>')
def deleteitem(id):
    if current_user.is_authenticated:
        if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
            return redirect(url_for('home'))

        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == id:
                    session['Shoppingcart'].pop(key, None)

                    flash('Item has been deleted successfully', 'success')

                    return redirect(url_for('getCart'))

            return redirect(url_for('getCart'))
        except Exception as e:
            print(e)

            return redirect(url_for('getCart'))

    flash('You need to login first', 'warning')
    return redirect(url_for('customerLogin'))


@app.route('/clearcart')
def clearcart():
    if current_user.is_authenticated:
        try:
            session.pop('Shoppingcart', None)

            return redirect(url_for('home'))
        except Exception as e:
            print(e)

    flash('You need to login first', 'warning')
    return redirect(url_for('customerLogin'))