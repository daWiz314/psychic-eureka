
from flask import Flask, render_template
from index.blueprint_index import index_blueprint
from e_com_ref.e_com_ref import ecom_ref

# Main flask application
app = Flask(__name__)

# Main index blueprint
app.register_blueprint(index_blueprint, url_prefix='/index')

# E-commerce reference blueprint
app.register_blueprint(ecom_ref, url_prefix='/e_com_ref')

@app.route('/')
def hello_world():
    return render_template('index/index.html')

# Start app
if __name__ == '__main__':
    app.run(debug=True)