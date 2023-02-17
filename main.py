from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from forms import AddCafeForm
import os


SECRET_KEY = os.environ["SECRET_KEY"]

app = Flask(__name__)
app.secret_key = SECRET_KEY
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)

engine = create_engine("sqlite:///cafes.db", connect_args={'check_same_thread': False})
session = Session(engine, future=True)


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = session.execute("SELECT * FROM cafe").all()
    print(result[0])
    return render_template("index.html", cafes=result)


@app.route("/add_cafe", methods=['GET', 'POST'])
def add_cafe():
    cafe_form = AddCafeForm()
    if cafe_form.validate_on_submit():
        if session.execute(f"SELECT name FROM cafe WHERE name='{cafe_form.name.data}'").first():

            flash("CAFE ALREADY ON LIST")
            return redirect(url_for("home"))
        else:
            new_cafe = Cafe(
                name=cafe_form.name.data,
                map_url=cafe_form.map_url.data,
                img_url=cafe_form.img_url.data,
                location=cafe_form.location.data,
                has_sockets=cafe_form.has_sockets.data,
                has_toilet=cafe_form.has_toilet.data,
                has_wifi=cafe_form.has_wifi.data,
                can_take_calls=cafe_form.can_take_calls.data,
                seats=cafe_form.seats.data,
                coffee_price=cafe_form.coffee_price.data,
            )
            session.add(new_cafe)
            session.commit()
            return redirect(url_for("home"))
    else:
        pass
    return render_template("add.html", form=cafe_form)


@app.route("/delete/<cafe_id>", methods=["GET", "POST"])
def delete_cafe(cafe_id):
    result = session.query(Cafe).filter_by(id=cafe_id).first()
    print(result)
    session.delete(result)
    session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
    