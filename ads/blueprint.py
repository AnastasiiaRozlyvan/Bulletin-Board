from flask import Blueprint
from flask import render_template

from models import Ad


ads = Blueprint("ads", __name__, template_folder="templates")


@ads.route("/")
def index():
    ads = Ad.query.all()
    return render_template("ads/index.html", ads=ads)


@ads.route('/<slug>')
def ad_detail(slug):
    ad = Ad.query.filter(Ad.slug == slug).first()
    return render_template('ads/ad_detail.html', ad=ad)
