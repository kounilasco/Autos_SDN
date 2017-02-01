from flask import render_template, flash, redirect,url_for
from app import app
from forms.forms import *
from entities.manager import *
TITLE = "Administration interface"
MENU = [
    {'list': 'CREATE NEW SLICE', 'link': 'createSlice'},
    {'list': 'DISCOVERY TOPOLOGY'},
    {'list': 'ABOUT', 'link': 'about'}
]
MENU1 = [
    {'list': 'SLICES CREATED', 'link': 'createSlice'},
    {'list': 'ACTIVES SLICES', 'link': 'about'}  
]

@app.route('/')
@app.route('/index')
def index():
    title = "Administration interface"
	m=Manager()
	if not m.is_running_fv():
		m.turnFvOn()
	s=Slice()
	s.setName("etudiant")	
	switch=m.getSwitchsDpid()
	sli=m.getAllSlices()
	f=m.getFlowSpace()
	i=m.getSliceInfo(s)
	user = {'nickname': 'Miguel'}  # fake user
	return render_template('index.html', dpids=switch,slices=sli,flow=f,tranche=i,title=title, menu=MENU, menu1=MENU1)

@app.route('/infoSlice/<string:nom>')
def infoSlice(nom):
	m=Manager()
	s=Slice()
	s.setName(nom)
	i =m.getSliceInfo(s)

	return render_template('vue.html',tranche=i)

@app.route('/about')
def about():
    """Create slice"""
    title = "About"
    return render_template('about.html', title=title, menu=MENU, menu1=MENU1)


@app.route('/createSlice', methods=['GET', 'POST'])
def createSlice():
	form = SliceForm()
	title = "Create slice"
	if form.validate_on_submit():
		m=Manager()
		s=Slice()
		s.setName(form.name.data)
		s.setIpAddr(form.IpAddr.data)
		s.setPort(form.port.data)
		s.setMail(form.mail.data)
		s.setPasswd(form.passwd.data)
		if m.createSlice(s):
			flash("Slice %s has been successfully created" % (s.getName()) )
			return redirect("/")
		else:
			flash("Slice %s can't be created. Please check your request and try again later ..."%(s.getName()))
			return redirect('/createSlice')
	 return render_template('create_slice.html', title=title, menu=MENU, menu1=MENU1)

@app.route('/createFlowspace', methods=['GET', 'POST'])
def createFlowspace():
	form = FlowspaceForm()
	if form.validate_on_submit():
		m=Manager()
		s=Flowspace()
		#s.setName(form.name.data)
		s.setDpid(form.dpid.data)
		s.setPriority(form.priority.data)
		s.setMatch(form.match.data)
		s.setSlicePerm(form.perm.data)
		if m.createSlice(s):
			flash("Slice %s has been successfully created" % (s.getName()) )
			return redirect("/")
		else:
			flash("Slice %s can't be created.  Please try again later ..."%(s.getName()))
			return redirect('/createSlice')
	return render_template('slice_new.html',form=form)

@app.route('/deleteSlice/<string:nom>/<int:conf>')
def deleteSlice(nom,conf):
	if conf==1:
		m=Manager()
		s=Slice()
		s.setName(nom)
		if m.deleteSlice(s):
			flash('Slice %s succesfully deleted'%(nom))
			return redirect(url_for('index'))
	return render_template('deleteSliceConf.html',nom=nom)

@app.route('/updateRequestSlice/<string:nom>')
def updateRequestSlice(nom):
	m=Manager()
	s=Slice()
	s.setName(nom)
	info=m.getSliceInfo(s)
	form=SliceEditForm()
	form.name.data=info["slice-name"]
	form.IpAddr.data=info["controller-url"].split(':')[1]
	form.port.data=info["controller-url"].split(':')[2]
	form.mail.data=info["admin-contact"]
	return render_template('slice_update.html',form=form)
	

@app.route('/updateSlice', methods=['GET','POST'])
def updateSlice():
	m=Manager()
	#info=m.getSliceInfo(nom)
	s=Slice()
	form=SliceEditForm()
	s.setName(form.name.data)
	s.setIpAddr(form.IpAddr.data)
	s.setPort(form.port.data)
	s.setMail(form.mail.data)
	s.setPasswd(form.passwd.data)
	if form.validate_on_submit():			
		
		if m.updateSlice(s):
			flash('Slice %s has been successfully updated'%(s.getName()))
			return redirect('/index')
		else:
			return redirect(url_for('updateRequestSlice',nom=s.getName()))
	else:
		return redirect(url_for('updateRequestSlice',nom=s.getName()))

@app.route('/login', methods=['GET', 'POST'])
def login():
	user={
	"login":"tuo",
	"password":"tuopass"
	}
	form = LoginForm()
	if form.validate_on_submit():
		if form.login.data == user["login"] and form.password.data == user["password"]:
			flash('Authentification successful with login : %s, password : %s' %
			      (form.login.data, str(form.password.data)))
			return redirect('/index')
		else:
			flash("Bad credentials")
			return redirect('/login')     
	return render_template('login.html', 
		           title='Sign In',
		           form=form)




