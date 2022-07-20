import os
from threading import Thread
from flask import Flask, render_template
#import pandas as pd

def flush(prompt,reply):
  with open('data.txt','a') as f:
    z=reply.replace("\n","|")
    f.write(f"${prompt}$,${z}$")
    f.write("\n")

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',
    static_folder='static'  # Name of directory for static files
)


@app.route('/')  # What happens when the user visits the site
def base_page():
    return render_template('base.html')


def runApp():
    app.run(host='0.0.0.0', port=8888)


def runMain():

    import telebot
    #import getreply
    import openai
    import constants as c

    #creting bot instace
    openai.api_key = os.getenv('key')
    TOKEN = os.environ['TOKEN']
    bot = telebot.TeleBot(TOKEN)

    global temp
    temp = 0.6

    @bot.message_handler(commands=['start', 'help'])
    def handle_start(message):
        bot.reply_to(message, c.h)

    @bot.message_handler(commands=['randomness'])
    def handle_help(message):
        global temp
        l = message.text.strip().split(" ")
        print(message.text)

        if len(l) != 2:
            bot.reply_to(message, "invalid input")
        else:
            x = l[1]
            print(x)
            if is_a_good_number(x) == True:
                temp = float(x)
                bot.reply_to(
                    message,
                    f"randomness updated! current randomeness is {temp}")
            else:
                bot.reply_to(message, "invalid input")

    @bot.message_handler(func=lambda x: True)
    def handle_update(message):
        msg = message.text
        answer = reply_msg(msg, temp)
        bot.send_message(message.chat.id, answer)

    def reply_msg(input_msg, temp=0.6):
        response = openai.Completion.create(
          model="text-davinci-002",
          prompt=input_msg,
          max_tokens=400,
          temperature=temp)
        y=response.choices[0].text
        #print(response.choices[0].text)
        flush(input_msg,y)
        return y

    def is_a_good_number(x):  #number that lies in 0 to1
        #flag=True
        try:
            float(x)
            if 0 <= float(x) <= 1:
                return True
            else:
                return False
        except ValueError:
            return False

    #start bot...
    print("Bot is started...")
    bot.polling()


if __name__ == "__main__":  # Makes sure this is the main process
    t1 = Thread(target=runApp)
    t2 = Thread(target=runMain)

    t1.start()
    t2.start()

t2.join()
t1.join()
