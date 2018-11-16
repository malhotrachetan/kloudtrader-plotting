from flask import *
import requests
import webbrowser


def plot(response):
    with app.test_request_context():
        return redirect(url_for('hello',response=response))


app = Flask(__name__)

def plot(response):
    with app.test_request_context():
        return redirect(url_for('hello',response=response))

    
@app.route('/hello')
def hello(response):
    try:
        response=request.args.get('response')
        return response
        
    except:
        response="Data not valid"
        return Response(response)



if __name__ == "__main__":
    app.run(debug=True,port=8080)
