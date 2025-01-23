from flask import Flask, request, jsonify                        # types: ignored
from libs.protocol.kProtocolRoot import process_data, prepare_response
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
    _data = request.form.get('data', "")  # Get param "data"
    _err, _info = process_data(_data)
    print(3, f"Info: {_info}, err: {_err}")

    response = prepare_response(_info.get('serial', {}))
    response['status'] = "OK"

    print(1, 100, response)
    return jsonify(response)


if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(debug=True)
