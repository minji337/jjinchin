from flask import Flask, render_template, request
import sys
import finance_chatbot

application = Flask(__name__)

@application.route('/get_return_rate')
def get_return_rate():
    fund_name = request.args.get('펀드명').replace(' ', '')
    return finance_chatbot.get_return_rate(펀드명=fund_name)

@application.route('/get_total_assets')
def get_total_assets():
    fund_name = request.args.get('펀드명').replace(' ', '')
    return finance_chatbot.get_total_assets(펀드명 = fund_name)

# Public 공개하는 경우
@application.route('/policy')
def policy():
    return render_template("policy.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))