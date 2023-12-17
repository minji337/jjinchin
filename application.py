from flask import Flask
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello goorm!"


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
