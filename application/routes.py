from flask import Flask, render_template, url_for, flash, redirect, request, abort
from sqlalchemy.sql.expression import asc
from application import app, bcrypt, db, mail
from application.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestPResetForm, ResetPwForm, ResetPwLoggedForm, DailyNewsForm, DailyTipsForm, SimulationNoteForm, PhotouploadForm, UpdateAccountPhotoForm
from application.forms import UserReportForm, ITReportForm, ITCheckForm, SimulationForm, PointRuleForm, AchievementRuleForm, BadgeRuleForm, RewardRuleForm, PickWinsForm, CheckuserForm, WithdrawalForm, PhotoselectForm
from application.newsapi.news import NewsofCA
from application.newsapi.newsinterests import NewsofInterest
from application.model import User, Post, Userreport, Itreport, Ituser, Phishingcampaign, Phishingresult, LikePostRecord, DislikePostRecord, Withdrawal, Photo, Emailchangerecord
from application.model import Pointrules, Achievementrules, Badgerules, Rewardrules, Userpoints, Userachievements, Userbadges, Userrewards, Phishinglinkrecord
from flask_login import login_user, current_user, logout_user, login_required
import secrets, sys, os
from PIL import Image
from flask_mail import Message
from application.backend.User_dailyemail_news import dailyemailnews
from application.backend.User_dailyemail_tips_noimage import dailyemailtips
from application.backend.User_dailyemail_tips_withimage import dailyemailtipsimage
from application.backend.IT_dailyemail_news import dailyemailnews_IT
from application.backend.IT_dailyemail_tips_noimage import dailyemailtips_IT
from application.backend.IT_dailyemail_tips_withimage import dailyemailtipsimage_IT
from datetime import datetime, timedelta, date
from sqlalchemy import desc, func, or_
from application.newsapi.T_Tablet_RBC import tablet_RBC
from application.newsapi.T_Tablet_ScotiaBank import tablet_Scotia
from application.newsapi.T_Tablet_TD import tablet_TD
from application.newsapi.T_Uwindsor_PWchange import PWchange
from application.newsapi.T_News_Google import Googlenews
from application.newsapi.T_Discount_Apple_Pay import Discount_Apple
from application.newsapi.T_Discount_Credit_Debit import Discount_Credit
from application.newsapi.T_Discount_Paypal import Discount_Paypal
from application.newsapi.T_PW_Google import PW_Google
from application.newsapi.T_PW_GoogleApp import PW_GoogleApp
from application.newsapi.T_News_Facebook import Facebooknews
from application.newsapi.T_News_Twitter import Twitternews
from application.backend.point_elements import register_point, post_point, likepost_point, deletelikepost_point, unlikepost_point, deleteunlikepost_point, report_point
from application.backend.point_elements import deleteuserreport_point
from application.backend.achievement_elements import register_achievement, post_achievement, responsepost_achievement, belikedpost_achievement
from application.backend.achievement_elements import point_achievement, report_achievement, beunlikedpost_achievement, posterpoint_achievement
from application.backend.badge_elements import register_badge, post_badge, like_badge, like_rece_badge, report_badge, points_badge
from application.backend.IT_simulationnote import simulation_note_IT
from application.backend.User_dailyemail_news_noimage import dailyemailnews_noimage
from application.backend.IT_dailyemail_news_noimage import dailyemailnews_IT_noimage


# schedueled job
def pickWins():
    ranklist = []
    rank = 0
    tempM = 0
    points = db.session.query(Userpoints.user_id, func.sum(Pointrules.add_points)).outerjoin(Pointrules, Userpoints.points_id == Pointrules.point_id).group_by(Userpoints.user_id).order_by(desc(func.sum(Pointrules.add_points))).all()
    #get top 3s
    for point in points:
        if rank <= 3:
            maxP = point[1]
            if tempM != maxP:
                rank = rank + 1
                tempM = maxP
            ranklist.append([rank, point[0]])
        else:
            break
    print("Schedule running, current winners :"+ str(ranklist))
    for user in ranklist:
        # date, reward id, uid
        rewardR = Userrewards(reward_date=datetime.now(), reward_id=user[0], user_id=user[1])
        db.session.add(rewardR)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    #if logged in redirect to home
    if current_user.is_authenticated:
        if current_user.position != 'Admin':
            return redirect(url_for('homepage'))
        else:
            return redirect(url_for('daily'))
    form = LoginForm()
    nexts_page = request.args.get('nexts_page')
    token = request.args.get('token')
    if form.validate_on_submit():
        #check user with db
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.confirm == True:
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                    if token:
                        userverify = User.verify_emailtoken(token)
                        if userverify == user:
                            if user.position != 'Admin':
                                #log in
                                login_user(user)
                                if nexts_page:
                                        flash('Logged in', 'success')
                                        return redirect(nexts_page) if nexts_page else redirect(url_for('homepage'))
                                else:
                                        next_page = request.args.get('next')
                                        flash('Logged in', 'success')
                                        return redirect(next_page) if next_page else redirect(url_for('homepage'))
                            else:
                                login_user(user)
                                flash('Logged in', 'success')
                                return redirect(url_for('daily'))
                        else:
                            flash('Sorry, you do not have this permission', 'danger')
                            return redirect(url_for('login', nexts_page=nexts_page, token=token))
                    else:
                        if user.position != 'Admin':
                                #log in
                                login_user(user)
                                if nexts_page:
                                    flash('Logged in', 'success')
                                    return redirect(nexts_page) if nexts_page else redirect(url_for('homepage'))
                                else:
                                    next_page = request.args.get('next')
                                    flash('Logged in', 'success')
                                    return redirect(next_page) if next_page else redirect(url_for('homepage'))
                        else:
                            login_user(user)
                            flash('Logged in', 'success')
                            return redirect(url_for('daily'))
                else:
                    flash('Login Unsuccessful. Please check username and password', 'danger')
            else:
                flash('Please confirm your registration', 'danger')
        else:
            flash('User does not exist! Please register first', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@app.route('/user/register', methods=['GET', 'POST'])
def register():
    #if logged in redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    #else register
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.position.data == 'Yes':
            itusercode = Ituser.query.filter_by(usercode=form.itusercode.data).first()
            if itusercode:
                pwHash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
                user = User(username=form.username.data, email=form.email.data, password=pwHash, position='IT',
                        interest=form.interest.data, qa=form.qa.data, qb=form.qb.data, qc=form.qc.data, qd=form.qd.data, qe=form.qe.data,
                        qf=form.qf.data, qg=form.qg.data, qh=form.qh.data, qi=form.qi.data, qj=form.qj.data, qk=form.qk.data)
                db.session.add(user)
                db.session.commit()
                registerconfirm(user)
                flash(f'Please confirm your registration {form.username.data}!', 'warning')
                return redirect(url_for('login'))
            else:
                flash('IT code is incorrect, please check it again!', 'danger')
        else:
            form.itusercode.data=0
            #hash psw
            pwHash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            #create new user
            user = User(username=form.username.data, email=form.email.data, password=pwHash, position='Normal',
                        interest=form.interest.data, qa=form.qa.data, qb=form.qb.data, qc=form.qc.data, qd=form.qd.data, qe=form.qe.data,
                        qf=form.qf.data, qg=form.qg.data, qh=form.qh.data, qi=form.qi.data, qj=form.qj.data, qk=form.qk.data)
            db.session.add(user)
            db.session.commit()
            register_point()
            register_achievement()
            register_badge()
            registerconfirm(user)
            flash(f'Please confirm your registration {form.username.data}!', 'warning')
            return redirect(url_for('login'))
    return render_template('user/register.html', title='Register', form=form)


@app.route('/register_confirm/<token>', methods=['GET', 'POST'])
def confirmtologin(token):
    if current_user.is_authenticated and token != None:
        user = User.verify_emailtoken(token)
        if current_user != user:
            logout_user()
        return redirect(url_for('confirmtologin', token=token))
    else:
        user = User.verify_emailtoken(token)
        user.confirm = True
        db.session.commit()
        flash(f'Account created for {user.username}! You are now able to login in!', 'success')
        return redirect(url_for('login'))


# send confirmation email when users register the platform. 
def registerconfirm(user):
    """
    docstring
    """
    token = createphish_token(user)
    msg = Message("Confirm Registration",
                  sender=os.environ["EMAIL_USERFASTMAIL"],
                  recipients=[user.email])
    msg.body = f''' Almost there!
                    Please click the link to confirm your regisration.
                    {url_for('confirmtologin', token=token, _external=True)}
                    This email will expire in 7 days.
                    If you have any problem, please contact support. 
                    {url_for('contact', _external=True)}.'''
    mail.send(msg)


@app.route('/user/homepage', methods=['GET', 'POST'])
@login_required
def homepage():
    today = datetime.now()
    date = today - timedelta(days=5)
    reports = Itreport.query.filter(Itreport.report_date >= date).order_by(desc(Itreport.report_date)).all()
    posts = Post.query.order_by(desc(Post.post_date)).paginate(per_page=5)
    return render_template('user/index.html', title='Homepage', reports=reports, posts=posts, date=date)


@app.route('/post/post_experience', defaults={'token': None}, methods=['GET', 'POST'])
@app.route('/post/post_experience/<token>', methods=['GET', 'POST'])
def pexperience(token):
    if not current_user.is_authenticated:
        nexts_page = '/post/post_experience'
        return redirect(url_for('login', nexts_page=nexts_page,token=token))
    form = PostForm()
    if current_user.is_authenticated and token != None:
        user = User.verify_emailtoken(token)
        if current_user != user:
            logout_user()
            return redirect(url_for('pexperience', token=token))
        else:
            return redirect(url_for('userreport'))
    else:
        usercount = User.query.filter_by(id = current_user.id).first()
        if form.validate_on_submit():
            #store post to db
            newPost = Post(post_title=form.title.data, content=form.content.data, user=current_user)
            db.session.add(newPost)
            db.session.commit()
            usercount.post_count = usercount.post_count + 1
            db.session.commit()
            if current_user.position == 'Normal':
                post_point()
                post_achievement()
                point_achievement()
            now = newPost.post_date
            flash(f"Posted {now.strftime('%Y-%m-%d %H:%M')}", 'success')
            return redirect(url_for('homepage'))
        else:
            return render_template("user/post_experience.html", form=form)
    

# to update&delete posts, we make a new page to display a single post first
@app.route('/post/<int:pid>')
@login_required
def post(pid):
   post = Post.query.get_or_404(pid)
   likecount = LikePostRecord.query.filter_by(post_id=pid).count()

   return render_template('user/post.html', post=post, likecount=likecount)


@app.route('/post/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def update_post(pid):
    form = PostForm()
    post = Post.query.get_or_404(pid)
    if post and current_user.id == post.user_id:
        if form.validate_on_submit():
            post.post_title = form.title.data
            post.content = form.content.data
            post.post_date = datetime.now()
            db.session.commit()
            now = post.post_date
            flash(f"Experience Updated {now.strftime('%Y-%m-%d %H:%M')}", 'success')
            return redirect(url_for('post', pid=pid))
        else:
            form.title.data = post.post_title
            form.content.data = post.content
        return render_template('user/post_experience.html', form=form, update="Update your experience")
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))


@app.route('/post/<int:pid>/delete', methods=['POST'])
def delete_post(pid):
    # find the post
    post = Post.query.get_or_404(pid)
    # verify user&post
    if post and current_user.id == post.user_id:
        likerecord = LikePostRecord.query.filter_by(post_id=pid).all()
        for record in likerecord:
            db.session.delete(record)
            db.session.commit()
        dislikerecord = DislikePostRecord.query.filter_by(post_id=pid).all()
        for record in dislikerecord:
            db.session.delete(record)
            db.session.commit()
        db.session.delete(post)
        db.session.commit()
        flash("Exeperience Deleted", 'success')
        return redirect(url_for('epsharing'))
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))
        


# like/unlike post
# if a post is liked => like button become gray, but the unlike will delete like record
# if disliked, 
@app.route('/post/<int:pid>/like')
def like(pid):
    # falg indicates if we want to cancel the same action
    # if liked, delete like, if not like it
    record = LikePostRecord.query.filter(LikePostRecord.post_id==pid, LikePostRecord.user_id==current_user.id).first()
    if not record:
        print('liked', file=sys.stdout)
        likeR = LikePostRecord(post_id=pid, user_id=current_user.id)
        #delete dislike if any
        dislikeR = DislikePostRecord.query.filter(DislikePostRecord.post_id==pid, DislikePostRecord.user_id==current_user.id).first()
        if dislikeR:
            db.session.delete(dislikeR)
        deleteunlikepost_point(pid)
        db.session.add(likeR)
        db.session.commit()
        if current_user.position == 'Normal':
            likepost_point(pid)
            responsepost_achievement()
            point_achievement()
            belikedpost_achievement(pid)
            posterpoint_achievement(pid)
        return 'success', 200
    else:
        # delete like record
        db.session.delete(record)
        db.session.commit()
        return 'success', 200


@app.route('/post/<int:pid>/unlike')
def unlike(pid):
    record = DislikePostRecord.query.filter(DislikePostRecord.post_id==pid, DislikePostRecord.user_id==current_user.id).first()
    if not record:
        print('unliked', file=sys.stdout)
        dislikeR = DislikePostRecord(post_id=pid, user_id=current_user.id)
        #delete like if any
        likeR = LikePostRecord.query.filter(LikePostRecord.post_id==pid, LikePostRecord.user_id==current_user.id).first()
        if likeR:
            db.session.delete(likeR)
        deletelikepost_point(pid)
        db.session.add(dislikeR)
        db.session.commit()
        if current_user.position == 'Normal':
            unlikepost_point(pid)
            responsepost_achievement()
            point_achievement()
            beunlikedpost_achievement(pid)
            posterpoint_achievement(pid)
        return 'success', 200
    else:
        # delete dislike record
        db.session.delete(record)
        db.session.commit()
        return 'success', 200


def savePic(picture, route):
    # get a random hex for file name
    rand = secrets.token_hex(8)
    # save the file ext
    _, f_ext = os.path.splitext(picture.filename)
    f_name = rand + f_ext
    if route == 1:
        # get path
        path = os.path.join(app.root_path, 'static/images', f_name)
    if route == 2:
        # get path
        path = os.path.join(app.root_path, 'static/gamification_badges', f_name)
    if route == 3:
        # get path
        path = os.path.join(app.root_path, 'static/gamification_reward', f_name)
    # resize the image to save space
    outSize = (125,125)
    outImage = Image.open(picture)
    outImage.thumbnail(outSize)
    #save
    outImage.save(path)
    
    return f_name


# send email if user change their username or email address to new address
def notechangeprofile(user):
    """
    docstring
    """
    msg = Message("Profile Updated",
                  sender=os.environ["EMAIL_USERFASTMAIL"],
                  recipients=[user.email])
    msg.body = f''' Your profile Has Been Updated!
                    This email is to let you know that the profile associated with your GamiSE account has been updated.
                    Your current username is   {user.username}
                    Your current email address is   {user.email}
                    If you did not make this change and believe your GamiSE account has been compromised, please contact support 
                    {url_for('contact', _external=True)}.'''
    mail.send(msg)


# send email if user change their username or email address to old address
def notechangeprofileold(user, email):
    """
    docstring
    """
    msg = Message("Profile Updated",
                  sender=os.environ["EMAIL_USERFASTMAIL"],
                  recipients=[email])
    msg.body = f''' Your profile Has Been Updated!
                    This email is to let you know that the profile associated with your GamiSE account has been updated.
                    Your current username is   {user.username}
                    Your current email address is   {user.email}
                    If you did not make this change and believe your GamiSE account has been compromised, please contact support 
                    {url_for('contact', _external=True)}.'''
    mail.send(msg)

       
@app.route('/user/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    images = Photo.query.all()
    useremailsave = current_user.email
    #update account info
    if form.validate_on_submit():
        # if uploaded a pic
        current_user.image_file = current_user.image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        record = Emailchangerecord(before=useremailsave, after=current_user.email)
        db.session.add(record)
        db.session.commit()
        notechangeprofile(current_user)
        notechangeprofileold(current_user, useremailsave)
        flash('Account info updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profilPic = url_for('static', filename='images/'+ current_user.image_file)
    return render_template('user/account.html', pic=profilPic, form=form, images=images)


@app.route('/user/account/pic/<int:pid>', methods=['GET', 'POST'])
@login_required
def accountphoto(pid):
    form = UpdateAccountPhotoForm()
    photo = Photo.query.get_or_404(pid)
    images = Photo.query.all()
    if form.validate_on_submit():
        current_user.image_file = photo.path
        current_user.username = current_user.username
        current_user.email = current_user.email
        db.session.commit()
        flash('Profile Photo updated', 'success')
        return redirect(url_for('account'))
    form.picture.data = photo.path
    profilPic = url_for('static', filename='images/'+ current_user.image_file)
    return render_template('user/accountchangephoto.html', pic=profilPic, form=form, photo=photo, images=images)


def sendEmail(user):
    """
    docstring
    """
    #get token for the user
    token = user.get_token()
    msg = Message("Reset Your Password",
                  sender=os.environ["EMAIL_USERFASTMAIL"],
                  recipients=[user.email])
    msg.body = f'''Please click the link below to reset your password:
                            {url_for('reset', token=token, _external=True)}
                    If you didn't request this email, ignore is and check you account security.
                    Thank you.'''
    mail.send(msg)


# change password email notification
def notechangepwd(user):
    """
    docstring
    """
    msg = Message("Password Updated",
                  sender=os.environ["EMAIL_USERFASTMAIL"],
                  recipients=[user.email])
    msg.body = f''' Your Password Has Been Updated!
                    This email is to let you know that the password associated with your GamiSE account has been updated.
                    If you did not make this change and believe your GamiSE account has been compromised, please contact support 
                    {url_for('contact', _external=True)}.'''
    mail.send(msg)


# request to reset password
# user request reset with an email address, we take it as is without telling user if it's a valid email
# if it is, we get the user obj with that email, then we generate the token (sign the data for protection)
# for that user's id. Then we send this token embedded in a url to the email, if the user get it and click
# the link, we'll receieve it via a route which we can capture that token and the validation is complete
# Then we can let user enter the new password and update the db
@app.route('/user/reset_req', methods=['GET', 'POST'])
def reset_req():
    form = RequestPResetForm()
    if form.validate_on_submit():
        targetEm = form.email.data
        # check user and send email, send email needs email and token, for token we need the user obj
        # to access the get token function
        user = User.query.filter_by(email=targetEm).first()
        sendEmail(user)
        flash("Email Sent", 'success')
    return render_template('user/requestPw.html', form=form)


@app.route('/user/reset', defaults={'token': None}, methods=['GET', 'POST'])
@app.route('/user/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    form = ResetPwForm()
    formLogged = ResetPwLoggedForm()
    if current_user.is_authenticated and token != None:
        user = User.verify_emailtoken(token)
        logout_user()
        return redirect(url_for('reset', token=token))
    else:
        if form.validate_on_submit() or formLogged.validate_on_submit():
            if form.password.data:
                # verify the token and update db
                user = User.verify_token(token)
                if user:
                    newHash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
                    user.password = newHash
                    db.session.commit()
                    notechangepwd(user)
                    return redirect(url_for('login'))
                else:
                    flash('User does not exist or this link has expired!', 'danger')
                    return redirect(url_for('login'))
            else:
                # Logged in user change password
                # verify old pw and update db
                if bcrypt.check_password_hash(current_user.password, formLogged.old_password.data):
                    newHash = bcrypt.generate_password_hash(formLogged.new_password.data).decode('utf-8')
                    current_user.password = newHash
                    db.session.commit()
                    notechangepwd(current_user)
                    logout_user()
                    flash("Password changed, please log in again.", 'success')
                    return redirect(url_for('login'))
                else:
                    flash("Incorrect Password, please try again.", 'danger')
        
        return render_template('user/resetPw.html', form=form, formLogged=formLogged)


# user submit a report when they think they face an attack
@app.route('/user/user_report', defaults={'token': None}, methods=['GET', 'POST'])
@app.route('/user/user_report/<token>', methods=['GET', 'POST'])
def userreport(token):
    if not current_user.is_authenticated:
        nexts_page = '/user/user_report'
        return redirect(url_for('login', nexts_page=nexts_page, token=token))
    form = UserReportForm()
    if current_user.is_authenticated and token != None:
        user = User.verify_emailtoken(token)
        if current_user != user:
            logout_user()
            return redirect(url_for('userreport', token=token))
        else:
            return redirect(url_for('userreport'))
    else:
        if current_user.position == 'Normal':
            form = UserReportForm()
            # count the number of the reports that submitted by current user and set the limitation
            reports = Userreport.query.filter_by(user_id=current_user.id)
            count = 0
            for report in reports:
                reportdate = report.report_date.strftime('%Y-%m-%d')
                if reportdate == str(date.today()):
                    count = count+1
            # submit and store in database userreport
            # if user click NO in the report status. Then have a flash message to remind the user report the attack.
            if form.validate_on_submit():
                if count < 3:
                    userreport = Userreport(subject=form.subject.data, reason=form.reason.data, senderemail=form.senderemail.data, riskaction=form.riskaction.data, 
                                            reportstatus=form.reportstatus.data, user=current_user)
                    db.session.add(userreport)
                    db.session.commit()
                    report_point()
                    point_achievement()
                    now = userreport.post_date
                    if form.reportstatus.data == "No":
                        flash(f"Successful Submit {now.strftime('%Y-%m-%d %H:%M')}. Please remember to forward the phishing email to IT department!", 'warning')
                        return redirect(url_for('homepage'))
                    else:
                        flash(f"Successful Submit {now.strftime('%Y-%m-%d %H:%M')}", 'success')
                        return redirect(url_for('homepage'))
                else:
                    now = datetime.now()
                    flash(f"Unseccessfully submit {now.strftime('%Y-%m-%d %H:%M')}. You already submitted 3 reports today!", 'danger')
                    return redirect(url_for('homepage'))
            else:
                return render_template("user/user_report_attack.html", title='User Report', form=form)
        elif current_user.position == 'Admin':
            return redirect(url_for('daily'))
        else:
            return redirect(url_for('homepage'))


# normal user have access to this interface to check their points record
@app.route('/user/points_account')
@login_required
def paccount():
    if current_user.position != 'Admin':
        point_achievement()
        pointsrecord = Userpoints.query.filter(Userpoints.user_id==current_user.id).order_by(desc(Userpoints.points_date)).all()
        return render_template("user/points_account.html", pointsrecord=pointsrecord)
    else:
        return redirect(url_for('daily'))


# normal user have access to this interface and check achievements
@app.route('/user/achievements_account')
@login_required
def achieveaccount():
    if current_user.position != 'Admin':
        point_achievement()
        achievementsrecord = db.session.query(Userachievements.achievement_date, Achievementrules.name, Achievementrules.description, Achievementrules.add_points).outerjoin(Achievementrules, Userachievements.achievement_id == Achievementrules.achievement_id).order_by(desc(Userachievements.achievement_date)).filter(Userachievements.user_id == current_user.id).all()
        return render_template("user/achievements_account.html", achievementsrecord=achievementsrecord)
    else:
        return redirect(url_for('daily'))    


# normal user have access to this interface and check badges
@app.route('/user/badges_account')
@login_required
def badgeaccount():
    if current_user.position != 'Admin':
        point_achievement()
        post_badge()
        like_badge()
        like_rece_badge()
        report_badge()
        points_badge()
        badgesrecord = db.session.query(Userbadges.badge_date, Badgerules.name, Badgerules.description, Badgerules.image_file).outerjoin(Badgerules, Badgerules.badge_id == Userbadges.badge_id).order_by(desc(Userbadges.badge_date)).filter(Userbadges.user_id == current_user.id).all()
        return render_template("user/badges_account.html", badgesrecord=badgesrecord)
    else:
        return redirect(url_for('daily'))


# normal user have access to this interface and check reward
@app.route('/user/rewards_account')
@login_required
def rewardaccount():
    if current_user.position != 'Admin':
        point_achievement()
        rewardsrecord = db.session.query(Userrewards.reward_date, Rewardrules.name, Rewardrules.description, Rewardrules.image_file).outerjoin(Rewardrules, Rewardrules.reward_id == Userrewards.reward_id).order_by(desc(Userrewards.reward_date)).filter(Userrewards.user_id == current_user.id).all()
        return render_template("user/rewards_account.html", rewardsrecord=rewardsrecord)
    else:
        return redirect(url_for('daily')) 


# normal user leaderboard, can check all the users total points
@app.route('/user/leaderboard')
@login_required
def leaderboard():
    if current_user.position != 'Admin':
        pointlist = []
        rank = 0
        total = 0
        points = db.session.query(Userpoints.user_id, func.sum(Pointrules.add_points)).outerjoin(Pointrules, Userpoints.points_id == Pointrules.point_id).group_by(Userpoints.user_id).order_by(desc(func.sum(Pointrules.add_points))).all()
        #print(points)
        for point in points:
            name = User.query.filter_by(id=point[0]).first()
            totalpoint = point[1]
            if total != totalpoint:
                rank = rank + 1
                total = totalpoint
            pointlist.append([rank, name.username, totalpoint])
        #print(pointlist)
        return render_template("user/leaderboard.html", pointlist=pointlist)
    else:
        return redirect(url_for('daily'))


# User gamification rules
@app.route('/user/gamification_rules', methods=['GET', 'POST'])
@login_required
def user_gamification():
    if current_user.position != 'Admin':
        pointrules = Pointrules.query.all()
        achievementrules = Achievementrules.query.all()
        badgerules = Badgerules.query.all()
        rewardrules = Rewardrules.query.all()
        return render_template('user/user_gamification.html', pointrules=pointrules, achievementrules=achievementrules, badgerules=badgerules, rewardrules=rewardrules)
    else:
        return redirect(url_for('daily'))


@app.route('/user/experience_sharing', methods=['GET', 'POST'])
@login_required
def epsharing():
    if current_user.position != 'Admin':
        postnum = Post.query.filter_by(user_id=current_user.id).count()
        posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.post_date)).paginate(per_page=5)
        return render_template("user/experience_sharing.html", posts=posts, postnum=postnum)
    else:
        return redirect(url_for('daily'))


# If User want to withdrawal, they can click the link in daily email to go to this route.
@app.route('/user/withdrawal/<token>', methods=['GET', 'POST'])
def withdrawal(token):
    form = WithdrawalForm()
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('withdrawal', token=token))
    else:
        if form.validate_on_submit() and form.qd.data == "Yes":
            user = User.verify_emailtoken(token)
            if user:
                withdrawal = Withdrawal(qa=form.qa.data, qb=form.qb.data, qc=form.qc.data, qd=form.qd.data, reason=form.reason.data, user_id=user.id, username=user.username, email=user.email)
                db.session.add(withdrawal)
                db.session.commit()
                # Delete all the information from database
                userreward = Userrewards.query.filter_by(user_id=user.id).all()
                if userreward:
                    for reward in userreward:
                        db.session.delete(reward)
                        db.session.commit()
                userbadge = Userbadges.query.filter_by(user_id=user.id).all()
                if userbadge:
                    for badge in userbadge:
                        db.session.delete(badge)
                        db.session.commit()
                userpoint = Userpoints.query.filter_by(user_id=user.id).all()
                if userpoint:
                    for point in userpoint:
                        db.session.delete(point)
                        db.session.commit()
                userachievement = Userachievements.query.filter_by(user_id=user.id).all() 
                if userachievement:
                    for achievement in userachievement:
                        db.session.delete(achievement)
                        db.session.commit()
                phishingresult = Phishingresult.query.filter_by(user_id=user.id).all() 
                if phishingresult:
                    for result in phishingresult:
                        db.session.delete(result)
                        db.session.commit()
                phishingclickrecord = Phishinglinkrecord.query.filter_by(user_id=user.id).all()
                if phishingclickrecord:
                    for record in phishingclickrecord:
                        db.session.delete(record)
                        db.session.commit()
                userreport = Userreport.query.filter_by(user_id=user.id).all() 
                if userreport:
                    for report in userreport:
                        db.session.delete(report)
                        db.session.commit()
                userlike = LikePostRecord.query.filter_by(user_id=user.id).all() 
                if userlike:
                    for like in userlike:
                        db.session.delete(like)
                        db.session.commit()
                userdislike = DislikePostRecord.query.filter_by(user_id=user.id).all() 
                if userdislike:
                    for dislike in userdislike:
                        db.session.delete(dislike)
                        db.session.commit()
                posts = Post.query.filter_by(user_id=user.id).all()
                if posts:
                    for post in posts:
                        likerecords = LikePostRecord.query.filter_by(post_id=post.post_id).all()
                        if likerecords:
                            for likerecord in likerecords:
                                db.session.delete(likerecord)
                                db.session.commit()
                        dislikerecords = DislikePostRecord.query.filter_by(post_id=post.post_id).all()
                        if dislikerecords:
                            for dislikerecord in dislikerecords:
                                db.session.delete(dislikerecord)
                                db.session.commit()
                userpost = Post.query.filter_by(user_id=user.id).all() 
                if userpost:
                    for post in userpost:
                        db.session.delete(post)
                        db.session.commit()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    flash('Successfully Withdrawal', 'success')
                    return redirect(url_for('login'))
            else:
                flash('User does not exist or this link has expired!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Please select Yes on question 3 to withdrawal the training', 'danger')
            return render_template("user/withdrawal_questionnaire.html", title='Withdrawal', form=form)


@app.route("/contact_us")
def contact():
    return render_template("user/contact_us.html")


@app.route("/Terms_and_Conditions")
def terms_conditions():
    return render_template("user/terms_conditions.html")


@app.route("/Instruction")
def instruction():
    return render_template("user/instruction.html")


# Two options. Only the IT department can have access to this interface.
@app.route('/IT/submit_a_solution', defaults={'token': None}, methods=['GET', 'POST'])
@app.route('/IT/submit_a_solution/<token>', methods=['GET', 'POST'])
@login_required
def rattack(token):
    if not current_user.is_authenticated:
        nexts_page = '/IT/submit_a_solution'
        return redirect(url_for('login', nexts_page=nexts_page,token=token))
    form = PostForm()
    if current_user.is_authenticated and token != None:
        user = User.verify_emailtoken(token)
        if current_user != user:
            logout_user()
            return redirect(url_for('rattack', token=token))
        else:
            return redirect(url_for('userreport'))
    else:
        if current_user.position == 'IT':
            return render_template("user/submit_a_solution.html")
        elif current_user.position == 'Admin':
            return redirect(url_for('daily'))
        else:
            return redirect(url_for('homepage'))


# IT department submit a solution according to the user reports
@app.route('/IT/IT_report', methods=['GET', 'POST'])
@login_required
def itreport():
    if current_user.position == 'IT':
        form = ITReportForm()
        if form.validate_on_submit():
            itreport = Itreport(subject=form.subject.data, senderemail=form.senderemail.data, reason=form.reason.data, solution=form.solution.data, user=current_user)
            db.session.add(itreport)
            db.session.commit()
            now = itreport.post_date
            flash(f"Successfully Submit {now.strftime('%Y-%m-%d %H:%M')}", 'success')
            return redirect(url_for('rattack'))
        else:
            return render_template("user/it_report_attack.html", title='IT Report', form=form)
    else:
        return redirect(url_for('homepage'))


# IT department check user reports.
@app.route('/IT/Check_User_Report', methods=['GET', 'POST'])
@login_required
def checkuserreport():
    if current_user.position == 'IT':
        reports = Userreport.query.order_by(desc(Userreport.report_date)).all()
        return render_template('user/check_user_report.html', title='Homepage', reports=reports)
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))

# IT department check a specific user report with a read button on the bottom
@app.route('/user_report/<int:pid>')
@login_required
def check_report(pid):
    if current_user.position == 'IT':
        report = Userreport.query.filter_by(report_id=pid).first()
        return render_template('user/it_read_report.html', report=report)
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))

# IT department click the read button and use this function to mark the user report read! and do not show it again.
@app.route('/user_report/<int:pid>/read', methods=['GET', 'POST'])
@login_required
def read_report(pid):
    # only IT can do this action
    if current_user.position == 'IT':
        report = Userreport.query.filter_by(report_id=pid).first()
        # set read = True then will not show on the check report page
        report.read=True
        db.session.commit()
        report_achievement(pid)
        flash("Read Success!", "success")
        return redirect(url_for('checkuserreport'))
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))

@app.route('/user_report/<int:pid>/delete', methods=['POST'])
@login_required
def delete_report(pid):
    # find the report
    report = Userreport.query.filter_by(report_id=pid).first()
    # verify user&post
    if current_user.position == 'IT':
        deleteuserreport_point(pid)
        db.session.delete(report)
        db.session.commit()
        flash("Report Deleted", 'success')
        return redirect(url_for('checkuserreport'))
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))

# IT edit IT report. Delete or update
@app.route('/ITreport/<int:pid>')
@login_required
def itreportchange(pid):
   itreport = Itreport.query.get_or_404(pid)
   return render_template('user/Itreport.html', itreport=itreport)

# update IT report
@app.route('/ITreport/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def itreportchange_update(pid):
    form = ITReportForm()
    itreport = Itreport.query.get_or_404(pid)
    if current_user.id == itreport.user_id:
        if form.validate_on_submit():
            itreport.subject = form.subject.data
            itreport.senderemail = form.senderemail.data
            itreport.reason = form.reason.data
            itreport.solution = form.solution.data
            itreport.report_date = datetime.now()
            db.session.commit()
            now = itreport.post_date
            flash(f"IT solution Updated {now.strftime('%Y-%m-%d %H:%M')}", 'success')
            return redirect(url_for('itreportchange', pid=pid))
        else:
            form.subject.data = itreport.subject
            form.senderemail.data = itreport.senderemail
            form.reason.data = itreport.reason
            form.solution.data = itreport.solution
        return render_template('user/it_report_attack.html', form=form, update="Update your IT solution")
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))

# delete IT solution
@app.route('/ITreport/<int:pid>/delete', methods=['POST'])
def itreportchange_delete(pid):
    # find the solution
    itreport = Itreport.query.get_or_404(pid)
    # verify IT&solution
    if itreport and current_user.id == itreport.user_id:
        db.session.delete(itreport)
        db.session.commit()
        flash("Solution Deleted", 'success')
        return redirect(url_for('homepage'))
    elif current_user.position == 'Admin':
        return redirect(url_for('daily'))
    else:
        return redirect(url_for('homepage'))

# 
# admin interface
# send daily email with news related to social engineering attacks
# when the admin click send, the platform will send daily news with dailyemail_news function.
@app.route('/admin/daily', methods=['GET', 'POST'])
@login_required
def daily():
    if current_user.position == 'Admin':
        return render_template("admin/daily/dailyEmail.html")
    else:
        return redirect(url_for('homepage'))

@app.route('/admin/daily/news', methods=['GET', 'POST'])
@login_required
def news():
    if current_user.position == 'Admin':
        form = DailyNewsForm()
        if form.validate_on_submit():
            if form.receiver.data == "Normal Users":
                if form.image_url.data == "":
                    dailyemailnews_noimage()
                    return redirect(url_for('daily'))
                else:
                    dailyemailnews()
                    return redirect(url_for('daily'))
            else:
                if form.image_url.data == "":
                    dailyemailnews_IT_noimage()
                    return redirect(url_for('daily'))
                else:
                    dailyemailnews_IT()
                    return redirect(url_for('daily'))
        else:
            return render_template("admin/daily/dailyNews.html", title='DailyEmailNews', form=form)
    else:
        return redirect(url_for('homepage'))



# when the admin click send, the platform will send daily tips with images by using dailyemailtips function.
# when the admin click send, the platform will send daily tips without images by using dailyemailtipsimage function.
@app.route('/admin/daily/tips', methods=['GET', 'POST'])
@login_required
def tips():
    if current_user.position == 'Admin':
        form = DailyTipsForm()
        if form.validate_on_submit():
            if form.receiver.data == "Normal Users":
                if form.image_url.data == "":
                    dailyemailtips()
                    return redirect(url_for('daily'))
                else:
                    dailyemailtipsimage()
                    return redirect(url_for('daily'))
            else:
                if form.image_url.data == "":
                    dailyemailtips_IT()
                    return redirect(url_for('daily'))
                else:
                    dailyemailtipsimage_IT()
                    return redirect(url_for('daily'))
        else:
            return render_template("admin/daily/dailyTips.html", title='DailyEmailTips', form=form)
    else:
        return redirect(url_for('homepage'))

# Admin end phishing simulation notification to IT department
@app.route('/admin/daily/simulation_note', methods=['GET', 'POST'])
@login_required
def simulation_note():
    if current_user.position == 'Admin':
        form = SimulationNoteForm()
        if form.validate_on_submit():
            simulation_note_IT()
            return redirect(url_for('daily'))
        else:
            return render_template("admin/daily/simulation_note.html", title='Phishing Simulation Notification', form=form)
    else:
        return redirect(url_for('homepage'))

@app.route('/admin/simulation', methods=['GET', 'POST'])
@login_required
def simulation():
    if current_user.position == 'Admin':
        form = SimulationForm()
        if form.validate_on_submit():
            if form.phishing_type.data == 'Tablet':
                campaign = Phishingcampaign(campaign_name=form.campaign_name.data, campaign_type=form.phishing_type.data)
                db.session.add(campaign)
                db.session.commit()
                usersrbc = User.query.filter_by(position='Normal').filter_by(qc='RBC').all()
                if usersrbc:
                    tablet_RBC(usersrbc)
                usersscotia = User.query.filter_by(position='Normal').filter_by(qc='Scotia Bank').all()
                if usersscotia:
                    tablet_Scotia(usersscotia)
                userstd = User.query.filter_by(position='Normal').filter_by(qc='TD').all()
                if userstd:
                    tablet_TD(userstd)
                flash('Successfully Send', 'success')
                return redirect(url_for('result'))
            if form.phishing_type.data == 'MFA PWD':
                campaign = Phishingcampaign(campaign_name=form.campaign_name.data, campaign_type=form.phishing_type.data)
                db.session.add(campaign)
                db.session.commit()
                userspw = User.query.filter_by(position='Normal').all()
                if userspw:
                    PWchange(userspw)
                flash('Successfully Send', 'success')
                return redirect(url_for('result'))
            if form.phishing_type.data == 'Google News':
                campaign = Phishingcampaign(campaign_name=form.campaign_name.data, campaign_type=form.phishing_type.data)
                db.session.add(campaign)
                db.session.commit()
                usersgoogle = User.query.filter_by(position='Normal').all()
                if usersgoogle:
                    Googlenews(usersgoogle)
                flash('Successfully Send', 'success')
                return redirect(url_for('result'))
            if form.phishing_type.data == 'Discount':
                campaign = Phishingcampaign(campaign_name=form.campaign_name.data, campaign_type=form.phishing_type.data)
                db.session.add(campaign)
                db.session.commit()
                usersapple = User.query.filter_by(position='Normal').filter_by(qd='Apple Pay').all()
                if usersapple:
                    Discount_Apple(usersapple)
                userscredit = User.query.filter_by(position='Normal').filter_by(qd='Credit/Debit').all()
                if userscredit:
                    Discount_Credit(userscredit)
                userspaypal = User.query.filter_by(position='Normal').filter_by(qd='Paypal').all()
                if userspaypal:
                    Discount_Paypal(userspaypal)
                flash('Successfully Send', 'success')
                return redirect(url_for('result'))
            if form.phishing_type.data == 'Change PWD':
                campaign = Phishingcampaign(campaign_name=form.campaign_name.data, campaign_type=form.phishing_type.data)
                db.session.add(campaign)
                db.session.commit()
                userspwgoogle = User.query.filter_by(position='Normal').filter_by(qi='No').all()
                if userspwgoogle:
                    PW_Google(userspwgoogle)
                usersgoogleapp = User.query.filter_by(position='Normal').filter_by(qi='Yes').all()
                if usersgoogleapp:
                    PW_GoogleApp(usersgoogleapp)
                flash('Successfully Send', 'success')
                return redirect(url_for('result'))
            if form.phishing_type.data == 'Trending News':
                campaign = Phishingcampaign(campaign_name=form.campaign_name.data, campaign_type=form.phishing_type.data)
                db.session.add(campaign)
                db.session.commit()
                usersfacebook = User.query.filter_by(position='Normal').filter_by(qb='Facebook').all()
                if usersfacebook:
                    Facebooknews(usersfacebook)
                userstwitter = User.query.filter_by(position='Normal').filter_by(qb='Twitter').all()
                if userstwitter:
                    Twitternews(userstwitter)
                flash('Successfully Send', 'success')
                return redirect(url_for('result'))
            else:
                flash('No template founded', 'danger')
                return redirect(url_for('result'))
        else:
            return render_template('admin/simulation.html', form=form)
    else:
        return redirect(url_for('homepage'))

# phishing email token link create
def createphish_token(user):
    phish_token = user.email_token()
    return phish_token

# phishing email link. If user click the link, will go to this function and save the token in the database
@app.route('/check_notification/<token>', methods=['GET', 'POST'])
def check_phishlink(token):
    user = User.verify_emailtoken(token)
    existrecord = Phishinglinkrecord.query.filter(Phishinglinkrecord.user_id==user.id, Phishinglinkrecord.record_link==token).all()
    if not existrecord:
        record = Phishinglinkrecord(record_link=token, user_id=user.id)
        db.session.add(record)
        db.session.commit()
    click = Phishingresult.query.filter(Phishingresult.user_id==user.id, Phishingresult.phish_link==token).first()
    if click and click.phish_click == False:
        click.phish_click = True
        db.session.commit()
        clickrecord = Userpoints(reason='Click the fake hyperlink in phishing simulation' + ' "' + click.campaign.campaign_name + '"', points_id=5, user_id=click.user_id)
        db.session.add(clickrecord)
        db.session.commit()
    if current_user != user:
        logout_user()
        return render_template('user/phishing_notification.html',token=token)
    return render_template('user/phishing_notification.html',token=token)

# Every time when admin check the result, it will run the Click function first.
# Click function is aim to find the match uniquelink num and change the phish_click and phish_open in the database to TRUE
# Next, show it on the platform.
@app.route('/admin/result', methods=['GET', 'POST'])
@login_required
def result():
    if current_user.position == 'Admin':
        resultdict = {}
        campaigns = Phishingcampaign.query.all()
        reportnum = Userreport.query.filter_by(read=True).count()
        for campaign in campaigns:
            campaign_id = campaign.campaign_id
            campaign_name = campaign.campaign_name
            result_send = Phishingresult.query.filter(Phishingresult.campaign_id==campaign.campaign_id, Phishingresult.phish_send==True).count()
            result_click = Phishingresult.query.filter(Phishingresult.campaign_id==campaign.campaign_id, Phishingresult.phish_click==True).count()
            if campaign_name not in resultdict:
                resultdict[campaign_id] = [campaign_name, result_send, result_click]
            else:
                resultdict[campaign_name].append([campaign_name, result_send, result_click])
        return render_template("admin/result.html", campaigns=campaigns, resultdict=resultdict, reportnum=reportnum)
    else:
        return redirect(url_for('homepage'))

# Admin reset password
@app.route('/admin/reset', methods=['GET', 'POST'])
def admin_reset():
    if current_user.position == 'Admin':
        formLogged = ResetPwLoggedForm()
        # Logged in user change password
        # verify old pw and update db
        if formLogged.validate_on_submit():
            if bcrypt.check_password_hash(current_user.password, formLogged.old_password.data):
                newHash = bcrypt.generate_password_hash(formLogged.new_password.data).decode('utf-8')
                current_user.password = newHash
                db.session.commit()
                notechangepwd(current_user)
                logout_user()
                flash("Password changed, please log in again.", 'success')
                return redirect(url_for('login'))
            else:
                flash("Incorrect Password, please try again.", 'danger')
    
        return render_template('admin/admin_resetPw.html', formLogged=formLogged)
    else:
        return redirect(url_for('homepage'))

# admin account change profile or password
@app.route('/admin/account', methods=['GET', 'POST'])
@login_required
def adminaccount():
    if current_user.position == 'Admin':
        form = UpdateAccountForm()
        images = Photo.query.all()
        useremailsave = current_user.email
        #update account info
        if form.validate_on_submit():
            # if uploaded a pic
            current_user.image_file = current_user.image_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            record = Emailchangerecord(before=useremailsave, after=current_user.email)
            db.session.add(record)
            db.session.commit()
            notechangeprofile(current_user)
            notechangeprofileold(current_user, useremailsave)
            flash('Account info updated', 'success')
            return redirect(url_for('adminaccount'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        profilPic = url_for('static', filename='images/'+ current_user.image_file)
        return render_template('admin/adminaccount.html', pic=profilPic, form=form, images=images)
    else:
        return redirect(url_for('homepage'))

# change Admin photo
@app.route('/admin/account/pic/<int:pid>', methods=['GET', 'POST'])
@login_required
def adminaccountphoto(pid):
    if current_user.position == 'Admin':
        form = UpdateAccountPhotoForm()
        photo = Photo.query.get_or_404(pid)
        images = Photo.query.all()
        if form.validate_on_submit():
            current_user.image_file = photo.path
            current_user.username = current_user.username
            current_user.email = current_user.email
            db.session.commit()
            flash('Profile Photo updated', 'success')
            return redirect(url_for('adminaccount'))
        form.picture.data = photo.path
        profilPic = url_for('static', filename='images/'+ current_user.image_file)
        return render_template('admin/adminaccountchangephoto.html', pic=profilPic, form=form, photo=photo, images=images)
    else:
        return redirect(url_for('homepage'))

# upload user profile img
@app.route('/admin/photoupload', methods=['GET', 'POST'])
@login_required
def photoselect():
    if current_user.position == 'Admin':
        form = PhotouploadForm()
        #update account info
        if form.validate_on_submit():
            # if uploaded a pic
            #print('Picture submitted', file=sys.stdout)
            f_name = savePic(form.picture.data,1)
            path = f_name
            photo = Photo(path = path)
            db.session.add(photo)
            db.session.commit()
            flash('Upload successful', 'success')
            return redirect(url_for('photoselect'))
        return render_template('admin/photoupload.html', form=form)
    else:
        return redirect(url_for('homepage'))

# admin check rules
@app.route('/admin/gamification', methods=['GET', 'POST'])
@login_required
def gamification():
    if current_user.position == 'Admin':
        pointrules = Pointrules.query.order_by(asc(Pointrules.point_id)).all()
        achievementrules = Achievementrules.query.order_by(asc(Achievementrules.achievement_id)).all()
        badgerules = Badgerules.query.order_by(asc(Badgerules.badge_id)).all()
        rewardrules = Rewardrules.query.order_by(asc(Rewardrules.reward_id)).all()
        return render_template('admin/gamification.html', pointrules=pointrules, achievementrules=achievementrules, badgerules=badgerules, rewardrules=rewardrules)
    else:
        return redirect(url_for('homepage'))

# admin add point rules
@app.route('/admin/gamification/add_pointrules', methods=['GET', 'POST'])
@login_required
def addpointrule():
    if current_user.position == 'Admin':
        form = PointRuleForm()
        if form.validate_on_submit():
            pointrule = Pointrules(description=form.description.data, add_points=form.addpoints.data)
            db.session.add(pointrule)
            db.session.commit()
            flash('Successfully Added', 'success')
            return redirect(url_for('gamification'))
        else:
            return render_template('admin/add_point_rule.html', form=form)
    else:
        return redirect(url_for('homepage'))

# admin point check, which can edit, delete the points rules
@app.route('/admin/gamification/point_rule/<int:pid>')
@login_required
def check_pointrule(pid):
    if current_user.position == 'Admin':
        pointrule = Pointrules.query.filter_by(point_id=pid).first()
        return render_template('admin/check_point_rule.html', pointrule=pointrule)
    else:
        return redirect(url_for('homepage'))

# update admin gamification rules
@app.route('/admin/gamification/point_rule/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def pointrule_update(pid):
    if current_user.position == "Admin":
        form = PointRuleForm()
        pointrule = Pointrules.query.get_or_404(pid)
        if form.validate_on_submit():
            pointrule.description = form.description.data
            pointrule.add_points = form.addpoints.data
            db.session.commit()
            flash("Point Rule Updated", 'success')
            return redirect(url_for('check_pointrule', pid=pid))
        else:
            form.description.data = pointrule.description
            form.addpoints.data = pointrule.add_points
        return render_template('admin/add_point_rule.html', form=form, update="Update Point Rule")
    else:
        return redirect(url_for('homepage'))

# delete admin gamification rules
@app.route('/admin/gamification/point_rule/<int:pid>/delete', methods=['POST'])
def pointrule_delete(pid):
    # find the solution
    pointrule = Pointrules.query.get_or_404(pid)
    # verify IT&solution
    if pointrule and current_user.position == "Admin":
        db.session.delete(pointrule)
        db.session.commit()
        flash("Point Rule Deleted", 'success')
        return redirect(url_for('gamification'))
    else:
        abort(404)    

# admin add achievement rules
@app.route('/admin/gamification/add_achivementrules', methods=['GET', 'POST'])
@login_required
def addachievementrule():
    if current_user.position == 'Admin':
        form = AchievementRuleForm()
        if form.validate_on_submit():
            achievementrule = Achievementrules(name=form.name.data, description=form.description.data, add_points=form.addpoints.data)
            db.session.add(achievementrule)
            db.session.commit()
            flash('Successfully Added', 'success')
            return redirect(url_for('gamification'))
        else:
            return render_template("admin/add_achievement_rule.html", form=form)
    else:
        return redirect(url_for('homepage'))

# admin achievement check, which can edit, delete the achivements rules
@app.route('/admin/gamification/achievement_rule/<int:pid>')
@login_required
def check_achievementrule(pid):
    if current_user.position == 'Admin':
        achievementrule = Achievementrules.query.filter_by(achievement_id=pid).first()
        return render_template('admin/check_achievement_rule.html', achievementrule=achievementrule)
    else:
        return redirect(url_for('homepage'))

# update admin gamification rules
@app.route('/admin/gamification/achievement_rule/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def achievementrule_update(pid):
    if current_user.position == 'Admin':
        form = AchievementRuleForm()
        achievementrule = Achievementrules.query.get_or_404(pid)
        if form.validate_on_submit():
            achievementrule.name = form.name.data
            achievementrule.description = form.description.data
            achievementrule.add_points = form.addpoints.data
            db.session.commit()
            flash("Achievement Rule Updated", 'success')
            return redirect(url_for('check_achievementrule', pid=pid))
        else:
            form.name.data = achievementrule.name
            form.description.data = achievementrule.description
            form.addpoints.data = achievementrule.add_points
        return render_template('admin/add_achievement_rule.html', form=form, update="Update Achievement Rules")
    else:
        return redirect(url_for('homepage'))

# delete admin gamification rules
@app.route('/admin/gamification/achievement_rule/<int:pid>/delete', methods=['POST'])
def achievementrule_delete(pid):
    # find the solution
    achievementrule = Achievementrules.query.get_or_404(pid)
    # verify IT&solution
    if achievementrule and current_user.position == "Admin":
        db.session.delete(achievementrule)
        db.session.commit()
        flash("Achievement Rule Deleted", 'success')
        return redirect(url_for('gamification'))
    else:
        abort(404)

# admin add badge rules
@app.route('/admin/gamification/add_badgerules', methods=['GET', 'POST'])
@login_required
def addbadgerule():
    if current_user.position == 'Admin':
        form = BadgeRuleForm()
        if form.validate_on_submit():
            f_name = savePic(form.image_file.data, 2)
            badgerule = Badgerules(name=form.name.data, description=form.description.data, image_file=f_name)
            db.session.add(badgerule)
            db.session.commit()
            flash('Successfully Added', 'success')
            return redirect(url_for('gamification'))
        else:
            return render_template("admin/add_badge_rule.html", form=form)
    else:
        return redirect(url_for('homepage'))

# admin badge check, which can edit, delete the badge rules
@app.route('/admin/gamification/badge_rule/<int:pid>')
@login_required
def check_badgerule(pid):
    if current_user.position == 'Admin':
        badgerule = Badgerules.query.filter_by(badge_id=pid).first()
        return render_template('admin/check_badge_rule.html', badgerule=badgerule)
    else:
        return redirect(url_for('homepage'))

# update admin gamification rules
@app.route('/admin/gamification/badge_rule/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def badgerule_update(pid):
    form = BadgeRuleForm()
    badgerule = Badgerules.query.get_or_404(pid)
    if badgerule and current_user.position == "Admin":
        # update badge rules
        if form.validate_on_submit():
            # if uploaded a pic
            if form.image_file.data:
                #print('Picture submitted', file=sys.stdout)
                f_name = savePic(form.image_file.data, 2)
                badgerule.image_file = f_name
            badgerule.name = form.name.data
            badgerule.description = form.description.data
            db.session.commit()
            flash('Badge Rule updated', 'success')
            return redirect(url_for('check_badgerule', pid=pid))
        elif request.method == 'GET':
            form.name.data = badgerule.name
            form.description.data = badgerule.description
        image_file = url_for('static', filename='gamification_badges/'+ badgerule.image_file)
        return render_template('admin/add_badge_rule.html', form=form, image_file=image_file)
    else:
        return redirect(url_for('homepage'))

# delete admin gamification rules
@app.route('/admin/gamification/badge_rule/<int:pid>/delete', methods=['POST'])
def badgerule_delete(pid):
    # find the solution
    badgerule = Badgerules.query.get_or_404(pid)
    # verify IT&solution
    if badgerule and current_user.position == "Admin":
        db.session.delete(badgerule)
        db.session.commit()
        flash("Badge Rule Deleted", 'success')
        return redirect(url_for('gamification'))
    else:
        abort(404)

# admin add reward rules
@app.route('/admin/gamification/add_reward_rule', methods=['GET', 'POST'])
@login_required
def addrewardrule():
    if current_user.position == 'Admin':
        form = RewardRuleForm()
        if form.validate_on_submit():
            f_name = savePic(form.image_file.data, 3)
            rewardrule = Rewardrules(name=form.name.data, description=form.description.data, image_file=f_name)
            db.session.add(rewardrule)
            db.session.commit()
            flash('Successfully Added', 'success')
            return redirect(url_for('gamification'))
        else:
            return render_template("admin/add_reward_rule.html", form=form)
    else:
        return redirect(url_for('homepage'))

# admin reward check, which can edit, delete the reward rules
@app.route('/admin/gamification/reward_rule/<int:pid>')
@login_required
def check_rewardrule(pid):
    if current_user.position == 'Admin':
        rewardrule = Rewardrules.query.filter_by(reward_id=pid).first()
        return render_template('admin/check_reward_rule.html', rewardrule=rewardrule)
    else:
        return redirect(url_for('homepage'))

# update admin gamification rules
@app.route('/admin/gamification/reward_rule/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def rewardrule_update(pid):
    form = RewardRuleForm()
    rewardrule = Rewardrules.query.get_or_404(pid)
    if rewardrule and current_user.position == "Admin":
        # update reward rules
        if form.validate_on_submit():
            # if uploaded a pic
            if form.image_file.data:
                #print('Picture submitted', file=sys.stdout)
                f_name = savePic(form.image_file.data, 2)
                rewardrule.image_file = f_name
            rewardrule.name = form.name.data
            rewardrule.description = form.description.data
            db.session.commit()
            flash('Reward Rule updated', 'success')
            return redirect(url_for('check_rewardrule', pid=pid))
        elif request.method == 'GET':
            form.name.data = rewardrule.name
            form.description.data = rewardrule.description
        image_file = url_for('static', filename='gamification_reward/'+ rewardrule.image_file)
        return render_template('admin/add_reward_rule.html', form=form, image_file=image_file)
    else:
        return redirect(url_for('homepage'))

# delete admin gamification reward rules
@app.route('/admin/gamification/reward_rule/<int:pid>/delete', methods=['POST'])
def rewardrule_delete(pid):
    # find the solution
    rewardrule = Rewardrules.query.get_or_404(pid)
    # verify IT&solution
    if rewardrule and current_user.position == "Admin":
        db.session.delete(rewardrule)
        db.session.commit()
        flash("Reward Rule Deleted", 'success')
        return redirect(url_for('gamification'))
    else:
        abort(404)

# Admin check user leaderboard
@app.route("/admin/leaderboard", methods=['GET', 'POST'])
@login_required
def admin_leaderboard():
    if current_user.position == 'Admin':
        pointlist = []
        rank = 0
        total = 0
        points = db.session.query(Userpoints.user_id, func.sum(Pointrules.add_points)).outerjoin(Pointrules, Userpoints.points_id == Pointrules.point_id).group_by(Userpoints.user_id).order_by(desc(func.sum(Pointrules.add_points))).all()
        print(points)
        for point in points:
            name = User.query.filter_by(id=point[0]).first()
            totalpoint = point[1]
            if total != totalpoint:
                rank = rank + 1
                total = totalpoint
            pointlist.append([rank, name.username, totalpoint])
        print(pointlist)
        form = PickWinsForm()
        if form.validate_on_submit():
            pickWins()
        return render_template("admin/adminside_leaderboard.html", pointlist=pointlist, form=form)
    else:
        return redirect(url_for('homepage'))

#check user rewards
@app.route("/admin/userrewards", methods=['GET', 'POST'])
@login_required
def admin_userreward():
    if current_user.position == 'Admin':
        winlist = []
        wins = Userrewards.query.order_by(desc(Userrewards.reward_date)).all()
        for win in wins:
            name = User.query.filter_by(id=win.user_id).first()
            date = win.reward_date.strftime('%Y-%m-%d')
            reward = Rewardrules.query.filter_by(reward_id=win.reward_id).first()
            winlist.append([name.username, date, reward.name])
        return render_template("admin/admincheckuserrewards.html", winlist=winlist)
    else:
        return redirect(url_for('homepage'))

# Admin Withdrawal. Only admin can click this button to delete all the information about one user.
@app.route('/admin/user_information', methods=['GET', 'POST'])
def check_user():
    # Find all the information about this user
    if current_user.position == "Admin":
        form = CheckuserForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            return render_template('admin/admin_check_user.html', user=user, pid=user.id)
        else:
            return render_template('admin/admin_check_user.html', form=form, user=None)
    else:
        return redirect(url_for('homepage'))

# delete user information
@app.route('/admin/user_information_delete/<int:pid>', methods=['GET', 'POST'])
def userinformation_delete(pid):
    # Find all the information about this user
    if current_user.position == "Admin":
        form = CheckuserForm()
        user = User.query.filter_by(id=pid).first()
        itreport = Itreport.query.filter_by(user_id=user.id).all()
        if itreport:
            for report in itreport:
                db.session.delete(report)
                db.session.commit()
        userreward = Userrewards.query.filter_by(user_id = user.id).all()
        if userreward:
            for reward in userreward:
                db.session.delete(reward)
                db.session.commit()
        userbadge = Userbadges.query.filter_by(user_id = user.id).all()
        if userbadge:
            for badge in userbadge:
                db.session.delete(badge)
                db.session.commit()
        userpoint = Userpoints.query.filter_by(user_id=user.id).all()
        if userpoint:
            for point in userpoint:
                db.session.delete(point)
                db.session.commit()
        userachievement = Userachievements.query.filter_by(user_id=user.id).all() 
        if userachievement:
            for achievement in userachievement:
                db.session.delete(achievement)
                db.session.commit()
        phishingresult = Phishingresult.query.filter_by(user_id=user.id).all() 
        if phishingresult:
            for result in phishingresult:
                db.session.delete(result)
                db.session.commit()
        phishingclickrecord = Phishinglinkrecord.query.filter_by(user_id=user.id).all()
        if phishingclickrecord:
            for record in phishingclickrecord:
                db.session.delete(record)
                db.session.commit()
        userreport = Userreport.query.filter_by(user_id=user.id).all() 
        if userreport:
            for report in userreport:
                db.session.delete(report)
                db.session.commit()
        userlike = LikePostRecord.query.filter_by(user_id=user.id).all() 
        if userlike:
            for like in userlike:
                db.session.delete(like)
                db.session.commit()
        userdislike = DislikePostRecord.query.filter_by(user_id=user.id).all() 
        if userdislike:
            for dislike in userdislike:
                db.session.delete(dislike)
                db.session.commit()
        posts = Post.query.filter_by(user_id=user.id).all()
        if posts:
            for post in posts:
                likerecords = LikePostRecord.query.filter_by(post_id=post.post_id).all()
                if likerecords:
                    for likerecord in likerecords:
                        db.session.delete(likerecord)
                        db.session.commit()
                dislikerecords = DislikePostRecord.query.filter_by(post_id=post.post_id).all()
                if dislikerecords:
                    for dislikerecord in dislikerecords:
                        db.session.delete(dislikerecord)
                        db.session.commit()
        userpost = Post.query.filter_by(user_id=user.id).all() 
        if userpost:
            for post in userpost:
                db.session.delete(post)
                db.session.commit()
        if user:
            db.session.delete(user)
            db.session.commit()

        flash("User Deleted", 'success')
        return redirect(url_for('check_user'))
    else:
        return redirect(url_for('homepage'))

# User log out
@app.route("/user/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))






















    



