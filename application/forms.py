from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, InputRequired, ValidationError, NumberRange
from flask_wtf.file import FileField, FileAllowed
from application.model import User, Phishingcampaign
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password'), Length(min=6, max=60)])
    position = RadioField('Position', choices=[('Yes', 'Yes'), ('No', 'No')])
    itusercode = StringField('Code')
    interest = SelectField('Interests', choices=[('Sport', 'Sport'), ('Pets', 'Pets'), ('Music', 'Music'), ('Electronic', 'Electronic')])
    qa = RadioField('Qa', choices=[('Yes', 'Yes'), ('No', 'No')])
    qb = RadioField('Qb', choices=[('Facebook', 'Facebook'), ('Twitter', 'Twitter')])
    qc = RadioField('Qc', choices=[('TD', 'TD'), ('Scotia Bank', 'Scotia Bank'), ('RBC', 'RBC')])
    qd = RadioField('Qd', choices=[('Credit/Debit', 'Credit/Debit'), ('Apple Pay', 'Apple Pay'), ('Paypal', 'Paypal')])
    qe = RadioField('Qe', choices=[('Yes', 'Yes'), ('No', 'No')])
    qf = RadioField('Qf', choices=[('Yes', 'Yes'), ('No', 'No')])
    qg = RadioField('Qg', choices=[('Student', 'Student'), ('Graduated', 'Graduated')])
    qh = RadioField('Qh', choices=[('Yes', 'Yes'), ('No', 'No')])
    qi = RadioField('Qi', choices=[('Yes', 'Yes'), ('No', 'No')])
    qj = RadioField('Qj', choices=[('Yes', 'Yes'), ('No', 'No')])
    qk = RadioField('Qk', choices=[('Yes', 'Yes'), ('No', 'No')])
    terms = RadioField('Terms', choices=[('Yes', 'Yes')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username!')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired('Title is required!'), Length(min=1, max=200)])
    content = TextAreaField('Content', validators=[InputRequired('Content is required!')])
    submit = SubmitField('Post')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=2, max=150)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UpdateAccountPhotoForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Select')


class RequestPResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=2, max=150)])
    submit = SubmitField('Request Token')


class ResetPwForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password'), Length(min=6, max=50)])
    submit = SubmitField('Confirm Password')
    

class ResetPwLoggedForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired(), Length(min=6, max=50)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('new_password'), Length(min=6, max=50)])
    submit = SubmitField('Confirm Password')


class UserReportForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired(), Length(min=2, max=200)])
    senderemail = StringField('Email', validators=[InputRequired(), Length(min=2, max=200)])
    reason = TextAreaField('Reason', validators=[InputRequired()])
    riskaction = TextAreaField('Riskaction', validators=[InputRequired()])
    reportstatus = RadioField('Reportstatus', choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField('Submit')


class WithdrawalForm(FlaskForm):
    qa = RadioField('qa', choices=[('Less than 15 minutes', 'Less than 15 minutes'), ('16-30 minutes', '16-30 minutes'), ('Over 30 minutes', 'Over 30 minutes')])
    qb = RadioField('qb', choices=[('Yes', 'Yes'), ('No', 'No')])
    qc = RadioField('qc', choices=[('Yes', 'Yes'), ('No', 'No')])
    qd = RadioField('qd', choices=[('Yes', 'Yes'), ('No', 'No')])
    reason = TextAreaField('Reason', validators=[InputRequired()])
    submit = SubmitField('Withdrawal')


class ITReportForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired(), Length(min=2, max=200)])
    senderemail = StringField('Email', validators=[InputRequired(), Length(min=2, max=200)])
    reason = TextAreaField('Reason', validators=[InputRequired()])
    solution = TextAreaField('Riskaction', validators=[InputRequired()])
    submit = SubmitField('Submit')


class ITCheckForm(FlaskForm):
    submit = SubmitField('Read')


class DailyNewsForm(FlaskForm):
    receiver = SelectField('Receiver', choices=[('Normal Users', 'Normal Users'), ('IT', 'IT')])
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=200)])
    link = StringField('Link', validators=[InputRequired()])
    image_url = StringField('Image URL (Optional)')
    description = TextAreaField('Desription', validators=[InputRequired()])
    submit = SubmitField('Send')


class DailyTipsForm(FlaskForm):
    receiver = SelectField('Receiver', choices=[('Normal Users', 'Normal Users'), ('IT', 'IT')])
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=200)])
    link = StringField('Link', validators=[InputRequired()])
    image_url = StringField('Image URL (Optional)')
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Send')


class SimulationNoteForm(FlaskForm):
    receiver = SelectField('Receiver', choices=[('IT', 'IT')])
    subject = TextAreaField('Simulation Subject', validators=[InputRequired()])
    sender = TextAreaField('Sender', validators=[InputRequired()])
    submit = SubmitField('Send')


class SimulationForm(FlaskForm):
    campaign_name = StringField('Campaign Name', validators=[InputRequired(), Length(min=2, max=100)])
    phishing_type = SelectField('Phishing Type', choices=[('Tablet', 'Tablet'), ('MFA PWD', 'MFA PWD'), ('Google News', 'Google News'), 
                                                            ('Discount', 'Discount'), ('Change PWD', 'Change PWD'), ('Trending News', 'Trending News')])
    submit = SubmitField('Send')


    def validate_campaign(self, campaign_name):
        campaign_name = Phishingcampaign.query.filter_by(campaign_name=campaign_name.data).first()
        if campaign_name:
            raise ValidationError('That campaign name is taken. Please choose a different username!')


class PointRuleForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired(), Length(min=2, max=200)])
    addpoints = IntegerField('Points', validators=[InputRequired(), NumberRange(min=-1000, max=1000)])
    submit = SubmitField('Add')


class AchievementRuleForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=200)])
    description = StringField('Description', validators=[InputRequired(), Length(min=2, max=200)])
    addpoints = IntegerField('Points', validators=[InputRequired(), NumberRange(min=-1000, max=1000)])
    submit = SubmitField('Add')


class BadgeRuleForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=200)])
    description = StringField('Description', validators=[InputRequired(), Length(min=2, max=200)])
    image_file = FileField('Badge Image (Required)', validators=[InputRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')


class RewardRuleForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=200)])
    description = StringField('Description', validators=[InputRequired(), Length(min=2, max=200)])
    image_file = FileField('Reward Image (Required)', validators=[InputRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')


class PickWinsForm(FlaskForm):
    submit = SubmitField('PickWins')


class CheckuserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=2, max=200)])
    submit = SubmitField('Submit')


class PhotouploadForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class PhotoselectForm(FlaskForm):
    picture = FileField('Select Photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Choose')