from flask import Flask, make_response, request, jsonify
from flask_cors import CORS

from marker import Marker
from marker.utils import config
from marker.utils import pushd
from marker.utils.marksheet import Marksheet

import argparse
import os

############################# Init Flask ######################################

app = Flask(__name__)
CORS(app)

############################# Global Variables ################################

MARKER = None
ARGS = []

###############################################################################


@app.route('/')
def route_home():
    message = { 'message': 'Everything is OK here :)' }
    return make_response(message, 200)


@app.route('/config', methods=['GET', 'POST'])
def route_config():
    if request.method == 'GET':
        return MARKER.cfg
    else:
        return make_response("This isn't implemented yet :(", 400)

@app.route('/results/')
def route_results():
    data = MARKER.getMarksheet().data
    if data is None:
        return make_response({"error": "Marksheet was not found"}, 401)
    response = [ {'username': u, 'marks': m} for u, m in data.items() ]
    return jsonify(response)


@app.route('/results/<string:student_id>', methods=['GET', 'POST'])
def route_single_result(student_id): 
    student_dir = MARKER.getStudentDir(student_id)
    if student_dir is None:
        return make_response({"error": "Student directory not found"}, 401)

    json_path = f'{student_dir}/results.json'
    if not os.path.isfile(json_path):
        return make_response({"error": "results.json not found"}, 401)

    return open(json_path).read()


@app.route('/stats')
def route_stats():
    return MARKER.stats(False, [])


@app.route('/<path:u_path>')
def route_catch_all(u_path):
    return "Why are you here?"


def main():
    top_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    top_parser.add_argument("-d","--assgn_dir", default=os.getcwd(), help="Marking directory (Default: current)")
    top_parser.add_argument("-c","--config", default=None, help="Location of config file (Default: assgn_dir/config.yml)")
    top_parser.add_argument("-s","--src_dir", default=None, help="Location of source files (Default: config directory)")

    args, unknown = top_parser.parse_known_args()
    args = vars(args)

    if args["config"] is None:
        args["config"] = f'{args["assgn_dir"]}/config.yml'
    if args["src_dir"] is None:
        args["src_dir"] = os.path.dirname(args["config"])

    global ARGS
    global MARKER

    ARGS = args
    MARKER = Marker(args)
    assert(MARKER is not None)
    print(MARKER)
    app.run()

if __name__ == '__main__':
    main()