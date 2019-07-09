from app import db
from datetime import datetime
import re


from flask_security import UserMixin, RoleMixin


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, "-", str(s))


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
    created = db.Column(db.DateTime, default=datetime.now)

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    rubrics = db.relationship(
        "Rubric", secondary=ad_rubrics, backref=db.backref("ads"), lazy="dynamic"
    )

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
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"{self.name}"


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
