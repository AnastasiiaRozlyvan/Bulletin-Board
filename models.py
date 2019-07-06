from app import db
from datetime import datetime
import re


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, "-", s)


ad_rubrics = db.Table(
    "ad_rubrics",
    db.Column("ad_id", db.Integer, db.ForeignKey("ad.id")),
    db.Column("rubric_id", db.Integer, db.ForeignKey("rubric.id")),
)


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    rubrics = db.relationship("Rubric", secondary=ad_rubrics, backref=db.backref('ads'), lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Ad, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f"<Ad id: {self.id}, title: {self.title}>"


class Rubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Rubric, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f"<Rubric id: {self.id}, name {self.name}>"
