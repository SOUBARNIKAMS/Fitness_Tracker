from flask import Flask, render_template, request, redirect, url_for, Response, session
import emailsend
import pose
import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
secret_key = os.urandom(24)
choice = 1
emailID = ""
performed = False
app = Flask(__name__)
app.secret_key = secret_key

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'emailID' in session and 'choice' in session:
        return redirect(url_for("emailing"))
    if request.method == "POST":
        emailID = request.form["email"]
        choice = request.form["option"]
        session['emailID'] = emailID
        session['choice'] = choice
        return redirect(url_for("video"))
    return render_template('index.html')

@app.route('/video')
def video():
    try:
        if 'choice' in session:
            return Response(pose.capture(session['choice']), mimetype='multipart/x-mixed-replace;boundary=frame')
        else:
            return "Error: Choice not found in session"
    except Exception as e:
        print(f"Error in /video route: {str(e)}")
        return "Error occurred"

@app.route('/emailing')
def emailing():
    try:
        if 'emailID' in session and 'choice' in session:
            emailID = session['emailID']
            msg = pose.msg
            emailsend.send_mail(emailID, "Fitness Corner Participant", msg)
            session.pop('emailID', None)
            session.pop('choice', None)
            return redirect(url_for("index"))
        else:
            return "Error: EmailID or Choice not found in session"
    except Exception as e:
        print(f"Error in /emailing route: {str(e)}")
        return "Error occurred"

if __name__ == '__main__':
    app.run(debug=True)
