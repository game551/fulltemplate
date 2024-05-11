from threading import Thread

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
@app.route("/alive")
def alive():
  return "Yes I am running"

def run():
  app.run(host='0.0.0.0', port=5000)


def keep_alive():
  t = Thread(target=run)
  t.start()
