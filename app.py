from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))

    def __init__(self, name, author):
        self.name = name
        self.author = author



@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", books=all_data)



@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']


        my_data = Data(name, author)
        db.session.add(my_data)
        db.session.commit()

        flash("Book Inserted Successfully")

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.author = request.form['author']


        db.session.commit()
        flash("Book Updated Successfully")

        return redirect(url_for('Index'))



@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book Deleted Successfully")

    return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(debug=True)
