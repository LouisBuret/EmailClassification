from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        mail = request.form['mail']
        print('ok')
        return render_template('response.html', response = 'safe') # later email_classifier(mail)
    else:
        return render_template('start.html')

if __name__ == "__main__":
    app.run(debug=True, port=8081)