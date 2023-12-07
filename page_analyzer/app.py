from flask import (Flask, render_template, redirect, request,
flash, url_for, get_flashed_messages)
from validators import ValidationError
import logging

from .database import DataBase
from .utils import get_from_env, is_valid_url, to_normal

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = get_from_env('SECRET_KEY')


#db = DataBase(get_from_env('DATABASE_URL')) or
db_url = get_from_env("DATABASE_URL")
db = DataBase(db_url=db_url) if db_url else DataBase(host='localhost', port='5432',dbname='page-analyzer', user='zcmn', password='123009')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def show_urls():
    urls = db.get_all_urls()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def analize_url():
    url = to_normal(request.form.get('url'))
    if not is_valid_url(url):
        flash("Некорректный URL", 'danger')
        return render_template('index.html', messages=get_flashed_messages(with_categories=True))
    id = db.get_id_if_exist(url)
    if id is not None:
        flash("Страница уже добавлена", 'info')
        return redirect(url_for('show_url', id=id))
    _id = db.add_url(url)
    flash("Запись успешно добавлена", 'success')
    return redirect(url_for('show_url', id=_id))

@app.route('/urls/<id>')
def show_url(id):
    url = db.get_url(id)
    return render_template('show_url.html', url=url)
    
    
    
if __name__ == '__main__':
    app.run()
    