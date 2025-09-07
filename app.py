from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
import json
from pathlib import Path
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

from models import Item, Category, User

_data_loaded = False

@app.before_request
def init_db_and_load_data():
    global _data_loaded
    db.create_all()
    if not _data_loaded:
        _data_loaded = True
        if Category.query.count() == 0:
            data = json.loads(Path("initial_data.json").read_text())
            for c in data["categories"]:
                cat = Category(name=c["name"], description=c.get("description"))
                db.session.add(cat)
            db.session.commit()
        if Item.query.count() == 0:
            data = json.loads(Path("initial_data.json").read_text())
            for i in data["items"]:
                cat = Category.query.filter_by(name=i["category"]).first()
                item = Item(name=i["name"], description=i.get("description"), category=cat)
                db.session.add(item)
            db.session.commit()

@app.route('/')
@login_required
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/view')
@login_required
def view_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('view_items.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    description = request.form.get('description')
    if name:
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/items/add', methods=['POST'])
def api_add_item():
    data = request.get_json()
    name = data.get('name')
    desc = data.get('description')
    item = Item(name=name, description=desc)
    db.session.add(item)
    db.session.commit()
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description
    }, 201

@app.route('/delete/<int:item_id>')
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if u and u.check_password(request.form['password']):
            login_user(u)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username taken")
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for('index'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)