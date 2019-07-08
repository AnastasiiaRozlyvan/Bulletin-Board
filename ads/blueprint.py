from flask import Blueprint
from flask import render_template

from models import Ad, Rubric
from .forms import AdForm
from app import db

from flask import request
from flask import redirect
from flask import url_for


ads = Blueprint("ads", __name__, template_folder="templates")


@ads.route('/create', methods=['POST', 'GET'])
def create_ad():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            ad = Ad(title=title, body=body)
            db.session.add(ad)
            db.session.commit()
        except:
            print("Unsuccessfully")

        return redirect(url_for('ads.index'))

    form = AdForm()
    return render_template('ads/create_ad.html', form=form)


@ads.route("/")
def index():
    q = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        adv = Ad.query.filter(Ad.title.contains(q) | Ad.body.contains(q))
    else:
        adv = Ad.query.order_by(Ad.created.desc())
    pages = adv.paginate(page=page, per_page=5)

    return render_template("ads/index.html", pages=pages)


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

