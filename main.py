from flask import Flask, render_template, redirect, request
import update

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':                    
        name = request.form['name']                                 # grabbing needed info from user
        router_ip = request.form['router_ip']
        username = request.form['username']
        password = request.form['password']

        update.db(name, router_ip, username, password)              # writing new line to db file

    return render_template('index.html')                            # reloading page

app.run(debug=True, host='0.0.0.0')