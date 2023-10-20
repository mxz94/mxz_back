import psycopg2
from flask import Flask, render_template, request
"""扩展实现彻底删除文件功能"""
import pprint
from typing import List


app = Flask(__name__, template_folder="./")


@app.route('/')
def hello_world():
    return render_template("./test.html")

@app.route('/hello/<fileId>')
def hello(fileId):
    return str(fileId)

if __name__ == '__main__':
    app.run(debug=True, port=8080)