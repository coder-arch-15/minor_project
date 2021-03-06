from flask import Blueprint, flash
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import new_user_credentials as nuc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from models import individual,labs,doctor
from flask_mail import Mail, Message

indi_dashboard_bp = Blueprint('indi_dashboard_bp', __name__)


mail = Mail(app)

db = SQLAlchemy(app)
db.create_all()
SQLALCHEMY_TRACK_MODIFICATIONS = False

#######do not  touch this code upto next comment
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id,endpoint='user'):
	temp = doctor.query.get(user_id)
	if temp:
		return temp
	else:
		return individual.query.get(user_id)
	
################upto here

@indi_dashboard_bp.route('/indi/dashboard') 		############Dashboard for individual
@login_required
def indi_dashboard():
	return render_template('indi_dashboard.html', cu = current_user)


@indi_dashboard_bp.route('/indi/dashboard/settings')		###########Dashboard settings for individual
@login_required
def dashboard_settings():
	return render_template('indi_settings.html', )


@indi_dashboard_bp.route('/dashboard/settings/update', methods = ['GET','POST'])		###########Dashboard settings update  button route for individual
@login_required
def dashboard_settings_update():
	if request.method == 'POST':
		try:
			current_user.fname = request.form['fname']
			current_user.lname = request.form['lname']
			current_user.mob = request.form['mob']
			current_user.dob = str(request.form['dob'])
			if(request.form.get('gender')):
				current_user.gender = request.form['gender']
			if(request.form.get('blood')):
				current_user.blood = request.form['blood']
			if(request.form.get('state')):
				current_user.state = request.form['state']
			if(request.form.get('city')):
				current_user.city = request.form['city']
			current_user.district = request.form['district']
			current_user.pin = request.form['pincode']
			current_user.addr1=request.form['add1']
			current_user.addr2=request.form['add2']
			if(request.form.get('upd_pasw')):
				current_user.pasw = generate_password_hash(request.form['upd_pasw'])

			message = "Hi "+current_user.fname+" " +current_user.lname+"\nYour account information has been updated on National Digital Health Portal."
			msg = Message('NDHP Registration', sender = 'ndhp.gov@gmail.com', recipients = [current_user.email])
			msg.body = message
			db.session.merge(current_user)
			db.session.commit()
			mail.send(msg)
			flash("Changes saved successfully!")
			return redirect(url_for('indi_dashboard_bp.dashboard_settings'))

		except Ecurrent_userception as e:
			flash(e)
			return redirect(url_for('indi_dashboard_bp.dashboard_settings'))



@indi_dashboard_bp.route('/indi/dashboard/search_dr')		###########Dashboard doctor searcch
@login_required
def dashboard_search_dr():
	return render_template('indi_search_dr.html')



@indi_dashboard_bp.route('/indi/dashboard/search_labs')		###########Dashboard labs searcch
@login_required
def dashboard_search_lab():
	return render_template('indi_search_labs.html')



@indi_dashboard_bp.route('/indi/dashboard/search_dr/results', methods= ['GET','POST'])		###########Dashboard doctor searcch results
@login_required
def dashboard_search_dr_results():
	if request.method == 'POST':
		try:
			attr = request.form['attribute']
			value = request.form['value']
			if(attr=="name"):
				temp=doctor.query.filter(doctor.fname.ilike('%value%'))
				# if (!temp):
				# 	temp=doctor.query.filter(doctor.lname.ilike('%value%'))
			elif(attr=="city"):
				temp=query.filter(doctor.city.ilike('%value%'))
			else:
				temp=query.filter(doctor.Specialization.ilike('%value%'))
			if temp:
				return render_template('indi_search_dr.html', temp_obj=temp)

		except Exception as e:
			flash(e)
			return redirect(url_for('indi_dashboard_bp.dashboard_search_dr'))



@indi_dashboard_bp.route('/indi/dashboard/search_lab/results' , methods= ['GET','POST'])		###########Dashboard labs searcch results
@login_required
def dashboard_search_lab_results():
	if request.method == 'POST':
		try:
			attr = request.form['attribute']
			value = request.form['value']
			if(attr=="name"):
				temp=labs.query.filter(labs.labname.ilike('%value%')).all
			else:
				temp=labs.query.filter(labs.city.ilike('%value%'))
			if temp:
				return render_template('indi_search_labs.html', temp_obj=temp)

		except Exception as e:
			flash(e)
			return redirect(url_for('indi_dashboard_bp.dashboard_search_lab'))
