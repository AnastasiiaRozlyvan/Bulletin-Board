from flask import Blueprint
from flask import render_template

from models import Ad, Rubric


ads = Blueprint("ads", __name__, template_folder="templates")


@ads.route("/")
def index():
    ads = Ad.query.all()
    return render_template("ads/index.html", ads=ads)


@ads.route("/<slug>")
def ad_detail(slug):
    ad = Ad.query.filter(Ad.slug == slug).first()
    rubrics = ad.rubrics
    return render_template("ads/ad_detail.html", ad=ad, rubrics=rubrics)


@ads.route("/rubric/<slug>")
def rubric_detail(slug):
    rubric = Rubric.query.filter(Rubric.slug == slug).first()
    adv = rubric.ads
    return render_template("ads/rubric_detail.html", rubric=rubric, ads=adv)
