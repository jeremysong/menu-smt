import os

from flask import Flask
from flask import render_template
from flask import request
import json
from z3 import sat, BoolVal
from . import menu_solver


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def input():
        return render_template('index.html', name="Jeremy")

    @app.route('/solve', methods=['POST'])
    def solve():
        data = request.json
        print("data", data)
        s = menu_solver.MenuSolver().solve(max_price=data['max_price'], min_price=data['min_price'],
            max_count=data['max_count'], min_count=data['min_count'])
        
        # print(s.check())

        if (s.check() == sat):
            # process_model(s.model())
            response = json.dumps({
                'sat': True,
                'menu': process_model(s.model())
            })
        else:
            response = json.dumps({
                'sat': False
            })

        return response

    def process_model(model):
        return [m.name() for m in model if model[m] == BoolVal(True)]

    return app