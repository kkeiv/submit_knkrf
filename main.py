from flask import Flask, request, jsonify                        # types: ignored
from libs.protocol import kProtocolRoot as kProt
from libs.common.config import cfg

CONFIG_NAME: str = "config.json"
result = cfg.load(CONFIG_NAME)
if not result:
    print(f"Configuration does not loaded. Check {CONFIG_NAME}")
    exit(1)

app = Flask(__name__)


@app.route("/test")
def hello_test():
    print("/test")
    return "Hello World! Submit Test"


@app.route('/submit', methods=['POST'])
def submit():
    print(1, request, request.form)
    # get payload from request from user device
    _data = request.form.get('data', "")

    # process payload into database
    _err, _info = kProt.process_data(_data)
    print(3, f"Info: {_info}, err: {_err}")

    # prepare message for payload in response
    response = kProt.prepare_response(_info.get('serial', {}))
    print(1, 100, response)

    # send response to use device
    return jsonify(response)


@app.route('/acknowledge', methods=['POST'])
def acknowledge():
    print(10, request, request.form)
    # get payload from request from user device
    _data = request.form.get('data', "")

    # process payload for database update
    _err, _info = kProt.process_acknowledge(_data)
    print(11, f"Info: {_info}, err: {_err}")

    # send response to use device
    return jsonify({})


if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(debug=True)
