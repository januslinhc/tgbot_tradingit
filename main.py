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
ð¥° ç­åº¦æé«IPð¥°å¼å¯æ´åæè²âï¸âï¸âï¸

ð¢ æ¸¸æå·²åä¸çº¿ä½éª
ð¢ é¡¹ç®æ¨ç¹å·²åæ¨åå¹´
ð¢ å²æ åä¾çéæ¯æºå¶
ð¢ åçº¦å¹²åï¼æéæ¾å¼

ð¥ è´¢å¯å¯ç ï¼ç¾åæåº  ååèµ·èª ð¥
 ééè¥é! !  è¶å¼ºå±è¯! !  é¢å6000ä¸ç©ºæ! ! 

Tg       Trading IT
Github   https://github.com/eepnt/tgbot_tradingit
            """
        elif cmd == "/group_admin":
            self.response = """
ç¾¤ä¸»: https://www.linkedin.com/in/kevin-leung-hkust/
                """
        elif cmd == "/group_girlgod":
            self.response = """
è°·å¥³ç¥: https://www.linkedin.com/in/erikaaggarwal/
            """
        elif cmd == "/company_list":
            self.response = """
éç¾¤å¬å¸åå®
CS / BAML / GS / HSBC / MS / JPM / DB / Macquarie / SocGen
Tetrion/ XY / Amber / Jane Street / Maven / BitMEX / BFAM / Auros / Akuna / Binance / 3AC / Yubo / Schonfeld
Oracle / Amazon / Meta
            """
        elif cmd == "/hi":
            self.response = """hi {}""".format(content)

    def new_member_join(self, name):
        self.response = """
æ­¡è¿ {} å å¥Trading IT,

è¥æ³è¦å å¥è¨è«ï¼å°±è¦åé²è¡èº«ä»½é©è­(KYCé©è­)ï¼
å¿é è¦ä¸å³åäººçèº«ä»½è­ãLinkedInãè­·ç§(3é¸1)ï¼
æå¾ä¹å¿é ä½¿ç¨ææ©æé»è¦å§å»ºçç¸æ©æç§ä¸å³èªå·±çç§çï¼
éç¨®é©è­ç®çä¸»è¦æ¯ééå¯¦åèªè­é²ç¯æ´é¢ç­éæ³æ´»åã

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

