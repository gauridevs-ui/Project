from flask import Flask, send_from_directory, request
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# ================= MYSQL =================

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'coffee_shop'

mysql = MySQL(app)

# ================= GMAIL =================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'gaurichauhan411@gmail.com'
app.config['MAIL_PASSWORD'] = 'uamjcxofrcgjkewj'

mail = Mail(app)

# ================= HTML PAGES =================

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/contact.html')
def contactpage():
    return send_from_directory('.', 'contact.html')

@app.route('/about.html')
def aboutpage():
    return send_from_directory('.', 'about.html')

@app.route('/menu.html')
def menupage():
    return send_from_directory('.', 'menu.html')

@app.route('/products.html')
def productpage():
    return send_from_directory('.', 'products.html')

# ================= CONTACT FORM =================

@app.route('/contact', methods=['POST'])
def contact():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    # SAVE TO DATABASE

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO contacts(name,email,phone) VALUES(%s,%s,%s)",
        (name, email, phone)
    )

    mysql.connection.commit()
    cur.close()

    # SEND EMAIL

    msg = Message(
        'New Contact Message',
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']]
    )

    msg.body = f'''
    New Customer Contact

    Name: {name}
    Email: {email}
    Phone: {phone}
    '''

    mail.send(msg)

    return "Message Sent Successfully!"

if __name__ == '__main__':
    app.run(debug=True)