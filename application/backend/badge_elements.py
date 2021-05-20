from flask import Flask
from application import app, bcrypt, db
from application.model import User, Post, Userreport, Itreport, Ituser, Phishingcampaign, Phishingresult, LikePostRecord, DislikePostRecord
from application.model import Pointrules, Achievementrules, Badgerules, Rewardrules, Userpoints, Userachievements, Userbadges, Userrewards
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestPResetForm, ResetPwForm, ResetPwLoggedForm, DailyNewsForm, DailyTipsForm
from application.forms import UserReportForm, ITReportForm, ITCheckForm, SimulationForm, PointRuleForm, AchievementRuleForm, BadgeRuleForm, RewardRuleForm
from sqlalchemy.sql import func
import sys

def register_badge():
    form = RegistrationForm()
    currentuser = User.query.filter_by(email=form.email.data).first()
    badgerecord = Userbadges(badge_id=1, user_id=currentuser.id)
    db.session.add(badgerecord)
    db.session.commit()
    return form, currentuser, badgerecord

#  helpers
def checkBadge(badgeId):
    badgeR = Userbadges.query.filter(Userbadges.badge_id==badgeId, Userbadges.user_id==current_user.id).first()
    return badgeR

def addPostBadge(postCount, badgeId, badges):
    if current_user.post_count >= postCount and not checkBadge(badgeId):
        badge = Userbadges(badge_id=badgeId, user_id=current_user.id)
        db.session.add(badge)
        badges.append(badge)

def addReactBadge(reactCount, badgeId, badges):
    if len(current_user.like_record) + len(current_user.dislike_record) >= reactCount and not checkBadge(badgeId):
        badge = Userbadges(badge_id=badgeId, user_id=current_user.id)
        db.session.add(badge)
        badges.append(badge)

def addRecePointsBadge(sum, goal, badgeId, badges):
    if sum:
        if sum >= goal and not checkBadge(badgeId):
            badge = Userbadges(badge_id=badgeId, user_id=current_user.id)
            db.session.add(badge)
            badges.append(badge)


# Post num
def post_badge():
    badges = []
    addPostBadge(1,2,badges)
    addPostBadge(5,3,badges)
    addPostBadge(15,4,badges)
    addPostBadge(20,5,badges)
    addPostBadge(40,6,badges)
    db.session.commit()
    #print(badges)
    return badges
        
#  Like/Dislike num
def like_badge():
    badges = []
    addReactBadge(1,7,badges)
    addReactBadge(15,8,badges)
    addReactBadge(100,9,badges)
    addReactBadge(250,10,badges)
    addReactBadge(400,11,badges)
    db.session.commit()
    #print(badges)
    
    return badges
    
#  Like received num
def like_rece_badge():
    badges = []
    posts = current_user.posts
    sum = 0
    for post in posts:
        sum += LikePostRecord.query.filter_by(post_id=post.post_id).count()
    addRecePointsBadge(sum, 20, 12, badges)
    addRecePointsBadge(sum, 100, 13, badges)
    addRecePointsBadge(sum, 250, 14, badges)
    addRecePointsBadge(sum, 400, 15, badges)
    db.session.commit()
    
    return badges


#  Report badge
def report_badge():
    report = Userreport.query.filter_by(user_id=current_user.id).first()
    if report and not checkBadge(16):
        badge = Userbadges(badge_id=16, user_id=current_user.id)
        db.session.add(badge)
        db.session.commit()
        return badge
    else:
        pass
    
#  Points
def points_badge():
    badges = []
    sum = db.session.query(func.sum(Pointrules.add_points)).join(Userpoints).filter_by(user_id=current_user.id).all()
    #print(sum[0][0], file=sys.stdout)
    
    addRecePointsBadge(sum[0][0], 200, 17, badges)
    addRecePointsBadge(sum[0][0], 400, 18, badges)
    addRecePointsBadge(sum[0][0], 900, 19, badges)
    addRecePointsBadge(sum[0][0], 1240, 20, badges)
    
    return badges