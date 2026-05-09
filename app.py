from flask import Flask, send_from_directory, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# ================= GMAIL =================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

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

    # MYSQL CODE COMMENT KAR DIYA - Render pe nahi chalega
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO contacts(name,email,phone) VALUES(%s,%s,%s)", (name, email, phone))
    # mysql.connection.commit()
    # cur.close()

    # SEND EMAIL
    msg = Message(
        'New Contact Message',
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']]  # Khud ko mail jayega
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
