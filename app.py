from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置 SQLite 資料庫路徑
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystery_drinks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫
db = SQLAlchemy(app)

# 定義資料庫模型
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    toppings = db.Column(db.String(200), nullable=False)
    sugar_level = db.Column(db.String(50), nullable=False)
    ice_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Drink {self.title}>"

# 初始化資料庫（如果尚未建立）
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title')
    toppings = request.form.get('toppings')
    sugar_level = request.form.get('sugar_level')
    ice_level = request.form.get('ice_level')

    # 新增飲料到資料庫
    new_drink = Drink(
        title=title,
        toppings=toppings,
        sugar_level=sugar_level,
        ice_level=ice_level
    )
    db.session.add(new_drink)
    db.session.commit()

    return redirect(url_for('result'))

@app.route('/result')
def result():
    # 取得所有飲料資料
    drinks = Drink.query.all()
    return render_template('result.html', drinks=drinks)

if __name__ == '__main__':
    app.run(debug=True)
