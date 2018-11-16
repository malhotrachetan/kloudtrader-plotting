from flask import *
from flask.templating import render_template
from flask_restplus import Api, Resource
import webbrowser


app = Flask(__name__)
api = Api(app)

@api.route('/plot/<string:chart_name>/<string:chart_type>/<y_data>/<data_name>')
class HelloWorld(Resource):
    def get(self,chart_name,chart_type,y_data,data_name):
        response=render_template('1.html',chart_name=chart_name,chart_type=chart_type,y_data=y_data,data_name=data_name)
        return Response(response)

if __name__ == '__main__':
    app.run(debug=True)