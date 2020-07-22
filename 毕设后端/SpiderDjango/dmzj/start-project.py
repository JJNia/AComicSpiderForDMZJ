from scrapy import cmdline
from flask import Flask, request
from flask_cors import CORS

import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/start', methods=['post'])
def get_data():
    data = request.form
    manhua_url = data.get("url")
    manhua_name = data.get("name")
    print(manhua_url + " " + manhua_name)
    cmdline.execute(str("scrapy crawl DMZJ -a manhua_url=%s -a manhua_name=%s" % (manhua_url, manhua_name)).split())
    return "爬取结束"

app.run(debug=True)