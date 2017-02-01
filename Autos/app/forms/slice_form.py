from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class SliceForm(Form):
	name = StringField('Name', validators=[DataRequired()])
	host = StringField('Host', validators=[DataRequired()])
	port = StringField('Port', validators=[DataRequired()])
	admin = StringField('Admin contact', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
