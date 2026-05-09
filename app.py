from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'coffee_shop_secret_key'

# Mail Config - Render Environment Variables se aayega
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

@app.route('/')
def home():
    return render_templates('index.html')

@app.route('/about')
def about():
    return render_templates('about.html')

@app.route('/menu')
def menu():
    return render_templates('menu.html')

@app.route('/products')
def products():
    return render_templates('products.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        # Sirf mail bhejo, database nahi
        try:
            msg = Message('New Contact from Coffee Shop', 
                          recipients=[os.environ.get('MAIL_USERNAME')])
            msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            mail.send(msg)
            flash('Message Sent Successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            
    return render_templates('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
