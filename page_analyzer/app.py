from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    request,
    url_for,
    get_flashed_messages,
)
import logging
import requests
from page_analyzer.database import DataBase
from page_analyzer.utils import get_from_env, is_valid_url, to_normal, get_seo_data

# logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

app = Flask(__name__)
app.config["SECRET_KEY"] = get_from_env("SECRET_KEY")
app.logger.setLevel(logging.INFO)
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers

db_url = get_from_env("DATABASE_URL")
db = (
    DataBase(db_url)
    if db_url
    else DataBase(
        host="localhost",
        port="5432",
        dbname="page-analyzer",
        user="zcmn",
        password="123009",
    )
)


@app.route("/")
def index():
    return render_template(
        "index.html", messages=get_flashed_messages(with_categories=True)
    )


@app.route("/urls")
def show_urls():
    urls = db.get_all_urls()
    return render_template("urls.html", urls=urls)


@app.post("/urls")
def process_url():
    url = to_normal(request.form.get("url"))
    if not is_valid_url(url):
        flash("Некорректный URL", "danger")
        return redirect(url_for("index")), 302

    id = db.get_url_id_if_exist(url)
    if id is not None:
        flash("Страница уже добавлена", "info")
        return redirect(url_for("show_url", id=id))
    id = db.add_to_urls(url)
    flash("Запись успешно добавлена", "success")
    return redirect(url_for("show_url", id=id)), 302


@app.route("/urls/<int:id>")
def show_url(id):
    url = db.get_url(id)
    if not url:
        return render_template("404.html")
    checks = db.get_all_checks_by_id(id)
    return render_template(
        "show_url.html",
        url=url,
        checks=checks,
        messages=get_flashed_messages(with_categories=True),
    )


@app.post("/urls/<int:id>/checks")
def check_url(id):
    try:
        url = db.get_url(id).get("name")
        response = requests.get(url)
        code = response.status_code
        if code != 200:
            raise
        seo_data = get_seo_data(response.text)
        db.add_to_checks(url_id=id, code=code, seo_data=seo_data)
        flash("Страница успешно проверена", "success")
        return redirect(url_for("show_url", id=id))
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("show_url", id=id)), 301


@app.errorhandler(404)
def error_404(err):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(err):
    return render_template("505.html"), 500


if __name__ == "__main__":
    try:
        app.run()
    finally:
        db.close()
