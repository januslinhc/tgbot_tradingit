import flask, random, functools, logging, google.cloud.logging

google.cloud.logging.Client().setup_logging()

try:
  import googleclouddebugger
  googleclouddebugger.enable(
    breakpoint_enable_canary=False
  )
except ImportError:
  pass

app = flask.Flask(__name__)

class tgmsg_digester():
    def __init__(self, data):
        self.data = data
        self.response = None
        if "message" in data:
            message = data["message"]
            if "text" in message:
                text = message["text"]
                splits = text.split(' ', 1)
                command = splits[0].replace("@tradingitbot", "")
                if len(splits) == 1:
                    splits.append("")
                self.command(command, splits[1])
            elif "new_chat_member" in message:
                new_chat_member = message["new_chat_member"]
                if new_chat_member["is_bot"] == False:
                    self.new_member_join(new_chat_member["first_name"])

        
    def command(self, cmd, content):
        if cmd == "/help":
            self.response = """
🥰 热度最高IP🥰开启暴力拉菲❗️❗️❗️

🟢 游戏已先上线体验
🟢 项目推特已发推半年
🟢 史无前例的销毁机制
🟢 合约干净，权限放弃

💥 财富密码：百倍打底  千倍起航 💥
 重金营销! !  超强共识! !  领取6000万空投! ! 

Tg       Trading IT
Github   https://github.com/eepnt/tgbot_tradingit
            """
        elif cmd == "/group_admin":
            self.response = """
群主: https://www.linkedin.com/in/kevin-leung-hkust/
                """
        elif cmd == "/group_girlgod":
            self.response = """
谷女神: https://www.linkedin.com/in/erikaaggarwal/
            """
    def new_member_join(self, name):
        self.response = """
歡迎 {} 加入Trading IT,

若想要加入討論，就要再進行身份驗證(KYC驗證)，
必須要上傳個人的身份證、LinkedIn、護照(3選1)，
最後也必須使用手機或電腦內建的相機拍照上傳自己的照片，
這種驗證目的主要是透過實名認證防範洗錢等非法活動。

Best Regards
            """.format(name)
    def response_output(self):
        if self.response is not None:
            return {
                "method": "sendMessage",
                "chat_id": self.data["message"]["chat"]["id"],
                'text': self.response
            }
        else:
            return None


def command_match(cmd, input):
    return input == cmd or input == cmd + "@tradingitbot"

@app.route('/', methods=["POST"])
def hello():
    try:
        data = flask.request.get_json()
        logging.info(data)
        response = tgmsg_digester(data).response_output()
        logging.info(response)
        if response != None:
            return flask.jsonify(response)
        else:
            return ""
    except Exception as e:
        import traceback
        logging.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        return ""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

