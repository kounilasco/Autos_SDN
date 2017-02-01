from flask import render_template, flash, redirect,url_for
from app import app
from forms.forms import *
from entities.manager import Manager
from entities.slice import Slice,Flowspace
TITLE = "Administration interface"
MENU = [
    {'list': 'CREATE NEW SLICE', 'link': '/createSlice'},
	{'list': 'CREATE FLOWSPACE', 'link': '/createFlowspace'} ,
    {'list': 'DISCOVERY TOPOLOGY'},
    {'list': 'ABOUT', 'link': '/about'}
]
MENU1 = [
    {'list': ' CREATED SLICES', 'link': '/createdSlice'},
	{'list': 'CREATED FLOWSPACES', 'link': '/listFlowspaces'},
    #{'list': 'ACTIVES SLICES', 'link': 'about'},
    {'list': 'CONNECTED SWITCHS', 'link': '/connectedSwitchs'}	
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

@app.route('/createdSlice')
def createdSlice():
    m=Manager()
    s=m.getAllSlices()
    return render_template('slice_created.html',slices=s, menu=MENU, menu1=MENU1)

@app.route('/connectedSwitchs')
def connectedSwitchs():
    m=Manager()
    s=m.getSwitchsDpid()
    return render_template('switchs_list.html',dpids=s, menu=MENU, menu1=MENU1)

@app.route('/listFlowspaces',methods=['GET','POST'])
def listFlowspaces():
	form=FiltreForm()
	form.set_nom_slice()
	m=Manager()
	f=m.getFlowSpace()
	if form.validate_on_submit():
		resultat=m.getFlowSpace(form.nom_slice.data)
		return render_template('flows_list.html',flows=resultat,form=form, menu=MENU, menu1=MENU1)
	return render_template('flows_list.html',flows=f,form=form, menu=MENU, menu1=MENU1)

@app.route('/infoSlice/<string:nom>')
def infoSlice(nom):
	m=Manager()
	s=Slice()
	s.setName(nom)
	i =m.getSliceInfo(s)

	return render_template('vue.html',tranche=i, menu=MENU, menu1=MENU1)

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
            r=m.createSlice(s)
            if r:
                flash('Slice "%s" has been successfully created' % (s.getName()) )
                return redirect("/createFlowspace")
            else:
                flash("Slice %s can't be created. Please check your request and try again later ..."%(s.getName()))
                return redirect('/createSlice',r=r)
        return render_template('create_slice.html',form=form, title=title, menu=MENU, menu1=MENU1)

@app.route('/createFlowspace', methods=['GET', 'POST'])
def createFlowspace():
	form = FlowspaceForm()
	form.perm.set_nom_slice()
	form.set_dpid()
	if form.validate_on_submit():
		m=Manager()
		f=Flowspace()
		#s.setName(form.name.data)
		f.setDpid(form.dpid.data)
		f.setPriority(form.priority.data)
		f.setMatch(form.match.data)
		p={}
		p[form.perm.nom_slice.data]=form.perm.valeur.data
		f.setSlicePerm(p)
		f.setName()
		if m.createFlowSpace(f):
			flash("Flowspace %s has been successfully created." % (f.getName()) )
			return redirect("/")
		else:
			flash("Flowspace %s can't be created. Probably already exist ! Please check and try again later ..."%(f.getName()))
			return redirect('/createFlowspace')
	return render_template('flowspace_new.html',form=form, menu=MENU, menu1=MENU1)

@app.route('/deleteFlowspace/<string:nom>/<int:response>')
def deleteFlowspace(nom,response):
    	if response==1:
			m=Manager()
			f=Flowspace()
			f.name=nom
			if m.deleteFlowspace(f):
				flash('Flowspace %s succesfully deleted'%(nom))
				return redirect(url_for('listFlowspaces'))
			else:
				flash('impossible de supprimer %s'%(nom))
				return redirect(url_for('listFlowspaces'))
    	else:
			return render_template('confirmation.html',Nom=nom, menu=MENU, menu1=MENU1)

@app.route('/showFlowspace/<string:nom>')
def showFlowspace(nom):
			m=Manager()
			f=Flowspace()
			f.name=nom
			resultat=m.showFlowSpace(f)
			return render_template('showFlowspace.html',resultat=resultat, menu=MENU, menu1=MENU1)

@app.route('/deleteSlice/<string:nom>/<int:conf>')
def deleteSlice(nom,conf):
	if conf==1:
		m=Manager()
		s=Slice()
		s.setName(nom)
		if m.deleteSlice(s):
			flash('Slice %s succesfully deleted'%(nom))
			return redirect(url_for('index'))
	return render_template('deleteSliceConf.html',nom=nom, menu=MENU, menu1=MENU1)

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
	return render_template('slice_update.html',form=form, menu=MENU, menu1=MENU1)
	

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
                   
@app.route('/refreshFv')
def refresFv():
	m=Manager()
	m.restartFv()
	if m.restartFv():
		flash('Sorry try again later !')
		
	else :
		flash('Flowvisor is working !')

	return redirect(url_for('index'))



