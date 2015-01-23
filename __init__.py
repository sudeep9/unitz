from flask import Flask

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
from alchemy import views
