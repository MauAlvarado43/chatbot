from flask import Flask, request, render_template
from flask_cors import CORS
from bot import Bot
from database import DB


database = DB()
bot = Bot(database)
app = Flask(__name__, static_folder="static", template_folder="templates")
cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/resetdb")
def reset_db():
    database.init_data()
    return "Se ha reseteado la base de datos"

@app.route("/bot",  methods=['GET'])
def bot_request():
    text = request.args.get('msg')
    return {
        "message": str(bot.get_response(text))
    }
