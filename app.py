# %B with help from https://www.kite.com/python/docs/django.forms.DateField, %I:%M:%S %p with help from https://docs.oracle.com/cd/E19857-01/817-6248-10/crtime.html
# page variable is there to add to the <title> to change depending on what page the user is on
# Very basic profanity filter so that user_id can't be any of the words in the list (Line 77)
# Can't have same user id but with different case combinations, as it is all converted to lower case e.g dolan and dOLan, Alice and aLiCe etc (Line 74)
# Avoids multiple users of the same id from registering (Line 91)
# Custom error 404 page (Line 60)
# Suggestion page for a regular user gives a form asking for a suggestion of a new quiz. It is optional, and once they make a suggestion, cookies forbid them from making another one for a certain amount of time.
''' Admin user id is dolan
    Password is orlando
    This user can see a table of the suggestions that have been made in the "Suggestion" page. If no suggestion has been made, it simply says "There are no suggestions at this time." '''

''' Answers to wombats quiz: Q1: 3
                            Q2: 24
                            Q3: Cube
                            Q4: 25 Years
                            Q5: Koala
'''
''' Answers to history quiz: Q1: 2 September 1945
                            Q2: Yuri Gagarin
                            Q3: 4
                            Q4: 9
                            Q5: Austria (There's no case sensitivity)
'''
''' Answers to geography quiz: Q1: Paris (There's no case sensitivity)
                                Q2: K2
                                Q3: 3
                                Q4: 50
                                Q5: Indonesia
'''
from flask import Flask, render_template, session, request, redirect, url_for, g, make_response
from datetime import datetime
from database import get_db, close_db
from forms import RegistrationForm, LoginForm, WombatQuizForm, HistoryQuizForm, GeographyQuizForm, LeaderboardForm, SuggestionForm, PastAttemptsForm
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id",None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html", page="Error!"), 404

@app.route("/")
def index():
    current_date = datetime.now().strftime("%d %B %Y")
    return render_template("index.html",current_date=current_date, page="Home")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user_id = user_id.lower()
        password = form.password.data
        password2 = form.password2.data
        profanity = ["fuck","bitch","cunt","fucker","shithead","dick","shit","pharaoh","asshole","crap","idiot","bastard","bollocks","wanker","twat","whore"]
        if user_id in profanity:
            form.user_id.errors.append("User ID invalid.")
        else:
            db = get_db()
            user = db.execute(''' SELECT * FROM users
                                    WHERE user_id = ?;''',(user_id,)).fetchone()
            if user is None:
                db.execute('''INSERT INTO users (user_id,password)
                            VALUES (?,?);''',(user_id,generate_password_hash(password)))
                db.commit()
                db.execute(''' INSERT INTO leaderboard (user_id,wombatpoints,historypoints,geographypoints,totalpoints)
                                VALUES (?,?,?,?,?);''',(user_id,0,0,0,0))
                db.commit()
                return redirect(url_for("login"))
            elif user is not None:
                form.user_id.errors.append("User ID already taken.")
    return render_template("register.html", form=form, page="Register")

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user_id = user_id.lower()
        password = form.password.data
        db = get_db()
        user = db.execute(''' SELECT * FROM users
                                WHERE user_id = ?;''',(user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("Unknown User ID.")
        elif not check_password_hash(user["password"],password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form, page="Login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/quizzes", methods=["GET","POST"])
@login_required
def quiizes():
    return render_template("quiizes.html",page="Quizzes")

@app.route("/leaderboards", methods=["GET","POST"])
@login_required
def leaderboards():
    form = LeaderboardForm()
    leaderboard = None
    caption = ""
    db = get_db()
    if form.validate_on_submit():
        select = form.quiz.data
        if select=="wombats":
            leaderboard = db.execute(''' SELECT * FROM leaderboard
                                        ORDER BY wombatpoints DESC;''').fetchall()
            caption = "Wombats"
        elif select=="history":
            leaderboard = db.execute(''' SELECT * FROM leaderboard
                                        ORDER BY historypoints DESC;''').fetchall()
            caption = "History"
        elif select=="geography":
            leaderboard = db.execute(''' SELECT * FROM leaderboard
                                        ORDER BY geographypoints DESC;''').fetchall()
            caption = "Geography"
        elif select=="total":
            leaderboard = db.execute(''' SELECT * FROM leaderboard
                                        ORDER BY totalpoints DESC;''').fetchall()
            caption = "Total"
    return render_template("leaderboards.html", form=form,caption=caption, leaderboard=leaderboard, page="Leaderboards")

@app.route("/wombat", methods=["GET","POST"])
@login_required
def wombatQuiz():
    form = WombatQuizForm()
    points = 0
    feedback = ""
    answers = ["3",24,"cube","25years","koala"]
    db = get_db()
    date = datetime.now().strftime("%I:%M:%S %p %d %B %Y")
    if form.validate_on_submit():
        species = form.speciesQ.data
        teeth = form.teethQ.data
        scat = form.poopQ.data
        lifespan = form.averageQ.data
        relative = form.relativeQ.data
        if species in answers:
            points +=1
        if teeth in answers:
            points +=1
        if scat in answers:
            points +=1
        if lifespan in answers:
            points +=1
        if relative in answers:
            points +=1
        db.execute('''UPDATE leaderboard
                        SET wombatpoints = ?
                        WHERE user_id=?
                        AND ? > wombatpoints;''',(points,g.user,points))
        db.commit()
        db.execute('''UPDATE leaderboard
                    SET totalpoints = wombatpoints+historypoints+geographypoints
                    WHERE user_id=?;''',(g.user,))
        db.commit()
        db.execute(''' INSERT INTO pastwombat (user_id,points,date)
                        VALUES (?,?,?); ''',(g.user,points,date))
        db.commit()
    if points==5:
        feedback="Great job!"
    elif points < 5 and points >= 3:
        feedback="Good job."
    elif points ==2:
        feedback="You did below average."
    elif points < 2:
        feedback="Damn, you did bad."
    return render_template("wombatQuiz.html",form=form, points=points, feedback=feedback, page="Wombats")

@app.route("/history", methods=["GET","POST"])
@login_required
def historyQuiz():
    form = HistoryQuizForm()
    points = 0
    feedback = ""
    answers = ["2","yuri",4,9,"austria"]
    db = get_db()
    date = datetime.now().strftime(" %I:%M:%S %p %d %B %Y")
    if form.validate_on_submit():
        ww2 = form.worldwarQ.data
        space = form.spaceQ.data
        assassinate = form.assassinateQ.data
        president = form.presidentQ.data
        hitler = form.hitlerQ.data
        hitler = hitler.lower()
        if ww2 in answers:
            points+=1
        if space in answers:
            points +=1
        if assassinate in answers:
            points +=1
        if president in answers:
            points +=1
        if hitler in answers:
            points +=1
        db.execute('''UPDATE leaderboard
                        SET historypoints = ?
                        WHERE user_id=?
                        AND ? > historypoints;''',(points,g.user,points))
        db.commit()
        db.execute('''UPDATE leaderboard
                    SET totalpoints = wombatpoints+historypoints+geographypoints
                    WHERE user_id=?;''',(g.user,))
        db.commit()
        db.execute(''' INSERT INTO pasthistory (user_id,points,date)
                        VALUES (?,?,?); ''',(g.user,points,date))
        db.commit()
    if points==5:
        feedback="Great job!"
    elif points<5 and points>=3:
        feedback="Good job."
    elif points==2:
        feedback="You did below average."
    elif points<2:
        feedback="Damn, you did bad."
    return render_template("historyQuiz.html", form=form, points=points, feedback=feedback, page="History")

@app.route("/geography", methods=["GET","POST"])
@login_required
def geographyQuiz():
    form = GeographyQuizForm()
    points = 0
    feedback = ""
    answers = ["paris","k2","3",50,"indonesia"]
    db = get_db()
    date = datetime.now().strftime("%I:%M:%S %p %d %B %Y")
    if form.validate_on_submit():
        capital = form.capitalQ.data
        capital = capital.lower()
        mountain = form.mountainQ.data
        rock = form.rockQ.data
        state = form.stateQ.data
        population = form.populationQ.data
        if capital in answers:
            points += 1
        if mountain in answers:
            points += 1
        if rock in answers:
            points += 1
        if state in answers:
            points += 1
        if population in answers:
            points += 1
        db.execute('''UPDATE leaderboard
                        SET geographypoints = ?
                        WHERE user_id=?
                        AND ? > geographypoints;''',(points,g.user,points))
        db.commit()
        db.execute('''UPDATE leaderboard
                    SET totalpoints = wombatpoints+historypoints+geographypoints
                    WHERE user_id=?;''',(g.user,))
        db.commit()
        db.execute(''' INSERT INTO pastgeography (user_id,points,date)
                        VALUES (?,?,?); ''',(g.user,points,date))
        db.commit()
    if points==5:
        feedback="Great job!"
    elif points<5 and points>=3:
        feedback="Good job."
    elif points==2:
        feedback="You did below average."
    elif points<2:
        feedback="Damn, you did bad."
    return render_template("geographyQuiz.html", form=form, points=points, feedback=feedback, page="Geography")

@app.route("/suggestion",methods=["GET","POST"])
@login_required
def suggestion():
    form = SuggestionForm()
    db = get_db()
    date = datetime.now().strftime("%d %B %Y")
    suggestions = None
    if g.user!="dolan":
        user = db.execute('''SELECT user_id from suggestions WHERE user_id=?;''',(g.user,)).fetchone()
        if user is not None:
            if request.cookies.get("suggested")=="yes":
                return render_template("cookie.html", message="Sorry! You already made a suggestion.")
        elif user is None:
            if form.validate_on_submit():
                suggestion = form.suggestion.data
                db.execute(''' INSERT INTO suggestions (user_id,suggestion,date)
                                VALUES (?,?,?);''',(g.user,suggestion,date))
                db.commit()
                response = make_response(render_template("cookie.html",message="Thanks for your suggestion!"))
                response.set_cookie("suggested","yes",max_age=5*365*24*60*60)
                return response
    elif g.user=="dolan":
        suggestions = db.execute(''' SELECT * FROM suggestions; ''').fetchall()
    return render_template("suggestions.html",form=form,suggestions=suggestions, page="Suggestion")

@app.route("/past_attempts",methods=["GET","POST"])
@login_required
def attempts():
    form = PastAttemptsForm()
    db = get_db()
    attempts = None
    caption=""
    if form.validate_on_submit():
        quiz = form.quiz.data
        user_id = form.user_id.data
        if quiz=="wombats":
            if user_id=="":
                attempts=db.execute(''' SELECT * FROM pastwombat;''').fetchall()
            elif user_id!="":
                attempts=db.execute(''' SELECT * FROM pastwombat WHERE user_id=?;''',(user_id,)).fetchall()
            caption="Wombats"
        elif quiz=="history":
            if user_id=="":
                attempts=db.execute(''' SELECT * FROM pasthistory;''').fetchall()
            elif user_id!="":
                attempts=db.execute(''' SELECT * FROM pasthistory WHERE user_id=?;''',(user_id,)).fetchall()
            caption="History"
        elif quiz=="geography":
            if user_id=="":
                attempts=db.execute(''' SELECT * FROM pastgeography;''').fetchall()
            elif user_id!="":
                attempts=db.execute(''' SELECT * FROM pastgeography WHERE user_id=?;''',(user_id,)).fetchall()
            caption="Geography"
    return render_template("pastAttempts.html",form=form,attempts=attempts,caption=caption,page="Past Attempts")









