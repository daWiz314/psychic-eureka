
from flask import Flask
from index.blueprint_index import index_blueprint
from e_com_ref.e_com_ref import ecom_ref

# Main flask application
app = Flask(__name__)

# Main index blueprint
app.register_blueprint(index_blueprint)

# E-commerce reference blueprint
app.register_blueprint(ecom_ref, url_prefix='/e_com_ref')

# Start app
if __name__ == '__main__':
    app.run(debug=True)