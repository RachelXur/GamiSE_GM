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


# Post num 2,3,4,5,6
def post_badge():
    badges = []
    addPostBadge(1,2,badges)
    addPostBadge(3,3,badges)
    addPostBadge(5,4,badges)
    addPostBadge(7,5,badges)
    addPostBadge(20,6,badges)
    db.session.commit()
    #print(badges)
    return badges
        
#  Like/Dislike num 7,8,9,10,11
def like_badge():
    badges = []
    addReactBadge(1,7,badges)
    addReactBadge(10,8,badges)
    addReactBadge(40,9,badges)
    addReactBadge(250,10,badges)
    addReactBadge(400,11,badges)
    db.session.commit()
    #print(badges)
    
    return badges
    
#  Like received num 12,13,14,15
def like_rece_badge(pid):
    post = Post.query.filter_by(post_id=pid).first()
    belikedposts = db.session.query(Post.user_id, func.count(LikePostRecord.id)).outerjoin(LikePostRecord, Post.post_id == LikePostRecord.post_id).group_by(Post.user_id).filter(Post.user_id == post.user_id).all()
    #print(belikedposts)
    if belikedposts[0][1] >= 10:
        belikedbadgefirst = Userbadges.query.filter(Userbadges.badge_id == 12, Userbadges.user_id == belikedposts[0][0]).all()
        if not belikedbadgefirst:
            belikedbadge= Userbadges(badge_id=12, user_id=belikedposts[0][0])
            db.session.add(belikedbadge)
            db.session.commit()
    if belikedposts[0][1] >= 40:
        belikedbadgesecond = Userbadges.query.filter(Userbadges.badge_id == 13, Userbadges.user_id == belikedposts[0][0]).all()
        if not belikedbadgesecond:
            belikedbadge= Userbadges(badge_id=13, user_id=belikedposts[0][0])
            db.session.add(belikedbadge)
            db.session.commit()
    if belikedposts[0][1] >= 250:
        belikedbadgethird = Userbadges.query.filter(Userbadges.badge_id == 14, Userbadges.user_id == belikedposts[0][0]).all()
        if not belikedbadgethird:
            belikedbadge= Userbadges(badge_id=14, user_id=belikedposts[0][0])
            db.session.add(belikedbadge)
            db.session.commit()
    if belikedposts[0][1] >= 400:
        belikedbadgefourth = Userbadges.query.filter(Userbadges.badge_id == 15, Userbadges.user_id == belikedposts[0][0]).all()
        if not belikedbadgefourth:
            belikedbadge= Userbadges(badge_id=15, user_id=belikedposts[0][0])
            db.session.add(belikedbadge)
            db.session.commit()
    return post, belikedposts


#  Report badge 16
def report_badge():
    report = Userreport.query.filter_by(user_id=current_user.id).first()
    if report and not checkBadge(16):
        badge = Userbadges(badge_id=16, user_id=current_user.id)
        db.session.add(badge)
        db.session.commit()
        return badge
    else:
        pass
    
#  Points 17,18,19,20 (current_user)
def points_badge():
    badges = []
    sum = db.session.query(func.sum(Pointrules.add_points)).join(Userpoints).filter_by(user_id=current_user.id).all()
    #print(sum[0][0], file=sys.stdout)
    
    addRecePointsBadge(sum[0][0], 100, 17, badges)
    addRecePointsBadge(sum[0][0], 390, 18, badges)
    addRecePointsBadge(sum[0][0], 930, 19, badges)
    addRecePointsBadge(sum[0][0], 1390, 20, badges)
    
    return badges

#  Points 17,18,19,20 (not current_user (when current user click like, check point badge of the poster))
def posterpoints_badge(pid):
    post = Post.query.filter_by(post_id=pid).first()
    points = db.session.query(Userpoints.user_id, func.sum(Pointrules.add_points)).outerjoin(Pointrules, Userpoints.points_id == Pointrules.point_id).group_by(Userpoints.user_id).filter(Userpoints.user_id==post.user_id).all()
    #print(points)
    if points:
        if points[0][1] >= 100:
            #print(points[0][1])
            pointbadgefirst = Userbadges.query.filter(Userbadges.badge_id == 17, Userbadges.user_id == points[0][0]).all()
            if not pointbadgefirst:
                pointbadge = Userbadges(badge_id=17, user_id=points[0][0])
                db.session.add(pointbadge)
                db.session.commit()
        if points[0][1] >= 390:
            #print(points[0][1])
            pointbadgefirst = Userbadges.query.filter(Userbadges.badge_id == 18, Userbadges.user_id == points[0][0]).all()
            if not pointbadgefirst:
                pointbadge = Userbadges(badge_id=18, user_id=points[0][0])
                db.session.add(pointbadge)
                db.session.commit()
        if points[0][1] >= 930:
            #print(points[0][1])
            pointbadgefirst = Userbadges.query.filter(Userbadges.badge_id == 19, Userbadges.user_id == points[0][0]).all()
            if not pointbadgefirst:
                pointbadge = Userbadges(badge_id=19, user_id=points[0][0])
                db.session.add(pointbadge)
                db.session.commit()
        if points[0][1] >= 1390:
            #print(points[0][1])
            pointbadgefirst = Userbadges.query.filter(Userbadges.badge_id == 20, Userbadges.user_id == points[0][0]).all()
            if not pointbadgefirst:
                pointbadge = Userbadges(badge_id=20, user_id=points[0][0])
                db.session.add(pointbadge)
                db.session.commit()
    return post, points