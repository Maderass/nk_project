from flask import Flask, request, render_template, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# SMTP Konfigürasyonu
SMTP_SERVER = 'smtp.gmail.com'  # Gmail için
SMTP_PORT = 587
SMTP_USER = 'nubar.kostekoglu@gmail.com'  # Buraya kendi e-posta adresini yaz
SMTP_PASSWORD = 'oyyo vjmi njqr leqw'  # Buraya Gmail uygulama şifreni yaz
RECIPIENT_EMAIL = 'nubar.kostekoglu@gmail.com'  # Buraya e-postaları almak istediğin adresi yaz

# 📌 Ana Sayfa Route
@app.route('/')
def home():
    return render_template('index.html')

# 📌 Form Gönderme Route
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    company = request.form.get('company', '')  # Company zorunlu değil, boş olabilir
    email = request.form.get('email')
    message = request.form.get('message')

    # 📌 Email ve Message alanları zorunlu
    if not email or not message:
        return render_template('index.html', error="Email and Message fields are required!")

    try:
        # 📌 E-Posta Gönderme İşlemi
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f'New Contact Form Submission from {name}'
        email_body = f"Name: {name}\nCompany: {company}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(email_body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, RECIPIENT_EMAIL, msg.as_string())
        server.quit()

        return render_template('index.html', success="Your message has been sent successfully!")

    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

# 📌 Flask Uygulamasını Başlat
if __name__ == '__main__':
    app.run(debug=True)

