from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import func

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB


class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


def to_dict(self):
    # Method 1.
    # dictionary = {}
    # # Loop through each column in the data record
    # for column in self.__table__.columns:
    #     #Create a new dictionary entry;
    #     # where the key is the name of the column
    #     # and the value is the value of the column
    #     dictionary[column.name] = getattr(self, column.name)
    # return dictionary

    # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/random", methods=["GET"])
def get_random_cafe():
    result = db.session.execute(
        db.select(Cafe).order_by(func.random())).scalar()

    return jsonify(cafe=to_dict(result))


@app.route("/all", methods=["GET"])
def get_all_cafes():
    result = db.session.execute(
        db.select(Cafe).order_by(Cafe.id)).scalars()
    cafes_list = [to_dict(cafe) for cafe in result]
    return jsonify(all=cafes_list)

# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
