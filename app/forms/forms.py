from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField,EmailField,IntegerField,HiddenField,SelectField,FieldList,FormField
from wtforms.validators import DataRequired,NumberRange,IPAddress
from .. entities.manager import Manager

class LoginForm(Form):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

class SliceForm(Form):
	name = StringField('Name', validators=[DataRequired(message="this field is required")])
	IpAddr = StringField('Host', validators=[DataRequired(message="this field is required"),IPAddress('Not a IPAddress')])
	port = IntegerField('Port', validators=[DataRequired(message="this field is required"),NumberRange(min=1024,max=65536,message="Port number is not valid")])
	mail = EmailField('Admin contact', validators=[DataRequired(message="this field is required")])
	passwd = PasswordField('Password', validators=[DataRequired(message="this field is required")])

class SliceEditForm(Form):
	name = HiddenField('Name', validators=[])
	IpAddr = StringField('Host', validators=[DataRequired(message="this field is required"),IPAddress('Not a IPAddress')])
	port = IntegerField('Port', validators=[DataRequired(),NumberRange(min=1024,max=65536,message="Port number is not valid")])
	mail = EmailField('Admin contact', validators=[DataRequired(message="this field is required")])
	passwd = PasswordField('Password', validators=[DataRequired(message="this field is required")])


class PermForm(Form):
	valeur = SelectField('value',choices=[('7','high'), ('4', 'middle'),('3', 'low')])
	nom_slice = SelectField('slice name', validators=[DataRequired()])
	def set_nom_slice(self):
    		a=[]
    		for s in Manager().getAllSlices():
    			if s[0] !="fvadmin":
					a.append((s[0],s[0]))
			self.nom_slice.choices=a

class FlowspaceForm(Form):
	#name = StringField('Name', validators=[DataRequired()])
	dpid = SelectField('Host', validators=[])
	def set_dpid(self):
		a=[]
		switch=Manager().getSwitchsDpid()
		if type(switch)!=str:
			for k,v in switch.items():
					a.append((str(v),str(v)))
			self.dpid.choices=a
		else:
			self.dpid.choices=[('','NaN')]
	match = IntegerField('', validators=[DataRequired(),NumberRange(min=1,max=10,message="Port number is not valid")])
	perm = FormField(PermForm)
	priority = StringField('Priority', validators=[DataRequired()])

class FiltreForm(Form):
	nom_slice = SelectField('slice name', validators=[DataRequired()])
	def set_nom_slice(self):
			a=[]
			for s in Manager().getAllSlices():
				if s[0] !="fvadmin":
					a.append((s[0],s[0]))
			self.nom_slice.choices=a

