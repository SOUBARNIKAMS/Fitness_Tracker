import smtplib
email="your email id"
def send_mail(receiver_email,subject,message):
    text=f"Subject :Workout Report from {subject}\n\n{message}\n\nStay motivated and keep up the good work with Fitness Corner!"
    server=smtplib.SMTP("host",port)
    server.starttls()
    server.login(email,"use your password")
    server.sendmail(email,receiver_email,text)
    print("Email sent to "+receiver_email)

