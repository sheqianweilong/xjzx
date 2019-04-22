from flask import Blueprint, render_template

news_blueprint = Blueprint('news', __name__, url_prefix="")


@news_blueprint.route('/', methods=('GET', 'POST'))
def index():
    return render_template('news/index.html')
