from flask import Flask, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# import requests
# use FLASK to create an app
app = Flask(__name__)
app.secret_key = "faisal12345"
# use SQLAlchemy to create SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-coffee-shop-collection.db"
db = SQLAlchemy(app)
# use Bootstrap to bootstrap the app design
Bootstrap(app)
# use FlaskForm to create a form also include the security certificate
class CafeForm(FlaskForm):
    """Write the inputs elements using string"""
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google maps', validators=[DataRequired()])
    open_time = StringField('Cafe opening time', validators=[DataRequired()])
    close_time = StringField('Cafe closing time', validators=[DataRequired()])
    myChoices_0 = ("☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️")
    cafe_rating = SelectField('Power socket', choices=myChoices_0, validators=[DataRequired()])
    myChoices_1 = ("💪🏼", "💪🏼💪🏼", "💪🏼💪🏼💪🏼", "💪🏼💪🏼💪🏼💪🏼", "💪🏼💪🏼💪🏼💪🏼💪🏼")
    wifi_strength = SelectField('How is the wifi strength', choices=myChoices_1, validators=[DataRequired()])
    myChoices = ("🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")
    power_socket = SelectField('Power socket', choices=myChoices, validators=[DataRequired()])
    submit = SubmitField('Submit')

# Creating columns in the database:
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), unique=False, nullable=False)
    open = db.Column(db.String(250), unique=False, nullable=False)
    close = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.String(250), unique=False, nullable=False)
    wifi = db.Column(db.String(250), unique=False, nullable=False)
    power = db.Column(db.String(250), unique=False, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Cafe {self.title}>'


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # CREATE RECORD
            new_cafe = Cafe(
                name=form.cafe.data,
                location=form.location.data,
                open=form.open_time.data,
                close=form.close_time.data,
                rating=form.cafe_rating.data,
                wifi=form.wifi_strength.data,
                power=form.power_socket.data
            )
            # CREATE RECORD
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route("/delete")
def delete():
    cafe_id = request.args.get('id')
    print(cafe_id)
    # DELETE A RECORD BY ID
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))




if __name__ == '__main__':
    app.run(debug=True)