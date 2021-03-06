from flask import Blueprint, flash
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import new_user_credentials as nuc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from models import individual,labs,doctor
from flask_mail import Mail, Message

register_bp = Blueprint('register_bp', __name__)

login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)

db = SQLAlchemy(app)
db.create_all()
SQLALCHEMY_TRACK_MODIFICATIONS = False

@login_manager.user_loader
def load_user(user_id):
	return individual.query.get(user_id)


@register_bp.route('/individual_form_submit', methods = ['GET' , 'POST'])
def sub():
	if request.method == 'POST':
		try:
			fname = request.form['fname']
			lname = request.form['lname']
			email = request.form['email']
			mob = request.form['mob']
			dob = str(request.form['dob'])
			gender = request.form['gender']
			aadhaar = request.form['aadhaar']
			blood = request.form['blood']
			state = request.form['state']
			city = request.form['city']
			district = request.form['district']
			pin = request.form['pincode']
			addr1=request.form['add1']
			addr2=request.form['add2']

			nu = nuc.New_user(city, dob)
			h_id, pasw = nu.create_user()
			temp = individual(id=h_id, pasw=generate_password_hash(pasw) ,
				fname=fname, lname =lname, email=email, mob =mob, dob=dob,gender=gender,aadhaar=aadhaar, blood=blood,
				state=state, city=city, district=district, pin=pin, addr1=addr1, addr2=addr2 )
			temp.send_pdf_indi()
			db.session.add(temp)
			db.session.commit()

			thank_msg = "Record successfully added"
			message = "Hi "+fname+" " +lname+"\nThank You for registering with National Digital Health Portal.\nYour login credentials are - \nUsername - " + h_id + "\nPassword - " + pasw
			msg = Message('NDHP Registration', sender = 'ndhp.gov@gmail.com', recipients = [email])
			msg.body = message
			path = "C:\\minor_project\\static\\"
			with app.open_resource("GFG.pdf") as fp:
				msg.attach("GFG.pdf", "file/pdf", fp.read())
			mail.send(msg)
			return render_template('thank.html',namee=thank_msg)

		except Exception as e:
			msg = e
			return render_template('thank.html',namee=msg)

#############################################################################      doctor
@register_bp.route('/doctor_form_submit', methods = ['GET' , 'POST'])
def doctor_reg_sub():
	if request.method == 'POST':
		try:
			indi_id = request.form['uid']
			fname = request.form['fname']
			lname = request.form['lname']
			email = request.form['email']
			mob = request.form['mob']
			dob = str(request.form['dob'])
			gender = request.form['gender']
			regnum = request.form['regnum']
			Specialization = request.form['Specialization']
			##add3=request.form['add3']  Please remove this
			state = request.form['state']
			city = request.form['city']
			district = request.form['district']
			pin = request.form['pincode']
			addr1=request.form['add1']
			addr2=request.form['add2']

			h_id="D"+indi_id[1:]
			y,m,d = dob.split("-")
			pasw = d+m+y

			temp = doctor(id=h_id, pasw=generate_password_hash(pasw) ,
				fname=fname, lname =lname, email=email, mob =mob, dob=dob,gender=gender,regnum=regnum, Specialization=Specialization,
				state=state, city=city, district=district, pin=pin, addr1=addr1, addr2=addr2 )

			db.session.add(temp)
			db.session.commit()

			thank_msg = "Record successfully added"
			message = "Hi "+fname+" " +lname+"\nThank You for registering with National Digital Health Portal.\nYour login credentials are - \nUsername - " + h_id + "\nPassword - " + pasw
			msg = Message('NDHP Registration', sender = 'ndhp.gov@gmail.com', recipients = [email])
			msg.body = message
			path = "C:\\minor_project\\static\\"
			#with app.open_resource("GFG.pdf") as fp:
				#msg.attach("GFG.pdf", "file/pdf", fp.read())
			mail.send(msg)
			return render_template('thank.html',namee=thank_msg)

		except Exception as e:
			msg = e
			return render_template('thank.html',namee=msg)
###########################################################################

@register_bp.route('/labs_form_submit', methods = ['GET' , 'POST'])
def lab_form_sub():
	if request.method == 'POST':
		try:
			lab_name = request.form['lab_name']
			tests_avlbl = request.form['tests_avlbl']
			email = request.form['email']
			mob = request.form['mob']
			licenseno = request.form['licenseno']
			owner_name=request.form['owner_name']
			state = request.form['state']
			city = request.form['city']
			district = request.form['district']
			pin = request.form['pincode']
			addr1=request.form['add1']
			addr2=request.form['add2']

			#nu = lc.Labs(city, dob)
			nu = nuc.New_user(city, owner_name)
			h_id, pasw = nu.create_user()
			temp = labs(id = id, licenseno=licenseno, pasw=generate_password_hash(pasw) ,
				labname=lab_name, tests_avlbl =tests_avlbl, email=email, mob =mob, owner_name=owner_name,
				state=state, city=city, district=district, pin=pin, addr1=addr1, addr2=addr2 )
			db.session.add(temp)
			db.session.commit()

			thank_msg = "Record successfully added"
			message = "Hi "+lab_name+"\nThank You for registering with National Digital Health Portal.\nYour login credentials are - \nUsername - " + h_id + "\nPassword - " + pasw
			msg = Message('NDHP Registration', sender = 'ndhp.gov@gmail.com', recipients = [email])
			msg.body = message
			path = "C:\\minor_project\\static\\"
			with app.open_resource("GFG.pdf") as fp:
				msg.attach("GFG.pdf", "file/pdf", fp.read())
			mail.send(msg)
			return render_template('thank.html',namee=thank_msg)

		except Exception as e:
			msg = e
			return render_template('thank.html',namee=msg)
			mail.send(msg)
			return render_template('thank.html',namee=thank_msg)



@register_bp.route('/doctor_indi_check', methods = ['GET' , 'POST'])
def doctor_indi_check():
	if request.method == 'POST':
		try:
			indi_id = request.form['indi']
			if(indi_id[0]=="I"):
					temp = individual.query.filter_by(id = indi_id).first()
					if temp:
						return render_template('doctor_register.html', temp_obj=temp)
					else:
						msg = "User not registered"
						flash("User not registered!")
						return redirect(url_for('register_bp.doctor_indi_check'))

			else:
				msg = "Invalid User ID!"
				flash("Invalid User ID!")
				return redirect(url_for('register_bp.doctor_indi_check'))

		except Exception as e:
			flash(e)
			return render_template('doctor_indi_check.html')
			#msg = "Error in insert operation"
