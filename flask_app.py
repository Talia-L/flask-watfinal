from flask import Flask, render_template, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'happygirl759'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/TL759/site/finaldemo/tmp/database.db'
db = SQLAlchemy(app)

class Listing(db.Model):
    __tablename__ = "Eligible DC Bachelors and Bachelorettes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    sexorientation = db.Column(db.String(20))
    location = db.Column(db.String(30))
    occupation = db.Column(db.String(30))
    interests = db.Column(db.String(300))
    religion = db.Column(db.String(20))
    lookingfor = db.Column(db.String(300))
    email = db.Column(db.String(40))
    socialmedia = db.Column(db.String(200))

class ListingForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    sexorientation = TextAreaField('Sexual Orientation', validators=[DataRequired()])
    location = TextAreaField('Location', validators=[DataRequired()])
    occupation = TextAreaField('Occupation', validators=[DataRequired()])
    interests = TextAreaField('Interests', validators=[DataRequired()])
    religion = TextAreaField('Religion', validators=[DataRequired()])
    lookingfor = TextAreaField('I am looking for', validators=[DataRequired()])
    email = TextAreaField('Email Address', validators=[DataRequired()])
    socialmedia = TextAreaField('Social Media', validators=[DataRequired()])

@app.route('/')
def index():
    results = Listing.query.filter(1==1).all()
    return render_template('index.html', listings=results)

@app.route('/listing/new', methods=['GET', 'POST'])
def newlisting():
    form = ListingForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
          flash('All fields are required. Please provide all information!')
          return render_template('newlisting.html', form=form)
        else:
          lst = Listing(name=form.name.data, age=form.age.data, sexorientation=form.sexorientation.data, location=form.location.data, occupation=form.occupation.data, interests=form.interests.data, religion=form.religion.data, lookingfor=form.lookingfor.data, email=form.email.data, socialmedia=form.socialmedia.data)
          db.session.add(lst)
          db.session.commit()
          results = Listing.query.filter(1==1).all()
          return render_template('index.html', listings=results)
    else:
        return render_template('newlisting.html', form=form)

@app.route('/listing/show/<listing_id>')
def listing_show(listing_id):
    try:
        lst = Listing.query.get(listing_id)
    except:
        abort(404)

    return render_template('listing_show.html', list_id=lst.id, listing=lst)

@app.route('/listing/edit/<listing_id>', methods=['GET','POST'])
def listing_edit(listing_id):
    form = ListingForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('listing_edit.html', form=form)
        else:
          lst = Listing.query.get(listing_id)
          lst.name=form.name.data
          lst.age= form.age.data
          lst.sexorientation=form.sexorientation.data
          lst.location= form.location.data
          lst.occupation= form.occupation.data
          lst.interests= form.interests.data
          lst.religion= form.religion.data
          lst.lookingfor= form.lookingfor.data
          lst.email= form.email.data
          lst.socialmedia= form.socialmedia.data
          db.session.commit()
          flash('Your edits have been saved!')
          return render_template('listing_edit.html', form=form)
    else:
        try:
            lst = Listing.query.get(listing_id)
            lstForm = ListingForm(obj=lst)
        except:
            abort(404)
        return render_template('listing_edit.html', form=lstForm)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')









