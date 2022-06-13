from flask import Flask, redirect, render_template, request,url_for,flash,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime, timedelta, date
import random
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


application = app = Flask(__name__)

application.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(username="Ckoko99",
    password="Team53380",
    hostname="Ckoko99.mysql.pythonanywhere-services.com",
    databasename="Ckoko99$Videogamestore",
)
application.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
application.config["SQLALCHEMY_POOL_RECYCLE"] = 299
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.secret_key = 'supersecretkey'


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "warning"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))

class Employee(db.Model, UserMixin):
    __tablename__ = "EMPLOYEE"
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    address = db.Column(db.String(50))
    addressline = db.Column(db.String(50), default='')
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    deleted = db.Column(db.Boolean)
    employed_on = db.Column(db.Date)
    def get_id(self):
        return (self.employee_id)
class Customer(db.Model, UserMixin):
    __tablename__ = "CUSTOMER"
    customer_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.Date)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(50))
    addressline = db.Column(db.String(50), default='')
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    newsletter_subscription = db.Column(db.Boolean)
    reward_points = db.Column(db.Integer)
    def get_id(self):
           return (self.customer_id)
class Customer_order(db.Model, UserMixin):
    __tablename__ = "CUSTOMER_ORDER"
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shipper_id = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.Date, nullable=False)
    delivered_on = db.Column(db.Date, nullable=False)
    gift_card_code = db.Column(db.Integer)
    gift_balance_used = db.Column(db.Integer)
    bill_name = db.Column(db.String(50), nullable=False)
    bill_address = db.Column(db.String(50), nullable=False)
    bill_city = db.Column(db.String(50), nullable=False)
    bill_state = db.Column(db.String(2), nullable=False)
    bill_zipcode = db.Column(db.Integer, nullable=False)
    bill_card_number = db.Column(db.Integer, nullable=False)
    bill_cvc = db.Column(db.Integer)
    # email = db.Column(db.String(30), nullable=False)
    ship_name = db.Column(db.String(50), nullable=False)
    ship_address = db.Column(db.String(50), nullable=False)
    ship_city = db.Column(db.String(50))
    ship_state = db.Column(db.String(2), nullable=False)
    ship_zipcode = db.Column(db.Integer, nullable=False)
    total_quantity= db.Column(db.Integer, nullable=False)
    total_price= db.Column(db.Float, nullable=False)
    def get_id(self):
           return (self.order_id)
class Inventory(db.Model):
    __tablename__ = "INVENTORY"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    product_type = db.Column(db.String(15))
    product_description = db.Column(db.String(1000))
    quantity_in_stock = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, default=False)
    unit_price = db.Column(db.Float)
    image_source = db.Column(db.String(1000))
    number_of_ratings = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Integer)
    min_quantity = db.Column(db.Integer, default=5)             # NEW EDIT
    quantity_goal_when_low = db.Column(db.Integer, default=20)  # NEW EDIT
    def get_id(self):
        return(self.product_id)

class Supplier(db.Model):
    __tablename__ =  "SUPPLIER"
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    def get_id(self):
        return(self.supplier_id)

class SupplierOrder(db.Model):
    __tablename__ =  "SUPPLIER_ORDER"
    supplier_order_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer)
    created_on = db.Column(db.Date)
    shipper_id = db.Column(db.Integer)    # Should probably be removed actually, since the supplier will deal with this
    status_id = db.Column(db.Integer)
    total_quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    def get_id(self):
        return(self.supplier_order_id)

class SupplierOrderItem(db.Model):
    __tablename__ =  "SUPPLIER_ORDER_ITEM"
    supplier_order_item_id = db.Column(db.Integer, primary_key=True)
    supplier_order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    def get_id(self):
        return(self.supplier_order_item_id)

class Shippers(db.Model):
    __tablename__ =  "SHIPPERS"
    shipper_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def get_id(self):
        return(self.shipper_id)

class Order_status(db.Model):
    __tablename__ = "ORDER_STATUS"
    order_status_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    paid = db.Column(db.Boolean)
    shipped = db.Column(db.Boolean)
    delivered = db.Column(db.Boolean)
    cancelled = db.Column(db.Boolean)
    def get_id(self):
        return(self.order_status.id)

class Customer_order_item(db.Model):
    __tablename__ = "CUSTOMER_ORDER_ITEM"
    order_item_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    deal_code = db.Column(db.String)
    profit = db.Column(db.Float)
    def get_id(self):
        return(self.order_status.id)

class Gift(db.Model):
    __tablename__ = "GIFT_CARD"
    gift_card_code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    balance = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    def get_id(self):
        return(self.gift_card_code)

class MyModelView(ModelView):
    column_display_pk = True
    def is_accessible(self):
        if 'logged_in' in session:
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect('https://ckoko99.pythonanywhere.com/admin/')

admin = Admin(application,name='Dashboard', template_mode='bootstrap3')


admin.add_view(MyModelView( Employee,db.session))
admin.add_view(MyModelView( Customer,db.session))
admin.add_view(MyModelView( Customer_order,db.session))
admin.add_view(MyModelView( Customer_order_item,db.session))
admin.add_view(MyModelView( Order_status,db.session))
admin.add_view(MyModelView( Inventory,db.session))
admin.add_view(MyModelView( Shippers,db.session))
admin.add_view(MyModelView( Supplier,db.session))
admin.add_view(MyModelView( SupplierOrder,db.session))
admin.add_view(MyModelView( SupplierOrderItem,db.session))
admin.add_view(MyModelView( Gift,db.session))

@app.route('/videogames/',methods=['GET', 'POST'])
def videogames():
    currentinventory = Inventory.query.all()
    InventoryMatches = []
    for item in currentinventory:
        if item.product_type == 'videogame':
            InventoryMatches.append(item)

    if session.get('employee_logged_in'):   # User is an Employee
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template("search.html", searcheditems=InventoryMatches, user=current_employee)
    else:                                   # User is a Customer
        return render_template("search.html", searcheditems=InventoryMatches, user=current_user)
@app.route('/consoles/',methods=['GET', 'POST'])
def consoles():
    currentinventory = Inventory.query.all()
    InventoryMatches = []
    for item in currentinventory:
        if item.product_type == 'console':
            InventoryMatches.append(item)

    if session.get('employee_logged_in'):   # User is an Employee
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template("search.html", searcheditems=InventoryMatches, user=current_employee)
    else:                                   # User is a Customer
        return render_template("search.html", searcheditems=InventoryMatches, user=current_user)
@app.route('/accessories/',methods=['GET', 'POST'])
def accessories():
    currentinventory = Inventory.query.all()
    InventoryMatches = []
    for item in currentinventory:
        if item.product_type == 'accessory':
            InventoryMatches.append(item)

    if session.get('employee_logged_in'):   # User is an Employee
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template("search.html", searcheditems=InventoryMatches, user=current_employee)
    else:                                   # User is a Customer
        return render_template("search.html", searcheditems=InventoryMatches, user=current_user)

@app.route('/gift/', methods=['GET', 'POST'])
def gift():
    if session.get('employee_logged_in'):  # Only for Customers, not Employees
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('gift.html', user=current_user)
    else:
        json_sent = request.get_json()

        gift_card_number = json_sent['bill_card_number']
        gift_cvc = json_sent['bill_cvc']
        # Pseudocode: (Make transaction using card number & cvc) if we were actually charging money from a bank or something

        balance = json_sent['balance'] # request.form.get('amount')
        new_gift_card = Gift(balance=balance, start_date=date.today().strftime('%Y-%m-%d'))
        db.session.add(new_gift_card)
        db.session.commit()

        response = {'giftcode': new_gift_card.gift_card_code}
        return jsonify(response)

@app.route('/rewards/', methods=['GET', 'POST'])
def rewards():
    if session.get('employee_logged_in'):  # Only for Customers, not Employees
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('rewards.html', user=current_user)
    else:
        json_sent = request.get_json()

        gift_card_number = '0000 0000 0000 0000'
        gift_cvc = '000'
        # Pseudocode: (Make transaction using card number & cvc) if we were actually charging money from a bank or something

        points_after = int(current_user.reward_points) - int(json_sent['points'])
        if points_after >= 0:
            current_user.reward_points = points_after
        else:
            user = Customer.query.filter_by(username=current_user.username).first()
            user.reward_points = 50
            db.session.commit()
            messages = 'Not enough reward points for this reward'
            flash(messages, category='danger')
            response = {'success': False}
            return jsonify(response)

        balance = int(json_sent['balance']) # request.form.get('amount')
        new_gift_card = Gift(balance=balance, start_date=date.today().strftime('%Y-%m-%d'))
        db.session.add(new_gift_card)
        db.session.commit()

        response = {'giftcode': new_gift_card.gift_card_code, 'balance': new_gift_card.balance, 'success': True, 'points_after': points_after}
        return jsonify(response)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('employee_logged_in'):  # Only for Customers, not Employees
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('register.html', user=current_user)
    else:
        username = request.form.get('usernameRegister')
        password = request.form.get('passwordRegister')
        confirmPassword = request.form.get('passwordConfirm')
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        email = request.form.get('emailRegister')
        phone = request.form.get('phone')

        AddressLine1 = request.form.get('address1')
        AddressLine2 = request.form.get('address2')
        if AddressLine2 is None:
            AddressLine2 = ''
        City = request.form.get('city')
        State = request.form.get('state')
        Zipcode = request.form.get('zipcode')
        newsletter_subscription = request.form.get('newsletter')
        if newsletter_subscription == "on":
            newsletter_subscription = True
        else:
            newsletter_subscription = False

        user = Customer.query.filter_by(username=username).first()
        if user:
            return "<p>username is taken</p>"
        else:
            user = Customer.query.filter_by(email=email).first()
            if user:
                return "<p>email is taken</p>"
            else:
                if password == confirmPassword:
                    new_customer = Customer(created_on=date.today().strftime('%Y-%m-%d'),username=username,password=password,fname=fname,lname=lname,email=email,phone=phone,address=AddressLine1,addressline=AddressLine2,city=City,state=State,zipcode=Zipcode,newsletter_subscription=newsletter_subscription,reward_points=0)
                    db.session.add(new_customer)
                    db.session.commit()
                    login_user(new_customer, remember=True)
                    return redirect('/')
                else:
                    return "<p>passwords don't match</p>"

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        if session.get('employee_logged_in'):   # User is an Employee
            current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
            return render_template('login.html', user=current_employee)
        else:                                   # User is a Customer
            return render_template('login.html', user=current_user)
    else:
        username = request.form.get('usernameLogin')
        password = request.form.get('passwordLogin')

        user = Customer.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                # session.clear()
                login_user(user, remember=True)
                messages = 'You are now logged in'
                flash(messages, category='success')
                return redirect(url_for('home'))
            else:
                messages = 'Wrong Password'
                flash(messages, category='danger')
                return redirect(url_for('login'))
        else:
            messages = 'User not found'
            flash(messages, category='danger')
            return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    messages = 'You have been logged out successfully'
    flash(messages, category='success')
    return redirect('/')

@app.route("/profile", methods=["GET", "POST"]) # user profile page when logged in
@login_required
def profile():
    if request.method == 'GET':
        if session.get('employee_logged_in'):
            current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
            if current_employee.deleted:
                flash(str(current_employee.username)+' is no longer working here', category='danger')
                session.clear()
                return redirect(url_for('employeelogin'))
            else:
                return render_template('profile.html', user=current_employee)
        else:
            return render_template('profile.html', user=current_user)
    else:
        username = request.form.get('username')
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        email = request.form.get('email')
        phone = request.form.get('phone')

        AddressLine1 = request.form.get('address1')
        AddressLine2 = request.form.get('address2')
        if AddressLine2 == None:
            AddressLine2 = ''
        City = request.form.get('city')
        State = request.form.get('state')
        Zipcode = request.form.get('zipcode')

        if session.get('employee_logged_in'):
            employeeID = session.get('employee_id')
            current_employee = Employee.query.filter_by(employee_id=int(employeeID)).first()

            # job_title should be readonly, no newsletter_subscription

            employee = Employee.query.filter_by(username=username).first()
            if employee:
                if username != current_employee.username:
                    messages = 'Username is already taken'
                    flash(messages, category='danger')
                    return redirect(url_for('profile'))
            employee = Employee.query.filter_by(email=email).first()
            if employee:
                if email != current_employee.email:
                    messages = 'Email is already taken'
                    flash(messages, category='danger')
                    return redirect(url_for('profile'))

            employee = Employee.query.filter_by(username=current_employee.username).first()
            employee.username = username
            employee.fname = fname
            employee.lname = lname
            employee.email = email
            employee.phone = phone
            employee.address = AddressLine1
            employee.addressline = AddressLine2
            employee.city = City
            employee.state = State
            employee.zipcode = Zipcode
            db.session.commit()

            messages = 'Profile info has been updated successfully'
            flash(messages, category='success')
            return redirect(url_for("profile"))
        else:
            newsletter_subscription = request.form.get('newsletter')
            if newsletter_subscription == "on":
                newsletter_subscription = True
            else:
                newsletter_subscription = False

            user = Customer.query.filter_by(username=username).first()
            if user:
                if username != current_user.username:
                    messages = 'Username is already taken'
                    flash(messages, category='danger')
                    return redirect(url_for('profile'))
            user = Customer.query.filter_by(email=email).first()
            if user:
                if email != current_user.email:
                    messages = 'Email is already taken'
                    flash(messages, category='danger')
                    return redirect(url_for('profile'))

            user = Customer.query.filter_by(username=current_user.username).first()
            user.username = username
            user.fname = fname
            user.lname = lname
            user.email = email
            user.phone = phone
            user.address = AddressLine1
            user.addressline = AddressLine2
            user.city = City
            user.state = State
            user.zipcode = Zipcode
            user.newsletter_subscription = newsletter_subscription
            db.session.commit()

            messages = 'Profile info has been updated successfully'
            flash(messages, category='success')
            return redirect(url_for("profile"))

class LogItem(db.Model):
    __tablename__ = "LOGGED_ITEM"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    supplier_order_item_id = db.Column(db.Integer) #Since this is a 1 to 1 Relationship
    quantity = db.Column(db.Integer)
    logged_on = db.Column(db.Date)
    def get_id(self):
        return(self.log_id)

@app.route("/employeelogin/", methods=['GET', 'POST'])
def employeelogin():
    if request.method == 'GET':
        return render_template('employeelogin.html', user=current_user) # Would ideally always pass an unauthenticated user
    if request.method == 'POST':
        username = request.form.get('employeeUsernameLogin')
        password = request.form.get('employeePasswordLogin')

        user = Employee.query.filter_by(username=username).first()
        if user and user.deleted == False:
            if user.password == password:
                login_user(Customer.query.filter_by(username='admin').first(), remember=True)   # Critical New Edit
                session['employee_logged_in'] = True
                session['employee_id'] = user.get_id()
                return redirect(url_for('home'))
            else:
                messages = 'Wrong Password'
                flash(messages, category='danger')
                return redirect(url_for('employeelogin', messages=messages))
        else:
            session.clear()
            messages = 'User not found'
            flash(messages, category='danger')
            return redirect(url_for('employeelogin', messages=messages))

@app.route("/user-activity/", methods=['GET', 'POST'])
@login_required
def useractivity():
    if not session.get('employee_logged_in'):
        return redirect(url_for('employeelogin'))
    if request.method == 'GET':
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template('UserActivityReport.html', user=current_employee)
    else:
        json_sent = request.get_json()
        from_date = datetime.strptime(str(json_sent['from_date']), '%Y-%m-%d').date()

        customer_users = Customer.query.order_by(desc(Customer.created_on)).all()
        customer_matches = []
        for customer in customer_users:
            d = datetime.strptime(str(customer.created_on), '%Y-%m-%d').date()
            if from_date <= d:
                if customer not in customer_matches:
                    orders = Customer_order.query.filter_by(customer_id=int(customer.customer_id)).order_by(desc(Customer_order.created_on))
                    last_active = orders.first().created_on.strftime('%Y-%m-%d') if orders.first() else d.strftime('%Y-%m-%d')

                    orders = orders.all()
                    num_orders = 0
                    num_products = 0
                    total_spent = 0
                    for o in orders:
                        num_orders = num_orders + 1
                        num_products = num_products + o.total_quantity
                        total_spent = total_spent + o.total_price
                    if customer.addressline:
                        addr = (customer.address+" "+customer.addressline).strip()
                    else:
                        addr = customer.address.strip()
                    customer_matches.append({'joined_on': d.strftime('%Y-%m-%d'), 'username': customer.username, 'name': (customer.fname+" "+customer.lname).strip(), 'email': customer.email, 'phone': customer.phone, 'address': (addr+", "+customer.city+", "+customer.state+" "+str(customer.zipcode)).strip(), 'last_active': last_active, 'num_orders': num_orders, 'num_products': num_products, 'total_spent': total_spent})

        response = {'customers': customer_matches, 'success': True, 'amount': len(customer_matches)}
        return jsonify(response)

@app.route("/employee-activity/", methods=['GET', 'POST'])
@login_required
def employeeactivity():
    if not session.get('employee_logged_in'):
        return redirect(url_for('employeelogin'))
    if request.method == 'GET':
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template('EmployeeActivityReport.html', user=current_employee)
    else:
        json_sent = request.get_json()
        from_date = datetime.strptime(str(json_sent['from_date']), '%Y-%m-%d').date()

        employee_users = Employee.query.order_by(desc(Employee.employed_on)).all()
        employee_matches = []
        for employee in employee_users:
            d = datetime.strptime(str(employee.employed_on), '%Y-%m-%d').date()
            if from_date <= d:
                if employee not in employee_matches and not employee.deleted:
                    logged_items = LogItem.query.filter_by(employee_id=int(employee.employee_id)).order_by(desc(LogItem.logged_on))
                    last_active = logged_items.first().logged_on.strftime('%Y-%m-%d') if logged_items.first() else d.strftime('%Y-%m-%d')

                    logged_items = logged_items.all()
                    num_logs = 0
                    num_items = 0
                    for li in logged_items:
                        num_logs = num_logs + 1
                        num_items = num_items + li.quantity
                    addr = ""
                    if employee.addressline:
                        addr = (employee.address+" "+employee.addressline).strip()
                    else:
                        addr = employee.address.strip()
                    employee_matches.append({'employed_on': d.strftime('%Y-%m-%d'), 'title': employee.job_title, 'username': employee.username, 'name': (employee.fname+" "+employee.lname).strip(), 'email': employee.email, 'phone': employee.phone, 'address': (addr+", "+employee.city+", "+employee.state+" "+str(employee.zipcode)).strip(), 'last_active': last_active, 'num_items': num_items})

        response = {'employees': employee_matches, 'success': True, 'amount': len(employee_matches)}
        return jsonify(response)

@app.route("/sales/", methods=['GET', 'POST'])
@login_required
def sales():
    if not session.get('employee_logged_in'):
        return redirect(url_for('employeelogin'))
    if request.method == 'GET':
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template('SalesReport.html', user=current_employee)
    else:
        json_sent = request.get_json()
        from_date = datetime.strptime(str(json_sent['from_date']), '%Y-%m-%d').date()

        logged_items = LogItem.query.order_by(desc(LogItem.logged_on)).all()
        item_matches = []
        for item in logged_items:
            d = datetime.strptime(str(item.logged_on), '%Y-%m-%d').date()
            if from_date <= d:
                order_items = Customer_order_item.query.filter_by(product_id=int(item.product_id))
                for orderitem in order_items:
                    orders = Customer_order.query.filter_by(order_id=orderitem.order_id).order_by(desc(Customer_order.created_on))
                    last_bought_on = orders.first().created_on.strftime('%Y-%m-%d')
                    first_bought_on = Customer_order.query.filter_by(order_id=orderitem.order_id).order_by(Customer_order.created_on).first().created_on.strftime('%Y-%m-%d')

                    orders = orders.all()
                    num_orders = 0
                    quantity_bought = 0
                    total_profit = 0
                    for o in orders:
                        num_orders = num_orders + 1
                        for o_item in Customer_order_item.query.filter_by(order_id=o.order_id).all():
                            quantity_bought = quantity_bought + o_item.quantity
                            total_profit = total_profit + o_item.profit

                    p = Inventory.query.filter_by(product_id=int(item.product_id)).first()

                    index = next((i for (i, d) in enumerate(item_matches) if d['name'] == p.product_name), None)
                    if index is None: # and not item.deleted
                        item_matches.append({'index': index, 'logged_on': d.strftime('%Y-%m-%d'), 'first_bought_on': first_bought_on, 'last_bought_on': last_bought_on, 'name': p.product_name, 'type': p.product_type, 'unit_price': p.unit_price, 'current_quantity': p.quantity_in_stock, 'quantity_bought': quantity_bought, 'num_orders': num_orders, 'total_profit': total_profit})
                    elif not p.deleted:
                        item_matches[index]['quantity_bought'] = item_matches[index]['quantity_bought'] + quantity_bought
                        item_matches[index]['num_orders'] = item_matches[index]['num_orders'] + num_orders
                        item_matches[index]['total_profit'] = item_matches[index]['total_profit'] + total_profit

        response = {'products': item_matches, 'success': True, 'amount': len(item_matches)}
        return jsonify(response)

@app.route("/restocks/", methods=['GET', 'POST'])
@login_required
def restocks():
    if not session.get('employee_logged_in'):
        return redirect(url_for('employeelogin'))
    if request.method == 'GET':
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template('RestockReport.html', user=current_employee)
    else:
        json_sent = request.get_json()
        from_date = datetime.strptime(str(json_sent['from_date']), '%Y-%m-%d').date()

        supplier_order_items = SupplierOrderItem.query.order_by(SupplierOrderItem.product_id).all()
        item_matches = []
        for item in supplier_order_items:
            orders = SupplierOrder.query.filter_by(supplier_order_id=int(item.supplier_order_id)).order_by(desc(SupplierOrder.created_on))
            last_restocked_on = ""
            first_restocked_on = ""

            orders = orders.all()
            num_orders = 0
            quantity_restocked = 0
            for s_o in orders:
                if from_date <= s_o.created_on:
                    num_orders = num_orders + 1
                    if first_restocked_on == "":
                        first_restocked_on = s_o.created_on.strftime('%Y-%m-%d')
                    last_restocked_on = s_o.created_on.strftime('%Y-%m-%d')
                    for s_o_item in SupplierOrderItem.query.filter_by(supplier_order_id=s_o.supplier_order_id).all():
                        quantity_restocked = quantity_restocked + s_o_item.quantity

            if first_restocked_on != "" and last_restocked_on != "":
                p = Inventory.query.filter_by(product_id=int(item.product_id)).first()
                index = next((i for (i, d) in enumerate(item_matches) if d['name'] == p.product_name), None)
                if index is None: # and not item.deleted
                    item_matches.append({'first_restocked_on': first_restocked_on, 'last_restocked_on': last_restocked_on, 'name': p.product_name, 'type': p.product_type, 'unit_price': p.unit_price, 'current_quantity': p.quantity_in_stock, 'quantity_restocked': quantity_restocked, 'num_orders': num_orders})
                elif not p.deleted:
                    if item_matches[index]['first_restocked_on'] > first_restocked_on:
                        item_matches[index]['first_restocked_on'] = first_restocked_on
                    if item_matches[index]['last_restocked_on'] < last_restocked_on:
                        item_matches[index]['last_restocked_on'] = last_restocked_on
                    item_matches[index]['quantity_restocked'] = item_matches[index]['quantity_restocked'] + quantity_restocked
                    item_matches[index]['num_orders'] = item_matches[index]['num_orders'] + num_orders

        response = {'products': item_matches, 'success': True, 'amount': len(item_matches)}
        return jsonify(response)

@app.route("/addItem/", methods=['GET', 'POST'])
@login_required
def additem():
    if not session.get('employee_logged_in'):
        return redirect(url_for('employeelogin'))
    if request.method == 'GET':
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template('add-item.html', user=current_employee)
    else:
        # employee_id = get current_employee's id (that's logged in)
        employee_id = session.get('employee_id')

        sent_json = request.get_json()
        supplier_name = sent_json['supplier_name']
        supplier_email = sent_json['supplier_email']
        supplier_phone = sent_json['supplier_phone']
        product_name = sent_json['item_name']
        product_type = sent_json['item_type']
        unit_price = float(sent_json['unit_price'])
        quantity = sent_json['quantity']
        total_price = float(unit_price) * float(quantity)
        desc = sent_json['desc']
        image_source = sent_json['image_source']
        if image_source == "":
            image_source = None

        product = Inventory.query.filter_by(product_name=product_name).first()
        if product is None:
            product = Inventory(product_name=product_name,product_type=product_type,product_description=desc,quantity_in_stock=quantity,unit_price=unit_price,image_source=image_source)
            db.session.add(product)
            db.session.commit()
            messages = 'Added new item successfully'
            flash(messages, category='success')
        else:
            if product.unit_price == unit_price and product.product_type == product_type:
                product.quantity_in_stock = product.quantity_in_stock + quantity
                db.session.commit()
                messages = 'Added to existing item successfully'
                flash(messages, category='success')
            else:
                messages = 'Item in Database has different details'
                flash(messages, category='danger')
                response = {'message': messages, 'success': False, 'product_id': product.product_id}
                return jsonify(response)

        supplier = Supplier.query.filter_by(supplier_name=supplier_name).first()
        if supplier is None:
            supplier = Supplier(supplier_name=supplier_name,email=supplier_email,phone=supplier_phone)
            db.session.add(supplier)
            db.session.commit()

        order_status = Order_status(paid=True,shipped=True,delivered=True,cancelled=False)
        db.session.add(order_status)
        db.session.commit()

        today = date.today().strftime('%Y-%m-%d')
        supplier_order = SupplierOrder(supplier_id=supplier.supplier_id,created_on=today,shipper_id=random.randint(1,2),status_id=order_status.order_status_id,total_quantity=quantity,total_price=total_price)
        db.session.add(supplier_order)
        db.session.commit()

        supplier_order_item = SupplierOrderItem(supplier_order_id=supplier_order.supplier_order_id,product_id=product.product_id,quantity=quantity,unit_price=unit_price)
        db.session.add(supplier_order_item)
        db.session.commit()

        new_log_item = LogItem(employee_id=employee_id,product_id=product.product_id,supplier_order_item_id=supplier_order_item.supplier_order_item_id,quantity=quantity,logged_on=today)
        db.session.add(new_log_item)
        db.session.commit()

        response = {'message': 'Item was successfully added', 'success': True,  'product_id': product.product_id}
        return jsonify(response)
        # return render_template('add-item.html', user=current_user)

@app.route("/admin/", methods=['POST','GET'])
def adminlogin():

    if request.method == 'POST':

        if 'logged_in' not in session:
            username = request.form.get('adminUsernameLogin')
            password = request.form.get('adminPasswordLogin')
            messages = []

            if username == 'admin':
                if password == 'admin':

                    session['logged_in'] = True
                    session['username'] = username
                    messages = 'Login successfully'
                    flash(messages, category='success')

                    return  redirect("https://ckoko99.pythonanywhere.com/admin/")
                else:
                    messages = 'Wrong Credentials'
                    flash(messages, category='danger')
                    return redirect("https://ckoko99.pythonanywhere.com/admin/")
            else:

                messages = 'Wrong Credentials'
                flash(messages, category='danger')
                return redirect("https://ckoko99.pythonanywhere.com/admin/")
        else:

            session.clear()
            messages = 'You have been logged out successfully'
            flash(messages, category='success')
            return redirect("https://ckoko99.pythonanywhere.com/admin/")



@app.route("/search/", methods=['GET'])
def search():
    theurl = request.url
    search = theurl[theurl.find("?search=")+8:]
    search = search.lower()
    searches = search.split("+")
    currentinventory = Inventory.query.all()
    InventoryMatches = []
    for item in currentinventory:
        for searchword in searches:
            if searchword.lower() in item.product_name.lower():
                if item not in InventoryMatches:
                    InventoryMatches.append(item)

    if session.get('employee_logged_in'):   # User is an Employee
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        return render_template("search.html", searcheditems=InventoryMatches, user=current_employee)
    else:                                   # User is a Customer
        return render_template("search.html", searcheditems=InventoryMatches, user=current_user)

@app.route("/cart", methods=['GET','POST'])
def cart():
    if session.get('employee_logged_in'):  # Only for Customers, not Employees
        return redirect(url_for('login'))
    return render_template("cart.html", user=current_user)

@app.route("/checkout/", methods=['GET','POST'])
@login_required
def checkout():
    if session.get('employee_logged_in'):  # Only for Customers, not Employees
        return redirect(url_for('login'))
    if request.method == 'POST':
        totalq =0
        ready = False
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        address = request.form.get('address')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        c_id = current_user.customer_id
        created_on = date.today().strftime('%Y-%m-%d')
        delivered_on = date.today() + timedelta(days=2)                  # Note: DB has it as NOT NULL, can be changed
        gift_card_code = request.form.get('gift-code')
        gift_balance_used = request.form.get('gift-balance')

        bill_name = fname+" "+lname
        bill_address = address+" "+address2
        bill_city = city
        bill_state = state
        bill_zipcode = zipcode
        bill_card_number = request.form.get("cardNumber") # Note: the frontend is currently only requiring these 2 values to submit, include the rest
        bill_cvc = request.form.get('cvc')   # Note: the frontend is currently only requiring these 2 values to submit, include the rest
        ship_name = fname+" "+lname
        ship_address = address
        ship_city = city
        ship_state = state
        ship_zipcode = zipcode

        t_quantity=request.form.getlist('quantity')
        subtotal=request.form.getlist('subtotal')
        total_price = request.form.get('total')
        product_name = request.form.getlist('product')

        for (qt,pn) in zip(t_quantity,product_name):
            check_qt = Inventory.query.filter_by(product_name=pn).first()
            if check_qt.quantity_in_stock >= int(qt):
                totalq+=int(qt)
                check_qt.quantity_in_stock = int(check_qt.quantity_in_stock) - int(qt)
                db.session.commit()
            else:
                messages = "There is {} '{}' in stock".format(check_qt.quantity_in_stock,pn)
                flash(messages, category='danger')
                return  redirect(url_for('checkout', messages=messages))

        if gift_card_code:
            gift = Gift.query.filter_by(gift_card_code = int(gift_card_code)).first()
            if gift:
                if gift.balance > int(gift_balance_used):
                    # gift.balance = int(gift.balance) - int(gift_balance_used)
                    # db.session.commit()

                    # if float(total_price) > float(gift_balance_used):   # NEW EDIT (Was previously just before ###...UPDATE ORDER_STATUS...###)
                    #     total_price = float(total_price)-float(gift_balance_used)
                    if float(total_price) < float(gift_balance_used):
                        messages = "You tried paying more than the total price with your gift card"
                        flash(messages, category='danger')
                        return  redirect(url_for('checkout', messages=messages))
                    # else:
                    #     total_price = 0.00
                else:
                    messages = "Your gift card balance is only ${}".format(gift.balance)
                    flash(messages, category='danger')
                    return  redirect(url_for('checkout', messages=messages))
            else:
                messages = "Gift code is invalid"
                flash(messages, category='danger')
                return  redirect(url_for('checkout', messages=messages))
        else:
            gift_card_code = None       # NEW EDIT
            gift_balance_used = None    # NEW EDIT


        ################### UPDATE  ORDER_STATUS ##############
        order_status = Order_status(paid=True,shipped=True,delivered=True,cancelled=False)
        db.session.add(order_status)
        db.session.commit()
        ######################################################################################


        ############################ ADD NEW ORDER IN CUSTOMER ORDER TABLE  ##############################################
        new_order = Customer_order(customer_id = c_id,
        shipper_id = random.randint(1,2),
        status_id = order_status.delivered,
        created_on = created_on,
        delivered_on = delivered_on,
        gift_card_code = gift_card_code,
        gift_balance_used = gift_balance_used,
        bill_name = bill_name,
        bill_address = bill_address,
        bill_city = bill_city,
        bill_state = bill_state,
        bill_zipcode = int(bill_zipcode),
        bill_card_number = int(bill_card_number),
        bill_cvc = int(bill_cvc),
        ship_name = ship_name,
        ship_address = ship_address,
        ship_city = ship_city,
        ship_state = ship_state,
        ship_zipcode = int(ship_zipcode),
        total_quantity = totalq,
        total_price = float(total_price)
        )
        db.session.add(new_order)
        db.session.commit()
        ##########################  RETRIEVE THE ORDER ID FROM THE CUSTOMER ORDER TABLE  TO USE IT IN CUSTOMER ORDER ITEM ##########################
        od = Customer_order.query.filter_by(order_id = new_order.order_id).first()


        ################################### ADD EACH ITEM IN THE CART TO THE CUSTOMER ORDER ITEM TABLE
        for (pn,s,tq) in zip(product_name,subtotal,t_quantity):
            pid = Inventory.query.filter_by(product_name=pn).first()
            pid = pid.product_id
            unit_price = float(s)/float(tq)
            new_customer_order_item = Customer_order_item(order_id=od.order_id,product_id=pid,quantity=int(tq),unit_price=unit_price,profit=0)
            db.session.add(new_customer_order_item)
            db.session.commit()
            ready = True

        if ready:
            messages = 'we have received your order'
            flash(messages, category='success')

            if current_user.reward_points >= 1000:
                messages = 'You got over 1000 reward points!'
                flash(messages, category='success')
            elif current_user.reward_points >= 250:
                messages = 'You got over 250 reward points!'
                flash(messages, category='success')
            elif current_user.reward_points >= 50:
                messages = 'You got over 50 reward points!'
                flash(messages, category='success')

            return  redirect(url_for('home', messages=messages))
        else:
            messages = 'Something went wrong during checkout proccess, please try again'
            flash(messages, category='danger')
            return  redirect(url_for('checkout', messages=messages))

    else:
        return render_template("checkout.html",user=current_user)

@app.route('/',  methods=["GET", "POST"])
def home():
    # if request.method == 'POST':
    #     text = request.form.get('search')
    #     return "<p>" + text + "</p."
    # else:
    if session.get('employee_logged_in'):  # Specify that user is an Employee
        current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
        if current_employee.deleted:
            flash(str(current_employee.username)+' is no longer working here', category='danger')
            session.clear()
            return redirect(url_for('employeelogin'))
        else:
            return render_template('home.html', user=current_employee)
    else:   # User is a Customer
        return render_template('home.html', user=current_user)

@app.route('/product/<theproduct>', methods=["GET", "POST"])
def product(theproduct):
    if request.method == "GET":
        product = Inventory.query.filter_by(product_id=theproduct).first()
        if product:
            if session.get('employee_logged_in'):   # User is an Employee
                current_employee = Employee.query.filter_by(employee_id=int(session.get('employee_id'))).first()
                return render_template('product-details.html', product=product, user=current_employee)
            else:                                   # User is a Customer
                return render_template('product-details.html', product=product, user=current_user)
        else:
            return redirect(url_for('login', message = "<p>product not found</p>"))
    else:
        return redirect(url_for('cart'))

# @app.route("/addemployee/", methods=['POST','GET'])
# def addemployee():
#     if request.method == 'POST':

#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         job_title = request.form.get('title')
#         # date = request.form.get('date')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password= request.form.get('password')
#         address = request.form.get('address')
#         address2 = request.form.get('address2') if request.form.get('address2') else ""
#         city = request.form.get('city')
#         state = request.form.get('state')
#         zipcode = request.form.get('zipcode')
#         phone = request.form.get('phone')

#         messages = []
#         found_email = Employee.query.filter_by(email=email).first()
#         found_username = Employee.query.filter_by(username=username).first()
#         if found_email:
#             messages = 'Email taken'
#             flash(messages, category='danger')
#             return  redirect(url_for('addemployee',user=current_user,messages=messages))
#         elif found_username:
#             messages = 'Username taken'
#             flash(messages, category='danger')
#             return  redirect(url_for('addemployee',user=current_user,messages=messages))
#         else:

#             new_employee = Employee(job_title=job_title,username=username,email=email,password=password,phone=phone,fname=fname,lname=lname,address=address,addressline=address2,city=city,state=state,zipcode=zipcode,deleted=0)
#             db.session.add(new_employee)
#             db.session.commit()
#             messages = 'Employee added Successfully'
#             flash(messages, category='success')
#         # return redirect(url_for('addemployee',user=current_user,messages=messages))
#         return render_template('AddEmployee.html',user=current_user,messages=messages)
#     else:
#         return render_template('AddEmployee.html',user=current_user)

# @app.route("/addemployeelogin/", methods=['POST','GET'])
# def addemployeelogin():
#     if request.method == 'GET':
#         username = request.form.get('adminUsernameLogin')
#         password = request.form.get('adminPasswordLogin')
#         messages = []

#         if username == 'admin':
#             if password == 'admin':

#                 messages = 'Login successfully'
#          #       flash(messages, category='success')
#                 return redirect(url_for('dashboard', admin = username, messages = messages))
#             else:
#                 messages = 'wrong password'
#         #        flash(messages, category='danger')
#                 return redirect(url_for('adminlogin', messages = messages))
#         else:

#             messages = 'user does not exist'
#           # flash(messages, category='danger')
#         #    flash(messages)
#             return redirect(url_for('adminlogin', messages = messages, user=current_user))
#     else:
#         return render_template('AddEmployee.html')
# @app.route("/viewemployee/", methods=['POST','GET'])
# def viewemployees():
#     if request.method == 'GET':
#         all_employees = Employee.query.filter_by(deleted=0).all()
#         return render_template('ViewEmployee.html',user=current_user,all_employees=all_employees)
#     else:
#         id = request.form.get('id')
#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         job_title = request.form.get('title')
#         # date = request.form.get('date')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         address = request.form.get('address1')
#         address2 = request.form.get('address2') if request.form.get('address2') else ""
#         city = request.form.get('city')
#         state = request.form.get('state')
#         zipcode = request.form.get('zipcode')
#         phone = request.form.get('phone')

#         messages = []
#         found = Employee.query.filter_by(employee_id=id).first()

#         if found:
#             password = found.password
#             found.job_title=job_title
#             found.username=username
#             found.email=email
#             found.password=password
#             found.phone=phone
#             found.fname=fname
#             found.lname=lname
#             found.address=address
#             found.addressline=address2
#             found.city=city
#             found.state=state
#             found.zipcode=zipcode
#             found.deleted=0
#             db.session.commit()

#             messages = 'Employee Info Updated Successfully'
#             flash(messages, category='success')
#         # return redirect(url_for('addemployee',user=current_user,messages=messages))
#             return redirect(url_for('viewemployees', messages = messages, user=current_user))
#         else:
#             messages = 'Employee info could not be updated'
#             flash(messages, category='danger')
#             return render_template('ViewEmployee.html',user=current_user, messages=messages)


# @app.route("/viewcustomers/", methods=['POST','GET'])
# def viewcustomers():
#     if request.method == 'GET':
#         all_customer = Customer.query.all()
#         return render_template('ViewCustomers.html',user=current_user,all_customer=all_customer)



if __name__ == "__main__":
    application.debug = True
    application.run()
