from flask import Flask
from flask import redirect, url_for, request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import Security
from flask_security import current_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_security import SQLAlchemyUserDatastore


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


from models import *


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login", next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class AdAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'rubrics']


class RubricAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'ads']


admin = Admin(app, "B_board", url="/", index_view=HomeAdminView(name="Home"))
admin.add_view(AdAdminView(Ad, db.session))
admin.add_view(RubricAdminView(Rubric, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
