import flask
import sqlalchemy.sql
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/test'
db = SQLAlchemy(app)


class Visit(db.Model):
    town = db.Column(db.String(512), primary_key=True)
    visit_date = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', visit=Visit.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    town = flask.request.form['town']
    visit_date = flask.request.form['visit_date']

    # messages.append(Message(text, tag))
    if town not in Visit.query.all():
        db.session.add(Visit(town=town, visit_date=visit_date))
        db.session.commit()
    else:
        print(":(((")
    return flask.redirect(flask.url_for('hello'))


@app.route('/clear', methods=['POST'])
def clear():
    db.session.execute(sqlalchemy.sql.text("DELETE FROM visit"))
    db.session.commit()
    return flask.redirect(flask.url_for('hello'))



with app.app_context():
    db.create_all()
app.run()