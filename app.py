from flask import Flask, request, jsonify, render_template, url_for, redirect, Markup, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)
db_uri = os.environ.get("DATABASE_URL") or "postgresql://localhost/flasknote"
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)
app.secret_key = "abcdefghijklmn"
app.permanent_session_lifetime = timedelta(days=1)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/board/", methods=["POST"])
def post_board():
    name = request.form["name"]
    body = request.form["body"]
    if name != "" and body != "":
        session.permanent = True
        session["name"] = name
        body = body.replace('\n', '<br>')
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        b = Board(name=name, body=body, created_at=time)
        db.session.add(b)
        db.session.commit()
    return redirect(url_for("board"))

@app.route("/board/", methods=["GET"])
def board():
    boards = Board.query.all()
    boards = reversed(list(boards))
    if "name" in session:
        return render_template("board.html", boards=boards, name=session["name"])
    else:
        return render_template("board.html", boards=boards, name="")

if __name__ == "__main__":
    app.run()