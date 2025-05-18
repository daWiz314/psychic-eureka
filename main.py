
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/success/<name>')
def success(name):
    return redirect('/greet/' + name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user), code=301)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)