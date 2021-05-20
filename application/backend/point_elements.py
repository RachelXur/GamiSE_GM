from flask import Flask
from application import app, bcrypt, db
from application.model import User, Post, Userreport, Itreport, Ituser, Phishingcampaign, Phishingresult, LikePostRecord, DislikePostRecord
from application.model import Pointrules, Achievementrules, Badgerules, Rewardrules, Userpoints, Userachievements, Userbadges, Userrewards
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestPResetForm, ResetPwForm, ResetPwLoggedForm, DailyNewsForm, DailyTipsForm
from application.forms import UserReportForm, ITReportForm, ITCheckForm, SimulationForm, PointRuleForm, AchievementRuleForm, BadgeRuleForm, RewardRuleForm

def register_point():
    form = RegistrationForm()
    currentuser = User.query.filter_by(email=form.email.data).first()
    pointrecord = Userpoints(reason="Register", points_id=7, user_id=currentuser.id)
    db.session.add(pointrecord)
    db.session.commit()
    return form, currentuser, pointrecord

def post_point():
    form = PostForm()
    postpoint = Userpoints(reason='Share an experience' + ' "' + form.title.data + '"', points_id=1, user_id=current_user.id)
    db.session.add(postpoint)
    db.session.commit()
    return form, postpoint

def likepost_point(pid):
    reasonlike = 'Click Like' + ' "' + str(pid) + '"'
    responsepoints = Userpoints.query.filter(Userpoints.reason == reasonlike, Userpoints.points_id == 2, Userpoints.user_id == current_user.id).first()
    if not responsepoints:
        responserecord = Userpoints(reason='Click Like' + ' "' + str(pid) + '"', points_id=2, user_id=current_user.id)
        db.session.add(responserecord)
        db.session.commit()
    return pid, reasonlike, responsepoints

def deletelikepost_point(pid):
    reasonlike = 'Click Like' + ' "' + str(pid) + '"'
    responsepoints = Userpoints.query.filter(Userpoints.reason == reasonlike, Userpoints.points_id == 2, Userpoints.user_id == current_user.id).first()
    if responsepoints:
        db.session.delete(responsepoints)
        db.session.commit()
    return pid, reasonlike, responsepoints

def unlikepost_point(pid):
    reasonunlike = 'Click Not Interested' + ' "' + str(pid) + '"'
    responsepoints = Userpoints.query.filter(Userpoints.reason == reasonunlike, Userpoints.points_id == 3, Userpoints.user_id == current_user.id).first()
    if not responsepoints:
        responserecord = Userpoints(reason='Click Not Interested' + ' "' + str(pid) + '"', points_id=3, user_id=current_user.id)
        db.session.add(responserecord)
        db.session.commit()
    return pid, reasonunlike, responsepoints

def deleteunlikepost_point(pid):
    reasonunlike = 'Click Not Interested' + ' "' + str(pid) + '"'
    responsepoints = Userpoints.query.filter(Userpoints.reason == reasonunlike, Userpoints.points_id == 3, Userpoints.user_id == current_user.id).first()
    if responsepoints:
        db.session.delete(responsepoints)
        db.session.commit()
    return pid, reasonunlike, responsepoints

def report_point():
    form = UserReportForm()
    reportpoint = Userpoints(reason='Report an attack' + ' "' + form.subject.data + '"', points_id=4, user_id=current_user.id)
    db.session.add(reportpoint)
    db.session.commit()
    return form, reportpoint

def deleteuserreport_point(pid):
    report = Userreport.query.filter_by(report_id=pid).first()
    deleteuserreport = Userpoints(reason='IT delete your report' + ' "' + report.subject + '"', points_id=6, user_id=report.user_id)
    db.session.add(deleteuserreport)
    return pid, deleteuserreport