from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from mongo_util import MongoHandler

app = Flask(__name__)
bootstrap = Bootstrap(app)

mh = MongoHandler()
texts = mh.read_database('every_summary', 'fibre_db', '2019-4-15_2019-4-21').get('data', {})


@app.route('/')
def homepage():
    return render_template('homepage.html', texts=texts)


@app.route('/tech_prod/<item_id>')
def item_details(item_id):
    key = str(item_id) + '_txt'
    name = texts[key]['text'].split(' ')[0]
    return render_template('item_details.html', name=name, text=texts[key])


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/dashboard')
def dashboard():
    mh.download_pic('2019-4-15_2019-4-21_tech_product', 'E:/python/Fibre_NLP/frontend/static/images/week/tech_product.png','fibre_db')
    mh.download_pic('2019-4-15_2019-4-21_economy_market', 'E:/python/Fibre_NLP/frontend/static/images/week/economy_market.png', 'fibre_db')
    mh.download_pic('2019-4-15_2019-4-21_per', 'E:/python/Fibre_NLP/frontend/static/images/week/per.png', 'fibre_db')
    mh.download_pic('2019-4-15_2019-4-21_org', 'E:/python/Fibre_NLP/frontend/static/images/week/org.png', 'fibre_db')
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
