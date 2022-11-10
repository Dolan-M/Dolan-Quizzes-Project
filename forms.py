# min=4,max=20 for the PasswordField in registration means password must be at least 3 characters long and at most 20 characters long. Same effect for the user_id
# min and max for the questions act as expected

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, SelectField
from wtforms.validators import InputRequired, EqualTo, NumberRange, Length
#Length with help from https://wtforms.readthedocs.io/en/2.3.x/validators/
from wtforms.fields.html5 import DateField

class RegistrationForm(FlaskForm):
    user_id = StringField("User ID:",validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField("Password:",validators=[InputRequired(), Length(min=4,max=20)])
    password2 = PasswordField("Confirm Password:",validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User ID:",validators=[InputRequired()])
    password = PasswordField("Password:",validators=[InputRequired()])
    submit = SubmitField("Submit")

class LeaderboardForm(FlaskForm):
        quiz = SelectField("Order By:",
                        choices=[("wombats","Wombats"),
                                ("history","History"),
                                ("geography","Geography"),
                                ("total","Total")],
                        validators=[InputRequired()])
        submit = SubmitField("Submit")

class WombatQuizForm(FlaskForm):
    speciesQ = RadioField("Q1. How many wombat species are there?",
                            choices=[("1","1"),
                                ("2","2"),
                                ("3","3"),
                                ("4","4")],
                            default="1")
    teethQ = IntegerField("Q2. How many teeth do wombats have? (Hint: It's between 10 and 30)",
                            validators=[InputRequired(),NumberRange(10,30)])
    poopQ = SelectField("Q3. What shape is wombat poop?",
                            choices=[("round","Round"),
                                    ("octagon","Octagon"),
                                    ("hexagon","Hexagon"),
                                    ("cube","Cube")],
                            validators=[InputRequired()])
    averageQ = SelectField("Q4. What is the average lifespan of a wombat?",
                            choices=[("15years","15 Years"),
                                    ("20years","20 Years"),
                                    ("25years","25 Years")],
                            validators=[InputRequired()])
    relativeQ = SelectField("Q5. What is the wombat's nearest relative?",
                            choices=[("kangaroo","Kangaroo"),
                                    ("numbat","Numbat"),
                                    ("koala","Koala"),
                                    ("chimpanzee","Chimpanzee")],
                            validators=[InputRequired()])
    submit = SubmitField("Submit Quiz")

class HistoryQuizForm(FlaskForm):
        worldwarQ = SelectField("Q1. At what date did World War 2 end?",
                                choices=[("1","1 September 1945"),
                                        ("2","2 September 1945"),
                                        ("3","3 September 1945"),
                                        ("5","5 September 1945")],
                                validators=[InputRequired()])
        spaceQ = SelectField("Q2. Who was the first human to journey into space?",
                                choices=[("alan","Alan Shepard"),
                                        ("alexei","Alexei Leonov"),
                                        ("valentina","Valentina Tereshkova"),
                                        ("john","John Young"),
                                        ("yuri","Yuri Gagarin")],
                                validators=[InputRequired()])
        assassinateQ = IntegerField("Q3. How many U.S presidents were assassinated? (Hint: It's between 1 and 10)",validators=[InputRequired(),NumberRange(1,10)])
        presidentQ = IntegerField("Q4. How many Irish presidents have there been? (Hint: It's between 5 and 20)",validators=[InputRequired(),NumberRange(5,20)])
        hitlerQ = StringField("Q5. In what country was Hitler born? (Hint: It's 7 letters long)",validators=[InputRequired(),Length(max=7)])
        submit = SubmitField("Submit Quiz")

class GeographyQuizForm(FlaskForm):
        capitalQ = StringField("Q1. What is the capital city of France? (Hint: It's 5 letters long)",validators=[InputRequired(),Length(max=5)])
        mountainQ = SelectField("Q2. What is the second highest mountain on Earth?",
                                choices=[("everest","Everest"),
                                        ("makalu","Makalu"),
                                        ("manaslu","Manaslu"),
                                        ("k2","K2")],
                                validators=[InputRequired()])
        rockQ = RadioField("Q3. How many rock types are there?",
                                choices=[("1","1"),
                                        ("2","2"),
                                        ("3","3"),
                                        ("4","4")],
                                default="1")
        stateQ = IntegerField("Q4. How many states are in the U.S?",validators=[InputRequired(),NumberRange(10,100)])
        populationQ = SelectField("Q5. Which of these countries has the largest population??",
                                        choices=[("indonesia","Indonesia"),
                                                ("brazil","Brazil"),
                                                ("nigeria","Nigeria"),
                                                ("pakistan","Pakistan")],
                                        validators=[InputRequired()])
        submit = SubmitField("Submit Quiz")

class SuggestionForm(FlaskForm):
        suggestion = StringField("Type a suggestion for a new quiz:",validators=[Length(max=200)])
        submit = SubmitField("Submit")

class PastAttemptsForm(FlaskForm):
        quiz = SelectField("Choose Quiz:",
                                choices=[("wombats","Wombats"),
                                        ("history","History"),
                                        ("geography","Geography")],
                                validators=[InputRequired()])
        user_id = StringField("User ID (Optional):")
        submit = SubmitField("Submit")


