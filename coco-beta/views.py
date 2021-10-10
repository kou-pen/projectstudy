from flask import Flask,request,redirect,url_for,render_template,flash,session
from sqlalchemy.sql.expression import desc
from sqlalchemy import text
from datetime import datetime, timedelta, timezone
from models.entries import Entry ,SESSION,User


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'gmowyu7938q2y7uhfsiu7827rngw7390167reidnsdhgoi2yifg6t783hj4i'


@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    entrie = SESSION.query(Entry).order_by(desc(Entry.id))
    return render_template('home.html',entries = entrie)

@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method == 'POST':
        userm = User(
            name = request.form['usernames'],
            password = request.form['passwords'],
            roll = False
        )
        SESSION.add(userm)
        SESSION.commit()
        flash('signuped')
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('signups.html')
    else:
        pass

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pname = request.form['username']
        p1 = SESSION.query(User).filter(text("name=:name")).params(name=pname)#.first()
        
        for row in p1:
            NAME = row.name
            PASSWD = row.password
        if request.form['username'] != NAME:
            flash('error:username')
        elif request.form['password'] != PASSWD:
            flash('error:passwd')
        else:
            session['logged_in']=True
            session['user_name']=NAME
            flash('logged_in')
            return redirect(url_for('show_entries'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    session.pop('username',None)
    flash('logged out')
    return redirect(url_for('show_entries')) 

@app.route('/entries',methods=['POST'])
def add_entry():
    JST = timezone(timedelta(hours=+9), 'JST')
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    entry = Entry(
        long = request.form['long'],
        subject = request.form['subject'],
        comment = request.form['comment'],
        created_at = datetime.now(JST),
        created_by = session.get('user_name')
    )
    SESSION.add(entry)
    SESSION.commit()
    flash('created')
    return redirect(url_for('show_entries')) 

@app.route('/entries/new')
def new_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    return render_template('new.html')

@app.route('/delete/<counts>')
def delete(counts):
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    usernames = session.get('username')
    userroll = SESSION.query(User).filter(text("name=:name")).params(name=usernames)#.first()
    for raw in userroll:
        if raw.roll == False:
            return redirect(url_for('show_entries'))
    else:
        if counts != 'all':
            Nom = counts
            contents = SESSION.query(Entry).filter(text("id=:Nom")).params(Nom=Nom)
            for deletedata in contents:
                SESSION.delete(deletedata)
                SESSION.commit()
            flash('deleted')
            return redirect(url_for('show_entries'))
        elif counts == 'all':
            contents = SESSION.query(Entry).order_by(desc(Entry.id))
            for deletedata in contents:
                SESSION.delete(deletedata)
                SESSION.commit()
            flash('deleted')
            return redirect(url_for('show_entries'))

if __name__ =='__main__': 
    app.run(host='0.0.0.0')