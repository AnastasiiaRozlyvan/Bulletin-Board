from flask import Blueprint
from flask import render_template

ads = Blueprint("ads", __name__, template_folder="templates")


@ads.route('/')
def index():
    return render_template("ads/index.html")
