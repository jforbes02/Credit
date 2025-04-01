from flask import Flask, render_template, redirect, flash, url_for, request, session, jsonify
from flask_login import logout_user, login_required, current_user, LoginManager, login_user
from werkzeug.security import generate_password_hash
from Accounts import Account
from database import db, User, Config, Transaction, Item
from games import RPS

"""
App that
1. Creates profile for users  ✔
2. Provides new users a credit line based on age ✔
3. Has the user play rock-paper-scissors in order to pay back "credit" ✔
4. Allow users to buy things with credit 
5. Gives penalty to people that go over the credit limit
More needs realized afterwards
6. Something that provides weekly debt
7. Games playable on websites
8. Displays website Credit scores, maybe put on a leaderboard~~

"""
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secreter"
db.init_app(app)

#Login
login_manager = LoginManager()  #creates authentication system
login_manager.init_app(app)  #integrates login system with flask
login_manager.login_view = 'login'  #tells flask go to login page for unauthorized users


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/registration', methods=['GET', 'POST'])
def register():
    """
    Handles registration forms and sends new user info into the database
    """
    if request.method == 'POST':
        username = request.form['username'] #form data
        email = request.form['email'] #form data
        password = request.form['password'] #form data
        age = int(request.form['age']) #needs to be integer
        #one email per username
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        hashed_pass = generate_password_hash(password)
        i_credit = Account.initial_credit(age)
        new_user = User(username=username, email=email, password=hashed_pass, age=age, credit_limit=i_credit)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template("registration.html")

@login_manager.user_loader
def load_user(user_id):
    """
    #logged in users stay logged in when going to different page
    :param user_id: ID of the user to load
    :return: User object
    """
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """" Handles logging into the website from form submissions """
    if request.method == 'POST':
        email = request.form['email']  #form data
        password = request.form['password']  #form data

        user = User.query.filter_by(email=email).first()  #looks in database for user with email

        if user and user.check_password(password):  #checks if user was found and if password is valid
            login_user(user)  #creates session and authenticates user
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        elif not user:
            flash('User does not exist')
            return redirect(url_for('login'))
        else:
            flash('Incorrect password')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

@app.route('/dashboard')
@login_required
def dashboard():
    #items = i
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', transactions=transactions)

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    current_user.remove()
    db.session.commit()
    flash('Account deleted')
    return render_template('home.html')

@app.route('/RockPaperScissors', methods=['GET', 'POST'])
@login_required
def play_rps():
    """  Connecting the game to this  """
    if request.method == 'POST':
        try:
            data = request.get_json()
            amount = int(data.get('amount', 5))
            player_choice = data.get('player_choice')

            print(f"Received amount: {amount}, {player_choice}")
            if amount <=0:
                return jsonify({'error': 'Enter number > 0'}), 400

            g_result = RPS(player_choice, amount) #game function starts
            g_result['player_choice'] = player_choice

            if g_result["status"] == "tie":
                session['wager'] = g_result["amount"]
                return jsonify({
                    'status': 'tie',
                    'message': 'TIE',
                    'amount': g_result["amount"],
                    'cpu_choice': g_result['cpu_choice'],
                    'current_balance': current_user.current_balance
                })#wager for next round

            transaction_type = "payment" if g_result["status"] == "win" else "loss"
            transaction_amount = abs(g_result["amount"])
            description = f"{'Won Game' if g_result["status"] == "win" else 'Lost Game'}: RPS"

            rps_transresult = Account.transaction( #creates record of transaction
                current_user, #current logged in user
                transaction_type, #transaction type(payment or loss)
                transaction_amount, #amount lost or payed
                description
            )
            return jsonify({
                'status': g_result['status'],
                'message': g_result['message'],
                'amount': g_result['amount'],
                'cpu_choice': g_result['cpu_choice'],
                'current_balance': current_user.current_balance,
            })
        except Exception as e:
            (print(e))
    return render_template('RockPaperScissors.html', user=current_user)


@app.route('/purchase', methods=['POST'])
@login_required
def make_purchase():
    """ Handles making payment with credit in the store"""
    amount = int(request.form.get('amount', 0)) #gets price of item
    quantity = int(request.form.get('quantity', 1)) #gets how much of item
    description = request.form.get('description', 'Purchase')
    item_id = request.form.get('item_id')
    print(f"Received item_id: {item_id}, type: {type(item_id)}")

    total_amount = amount * quantity
    if current_user.current_balance + total_amount > current_user.credit_limit:
        flash("You dont have enough available credit to make this payment! Reduce it by playing a game!")
        return redirect(url_for('play_rps'))

    transaction_result = Account.transaction(
        current_user,
        "purchase",
        total_amount,
        description,
        )

    if item_id:
        item = Item.query.get(item_id)
        if item:
            current_user.items.append(item)
            db.session.commit()
            flash(f'Success!')
        else:
            flash('Item does not exist')


    return redirect(url_for('dashboard'))

@app.route("/store")
@login_required
def store():
    return render_template('store.html')



with app.app_context():
    #database initialization
    #db.drop_all()
    db.create_all()
    if Item.query.count() == 0:
        items = [
            Item(name="Cool Kat", price=100, quantity=1, image="static/cat.png", description="Cool Cat" ),
            Item(name="Cooler Kat", price=367, quantity=1, image="static/cat1.png", description="Cooler Cat"),
            Item(name="Coolest Kat", price=800, quantity=1, image="static/cat2.png", description="Coolest Cat"),
        ]
        db.session.add_all(items)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
