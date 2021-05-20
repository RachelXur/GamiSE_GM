from flask import Flask
from application import app, bcrypt, db
from application.model import User, Post, Userreport, Itreport, Ituser, Phishingcampaign, Phishingresult, LikePostRecord, DislikePostRecord
from application.model import Pointrules, Achievementrules, Badgerules, Rewardrules, Userpoints, Userachievements, Userbadges, Userrewards
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestPResetForm, ResetPwForm, ResetPwLoggedForm, DailyNewsForm, DailyTipsForm
from application.forms import UserReportForm, ITReportForm, ITCheckForm, SimulationForm, PointRuleForm, AchievementRuleForm, BadgeRuleForm, RewardRuleForm
from sqlalchemy import func, or_


# register achievement - 1
def register_achievement():
    form = RegistrationForm()
    currentuser = User.query.filter_by(email=form.email.data).first()
    achievementrecord = Userachievements(achievement_id=1, user_id=currentuser.id)
    db.session.add(achievementrecord)
    db.session.commit()
    return form, currentuser, achievementrecord

# post achievement - 2
def post_achievement():
    postachievement = Userachievements.query.filter(Userachievements.achievement_id == 2,Userachievements.user_id == current_user.id).all()
    postrecord = Userpoints.query.filter(Userpoints.points_id == 1, Userpoints.user_id == current_user.id).count()
    if postrecord == 10:
        if not postachievement:
            postachievementrecord = Userachievements(achievement_id=2, user_id=current_user.id)
            postachievementpoint = Userpoints(reason='The amout of the posting experience reach to 10', points_id=8, user_id=current_user.id)
            db.session.add(postachievementrecord)
            db.session.add(postachievementpoint)
            db.session.commit()
    return postachievement, postrecord

# Like or not interested achievement - 3, 4
def responsepost_achievement():
    likerecord = Userpoints.query.filter(Userpoints.user_id == current_user.id, Userpoints.point_id == 2).count()
    dislikerecord = Userpoints.query.filter(Userpoints.user_id == current_user.id, Userpoints.point_id == 3).count()
    recordcount = likerecord + dislikerecord
    postlikeachievementfirst = Userachievements.query.filter(Userachievements.achievement_id == 3, Userachievements.user_id == current_user.id).all()
    postlikeachievementsecond = Userachievements.query.filter(Userachievements.achievement_id == 4, Userachievements.user_id == current_user.id).all()
    if recordcount >= 50:
        if not postlikeachievementfirst:
            postlikeachievement = Userachievements(achievement_id=3, user_id=current_user.id)
            postlikeachievementpoint = Userpoints(reason='The amount of  clicking "Like" or "Not Interested" reach to 50', points_id=9, user_id=current_user.id)
            db.session.add(postlikeachievement)
            db.session.add(postlikeachievementpoint)
            db.session.commit()
    if recordcount >= 150:
        if not postlikeachievementsecond:
            postlikeachievement = Userachievements(achievement_id=4, user_id=current_user.id)
            postlikeachievementpoint = Userpoints(reason='The amount of  clicking "Like" or "Not Interested" reach to 50', points_id=10, user_id=current_user.id)
            db.session.add(postlikeachievement)
            db.session.add(postlikeachievementpoint)
    return likerecord, dislikerecord, recordcount, postlikeachievementfirst, postlikeachievementsecond


# Amount of like achievement - 5, 6
def belikedpost_achievement(pid):
    post = Post.query.filter_by(post_id=pid).first()
    belikedposts = db.session.query(Post.user_id, func.count(LikePostRecord.id)).outerjoin(LikePostRecord, Post.post_id == LikePostRecord.post_id).group_by(Post.user_id).filter(Post.user_id == post.user_id).all()
    #print(belikedposts)
    if belikedposts[0][1] >= 50:
        belikedachievementfirst = Userachievements.query.filter(Userachievements.achievement_id == 5, Userachievements.user_id == belikedposts[0][0]).all()
        if not belikedachievementfirst:
            belikedachievement = Userachievements(achievement_id=5, user_id=belikedposts[0][0])
            belikedpoint = Userpoints(reason='The amount of "Like" reach to 50', points_id=11, user_id=belikedposts[0][0])
            db.session.add(belikedachievement)
            db.session.add(belikedpoint)
            db.session.commit()
    if belikedposts[0][1] >= 150:
        belikedachievementsecond = Userachievements.query.filter(Userachievements.achievement_id == 6, Userachievements.user_id == belikedposts[0][0]).all()
        if not belikedachievementsecond:
            belikedachievement = Userachievements(achievement_id=6, user_id=belikedposts[0][0])
            belikedpoint = Userpoints(reason='The amount of "Like" reach to 150', points_id=12, user_id=belikedposts[0][0])
            db.session.add(belikedachievement)
            db.session.add(belikedpoint)
            db.session.commit()
    return post, belikedposts

# Amount of not interested achievement - 7, 8, 9, 10
def beunlikedpost_achievement(pid):
    post = Post.query.filter_by(post_id=pid).first()
    beunlikedposts = db.session.query(Post.user_id, func.count(DislikePostRecord.id)).outerjoin(DislikePostRecord, Post.post_id == DislikePostRecord.post_id).group_by(Post.user_id).filter(Post.user_id == post.user_id).all()
    #print(beunlikedposts)
    if beunlikedposts[0][1] >= 50:
        beunlikedachievementfirst = Userachievements.query.filter(Userachievements.achievement_id == 7, Userachievements.user_id == beunlikedposts[0][0]).all()
        if not beunlikedachievementfirst:
            beunlikedachievement = Userachievements(achievement_id=7, user_id=beunlikedposts[0][0])
            beunlikedpoint = Userpoints(reason='The amount of "Not Interested" reach to 50', points_id=13, user_id=beunlikedposts[0][0])
            db.session.add(beunlikedachievement)
            db.session.add(beunlikedpoint)
            db.session.commit()
    if beunlikedposts[0][1] >= 150:
        beunlikedachievementsecond = Userachievements.query.filter(Userachievements.achievement_id == 8, Userachievements.user_id == beunlikedposts[0][0]).all()
        if not beunlikedachievementsecond:
            beunlikedachievement = Userachievements(achievement_id=8, user_id=beunlikedposts[0][0])
            beunlikedpoint = Userpoints(reason='The amount of "Not Interested" reach to 150', points_id=14, user_id=beunlikedposts[0][0])
            db.session.add(beunlikedachievement)
            db.session.add(beunlikedpoint)
            db.session.commit()
    if beunlikedposts[0][1] >= 250:
        beunlikedachievementthird = Userachievements.query.filter(Userachievements.achievement_id == 9, Userachievements.user_id == beunlikedposts[0][0]).all()
        if not beunlikedachievementthird:
            beunlikedachievement = Userachievements(achievement_id=9, user_id=beunlikedposts[0][0])
            beunlikedpoint = Userpoints(reason='The amount of "Not Interested" reach to 250', points_id=15, user_id=beunlikedposts[0][0])
            db.session.add(beunlikedachievement)
            db.session.add(beunlikedpoint)
            db.session.commit()
    if beunlikedposts[0][1] >= 400:
        beunlikedachievementfour = Userachievements.query.filter(Userachievements.achievement_id == 10, Userachievements.user_id == beunlikedposts[0][0]).all()
        if not beunlikedachievementfour:
            beunlikedachievement = Userachievements(achievement_id=10, user_id=beunlikedposts[0][0])
            beunlikedpoint = Userpoints(reason='The amount of "Not Interested" reach to 400', points_id=16, user_id=beunlikedposts[0][0])
            db.session.add(beunlikedachievement)
            db.session.add(beunlikedpoint)
            db.session.commit()
    return post, beunlikedposts

# check the user of this post point achievement - 11, 12 (Not the login user)
def posterpoint_achievement(pid):
    post = Post.query.filter_by(post_id=pid).first()
    points = db.session.query(Userpoints.user_id, func.sum(Pointrules.add_points)).outerjoin(Pointrules, Userpoints.points_id == Pointrules.point_id).group_by(Userpoints.user_id).filter(Userpoints.user_id==post.user_id).all()
    #print(points)
    if points:
        if points[0][1] >= 320:
            #print(points[0][1])
            pointachievementfirst = Userachievements.query.filter(Userachievements.achievement_id == 11, Userachievements.user_id == points[0][0]).all()
            #print(pointachievementfirst)
            if not pointachievementfirst:
                pointachievement = Userachievements(achievement_id=11, user_id=points[0][0])
                pointpoint = Userpoints(reason='The points reach to 320', points_id=17, user_id=points[0][0])
                db.session.add(pointachievement)
                db.session.add(pointpoint)
                db.session.commit()
        if points[0][1] >= 640:
            #print(points[0][1])
            pointachievementsecond = Userachievements.query.filter(Userachievements.achievement_id == 12, Userachievements.user_id == points[0][0]).all()
            if not pointachievementsecond:
                pointachievement = Userachievements(achievement_id=12, user_id=points[0][0])
                pointpoint = Userpoints(reason='The points reach to 640', points_id=18, user_id=points[0][0])
                db.session.add(pointachievement)
                db.session.add(pointpoint)
                db.session.commit()
    return post, points

# check the login user point achievement - 11, 12
def point_achievement():
    points = db.session.query(Userpoints.user_id, func.sum(Pointrules.add_points)).outerjoin(Pointrules, Userpoints.points_id == Pointrules.point_id).group_by(Userpoints.user_id).filter(Userpoints.user_id==current_user.id).all()
    #print(points)
    if points:
        if points[0][1] >= 320:
            #print(points[0][1])
            pointachievementfirst = Userachievements.query.filter(Userachievements.achievement_id == 11, Userachievements.user_id == points[0][0]).all()
            #print(pointachievementfirst)
            if not pointachievementfirst:
                pointachievement = Userachievements(achievement_id=11, user_id=points[0][0])
                pointpoint = Userpoints(reason='The points reach to 320', points_id=17, user_id=points[0][0])
                db.session.add(pointachievement)
                db.session.add(pointpoint)
                db.session.commit()
        if points[0][1] >= 640:
            #print(points[0][1])
            pointachievementsecond = Userachievements.query.filter(Userachievements.achievement_id == 12, Userachievements.user_id == points[0][0]).all()
            if not pointachievementsecond:
                pointachievement = Userachievements(achievement_id=12, user_id=points[0][0])
                pointpoint = Userpoints(reason='The points reach to 640', points_id=18, user_id=points[0][0])
                db.session.add(pointachievement)
                db.session.add(pointpoint)
                db.session.commit()
    return points

# report amount achievement - 13
def report_achievement(pid):
    report = Userreport.query.filter_by(report_id=pid).first()
    reportcount = Userreport.query.filter(Userreport.user_id == report.user_id, Userreport.read == True).count()
    #print(report)
    #print(reportcount)
    reportachievementfirst = Userachievements.query.filter(Userachievements.achievement_id == 13, Userachievements.user_id == report.user_id).all()
    if reportcount >= 3:
        if not reportachievementfirst:
            reportachievement = Userachievements(achievement_id=13, user_id=report.user_id)
            reportpoint = Userpoints(reason='Report the SE attacks for three times.', points_id=19, user_id=report.user_id)
            db.session.add(reportachievement)
            db.session.add(reportpoint)
            db.session.commit()
    return report, reportachievementfirst