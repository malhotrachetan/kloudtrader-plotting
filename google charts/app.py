from flask import *
from kloudtrader.equities.data import *
import random

plotting_server = Flask(__name__)

@plotting_server.route('/')
def home():
    return render_template('1.html')

if __name__ == "__main__":
    plotting_server.run(debug=True)
