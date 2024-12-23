import pytz
from datetime import datetime
from flask import Flask, request                        # types: ignored
from libs.protocol.kProtocolRoot import process_data, save_info
from libs.common.config import cfg

CONFIG_NAME: str = "config.json"
result = cfg.load(CONFIG_NAME)
print(1, 100, cfg.read(debug=False))
if not result:
    print(f"Configuration does not loaded. Check {CONFIG_NAME}")
    exit(1)

save_info({"test": "test"})


# Получение текущего времени в UTC (GMT0)
utc_time = datetime.now(pytz.utc)
print("Текущий таймстамп в GMT0 (UTC):", utc_time.strftime('%Y-%m-%d %H:%M:%S'))

# Получение текущего времени в локальном часовом поясе
local_time = datetime.now()
print("Текущий таймстамп в текущем часовом поясе:", local_time.strftime('%Y-%m-%d %H:%M:%S'))

# Определение текущего часового пояса
local_tz = datetime.now().astimezone().tzinfo
print("Текущий часовой пояс:", local_tz)

app = Flask(__name__)


@app.route("/test")
def hello_test():
    print("/test")
    return "Hello World! Submit Test"


@app.route('/submit', methods=['POST'])
def submit():
    print(1, request, request.form)
    _data = request.form.get('data', "")  # Get param "data"
    print(2, f"Data: {_data} {type(_data)}")
    _err, _info = process_data(_data)
    print(3, f"Info: {_info}, err: {_err}")

    return "OK"


if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(debug=True)
