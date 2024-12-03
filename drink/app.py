from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'  # 使用 SQLite 資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料庫模型
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    toppings = db.Column(db.String(200), nullable=False)
    sugar_level = db.Column(db.String(50), nullable=False)
    ice_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Drink {self.title}>"

# 主頁面，顯示所有神祕飲料
@app.route('/')
def index():
    drinks = Drink.query.all()
    return render_template('index.html', drinks=drinks)

# 新增神祕飲料
@app.route('/add', methods=['GET', 'POST'])
def add_drink():
    if request.method == 'POST':
        title = request.form['title']
        toppings = request.form['toppings']
        sugar_level = request.form['sugar_level']
        ice_level = request.form['ice_level']

        new_drink = Drink(title=title, toppings=toppings, sugar_level=sugar_level, ice_level=ice_level)
        db.session.add(new_drink)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_drink.html')

# 編輯神祕飲料
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_drink(id):
    drink = Drink.query.get(id)

    if request.method == 'POST':
        drink.title = request.form['title']
        drink.toppings = request.form['toppings']
        drink.sugar_level = request.form['sugar_level']
        drink.ice_level = request.form['ice_level']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_drink.html', drink=drink)

# 刪除神祕飲料
@app.route('/delete/<int:id>')
def delete_drink(id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    return redirect(url_for('index'))

# 確保應用程式上下文存在
def create_db():
    with app.app_context():
        db.create_all()  # 創建資料庫表格

if __name__ == '__main__':
    create_db()  # 這裡會創建資料庫表格
    app.run(debug=True, host='0.0.0.0', port=5001)  # 在 0.0.0.0:5001 上運行 Flask
