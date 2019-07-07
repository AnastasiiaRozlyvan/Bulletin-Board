from wtforms import Form, StringField, TextAreaField


class AdForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
