from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length
from .src.constants import *

class SetupForm(Form):
    roles = [("none", "None"), ("random", "Random"), (CP, CP), (DISPATCHER, DISPATCHER), (MEDIC, MEDIC), (OE, OE), (QS, QS), (RESEARCHER, RESEARCHER), (SCIENTIST, SCIENTIST)]
    char0 = SelectField("Role 1", choices=roles, validators=[DataRequired()])
    char1 = SelectField("Role 2", choices=roles, validators=[DataRequired()])
    char2 = SelectField("Role 3", choices=roles, validators=[DataRequired()])
    char3 = SelectField("Role 4", choices=roles, validators=[DataRequired()])

    difficulty = SelectField("Difficulty", coerce=int, choices=[(4, "Easy (4 epidemics)"), (5, "Normal (5 epidemics)"), (6, "Hard (6 epidemics)")], validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False
        chosen = [self.char0.data, self.char1.data, self.char2.data, self.char3.data]
        if len(chosen) < 2:
            return False
        return True

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField("remember_me", default=False)
