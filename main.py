
from flask import Flask, redirect
from index.routes import setup_blueprint as index_set_up
from index.routes import index_blueprint
from e_com_ref.e_com_ref import ecom_ref

# Main flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for CSRF protection

# Main index blueprint
app.register_blueprint(index_blueprint, url_prefix='/index')
# Set up the database
index_set_up()

# E-commerce reference blueprint
app.register_blueprint(ecom_ref, url_prefix='/e_com_ref')

@app.route('/')
def hello_world():
    return redirect('/index')

# Start app
if __name__ == '__main__':
    app.run(debug=True)