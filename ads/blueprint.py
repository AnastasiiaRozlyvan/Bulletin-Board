from flask import Blueprint
from flask import render_template

from models import Ad


ads = Blueprint("ads", __name__, template_folder="templates")


@ads.route("/")
def index():
    ads = Ad.query.all()
    return render_template("ads/index.html", ads=ads)
