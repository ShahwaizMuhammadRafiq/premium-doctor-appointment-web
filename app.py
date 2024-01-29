# We Will Use Flask Module For Connection Between Html and Css 
from flask import *
from flask_bcrypt import *
import secrets
from twilio.rest import *
import logging

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secrets.token_hex(16)

logging.basicConfig(level=logging.DEBUG)

tokencounter = 0

# We Will Use Twilio For Sending Whatsapp Message
account_sid = 'ACbfe4b491134a1a3279edcc28fb8683df'
auth_token = 'ce991d2a214feb183d50f44ee9ca91d6'
twiliophonenumber = 'whatsapp:+14155238886'

client = Client(account_sid, auth_token, twiliophonenumber)

def send_whatsapp_message(phonenumber, message_body):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twiliophonenumber}",
            to=f"whatsapp:{phonenumber}",
            body=message_body
        )
        print(f"WhatsApp message sent to {phonenumber} with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")


#Guess everyone as user
def getuserrole(username):
    return 'User'

# route for log out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# request before request
@app.before_request
def before_request():
    if 'appointments' not in session:
        session['appointments'] = {}




# it will link home html html through app.route
@app.route('/')
def home():
    username = session.get('username')
    user_role = getuserrole(username) if username else None
    return render_template('home.html', username=username, user_role=user_role)



# it will link bookappointment html through app.route
@app.route('/bookappointment', methods=['GET', 'POST'])
def bookappointment():
    global tokencounter

    logging.debug('Entering bookappointment route')

    if request.method == 'POST':
        logging.debug('Handling POST request for booking appointment')

        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        doctor = request.form['doctor']
        phonenumber = request.form['phone_number']

        logging.debug(f'Form data: name={name}, date={date}, time={time}, doctor={doctor}, phonenumber={phonenumber}')

        tokencounter += 1
        session['token'] = tokencounter

        # Check appointment is in session or not
        if 'appointments' not in session:
            session['appointments'] = {}

        # Append appointment in new appointment
        new_appointment = {
            'name': name,
            'date': date,
            'time': time,
            'doctor': doctor,
            'phonenumber': phonenumber,
            'token': tokencounter
        }

        session['appointments'][tokencounter] = new_appointment

        logging.debug(f'Form data: name={name}, date={date}, time={time}, doctor={doctor}, phonenumber={phonenumber}')


        # Send a WhatsApp message to the provided phone number
        send_whatsapp_message(phonenumber, f"Your appointment is booked.name={name}, date={date}, time={time}, doctor={doctor}, phonenumber={phonenumber}' Token: {tokencounter}")
        logging.debug("Appointments after booking: %s", session['appointments'])

        print("Session contents after booking:", session)

        return redirect(url_for('bookappointment'))


    doctors = {
        'Dr. Shahwaiz': 'Cardiology',
        'Dr. Sufiyan': 'Pediatrics',
        'Dr. Sarmad': 'Internal Medicine',
        'Dr. Farzam': 'Neurologist'
    }

    logging.debug("Rendering bookappointment template")
    return render_template('appointment.html', appointments=session.get('appointments', {}).values(), doctors=doctors)



# it will link admin appointment html through app.route
@app.route('/adminappointments')
def adminappointments():
    if 'username' not in session or session['username'] != 'admin':
        abort(403) 


    appointments = session.get('appointments', {})
    

    print("Appointments in admin panel:", appointments)
    print("Session contents in adminappointments:", session)

 
    return render_template('adminappointments.html', appointments=appointments.values())


@app.route('/admineditappointment/<int:token>', methods=['GET', 'POST'])
def admineditappointment(token):
    if request.method == 'POST':
        updateappointment(token, request.form)
        return redirect(url_for('adminappointments'))
    else:
        appointment = getappointment(token)
        print("Appointment data for editing:", appointment)
        doctors = {
            'Dr. Shahwaiz': 'Cardiology',
            'Dr. Sufiyan': 'Pediatrics',
            'Dr. Sarmad': 'Internal Medicine',
            'Dr. Farzam': 'Neurologist'
        }
        return render_template('admineditappointment.html', appointment=appointment, doctors=doctors)

@app.route('/adminremoveappointment/<int:token>', methods=['GET', 'POST'])
def adminremoveappointment(token):
    removeappointment(token)
    print("Appointments after removal:", session['appointments'])
    return redirect(url_for('adminappointments'))

# it will link book html through app.route
@app.route('/about')
def about():
    return render_template('about.html')

# it will link login html through app.route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        if username == 'admin' and password == 'admin':
            
            session['username'] = username

            
            if username == 'admin':
                return redirect(url_for('adminappointments'))
            else:
                return redirect(url_for('home'))

    return render_template('login.html')

# it will update the appointment in the session in admin 
def updateappointment(index, form_data):
    if index in session['appointments']:
        appointment = session['appointments'][index]
        appointment.update({
            'name': form_data['name'],
            'date': form_data['date'],
            'time': form_data['time'],
            'doctor': form_data['doctor'],
            'phonenumber': form_data['phonenumber']
        })

def getappointment(token):
    appointments = session.get('appointments', {})
    appointment = appointments.get(token)

    if appointment is None:
        abort(404)

    appointment['token'] = token
    return appointment

# it will remove the appointment in the session in admin 
def removeappointment(token):
    if token in session['appointments']:
        session['appointments'].pop(token)


        if not session['appointments']:
            session['appointments'] = {}

# it will link contact html through app.route
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

#This we use to check flask and debug
if __name__ == '__main__':
    app.run(debug=True)