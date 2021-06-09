# referenced from https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

from searchEngine import retrieve_query
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTiaaamkZfAb'
Bootstrap(app)

class SearchForm(FlaskForm):
    query = StringField('What would you like to search?', validators=[DataRequired()])
    subit = SubmitField('Submit')

@app.route("/", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = ""
    if form.validate_on_submit():
        query = form.query.data
        urls = retrieve_query(query)
        if urls != []:
            results = urls
        else:
            results = ["Sorry, no match was found"]

    return render_template('home.html', form=form, results=results)


if __name__ == "__main__":
    app.run(debug=True)