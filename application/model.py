from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user includes Normal User, IT department, Admin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    image_file = db.Column(db.String(200), nullable=True, default='picture1.jpg')
    password = db.Column(db.String(60), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    interest = db.Column(db.String(60), nullable=False)
    qa = db.Column(db.String(40), nullable=False)
    qb = db.Column(db.String(40), nullable=False)
    qc = db.Column(db.String(40), nullable=False)
    qd = db.Column(db.String(40), nullable=False)
    qe = db.Column(db.String(40), nullable=False)
    qf = db.Column(db.String(40), nullable=False)
    qg = db.Column(db.String(40), nullable=False)
    qh = db.Column(db.String(40), nullable=False)
    qi = db.Column(db.String(40), nullable=False)
    qj = db.Column(db.String(40), nullable=False)
    qk = db.Column(db.String(40), nullable=False)
    post_count = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='user', lazy=True)
    user_report = db.relationship('Userreport', backref='user', lazy=True)
    it_report = db.relationship('Itreport', backref='user', lazy=True)
    phishresults = db.relationship('Phishingresult', backref='user', lazy=True)
    point_record = db.relationship('Userpoints', backref='user', lazy=True)
    achievement_record = db.relationship('Userachievements', backref='user', lazy=True)
    badge_record = db.relationship('Userbadges', backref='user', lazy=True)
    reward_record = db.relationship('Userrewards', backref='user', lazy=True)
    like_record = db.relationship('LikePostRecord', backref='user', lazy=True)
    dislike_record = db.relationship('DislikePostRecord', backref='user', lazy=True)
    

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.image_file}')"
    
    # get token
    def get_token(self, exp=1000):
        """
        payload : {"uid":self.id}
        """
        s = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), exp)
        return s.dumps({"uid":self.id}).decode('utf-8')

    # get sending phishing email token
    def email_token(self, exp=604800):
        """
        payload : {"uid":self.id}
        """
        emails = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), exp)
        return emails.dumps({"uid":self.id}).decode('utf-8')
    
    # since we need to determine if user liked a post already in html file, so we add this func to User class
    def liked_post(self, post_id):
        return LikePostRecord.query.filter(
                    LikePostRecord.post_id==post_id,
                    LikePostRecord.user_id==self.id).count()
        
    def disliked_post(self, post_id):
        return DislikePostRecord.query.filter(
                    DislikePostRecord.post_id==post_id,
                    DislikePostRecord.user_id==self.id).count()

    
    @staticmethod
    def verify_token(token):
        """
        docstring
        """
        s = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)["uid"]
            # This payload is decoded and safe
        except:
            return None
        # return the user obj
        return User.query.get(user_id)

    # verify phishing email token
    @staticmethod
    def verify_emailtoken(token):
        """
        docstring
        """
        emails = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = emails.loads(token)["uid"]
            # This payload is decoded and safe
        except:
            return None
        # return the user obj
        return User.query.get(user_id)


#Table to store like post id and by which user id
class LikePostRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"LikePostRecord('{self.id}', post_id:'{self.post_id}', user_id:'{self.user_id}')"
    
#Table to store dislike post id and by which user id
class DislikePostRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"DislikePostRecord('{self.id}', post_id:'{self.post_id}', user_id:'{self.user_id}')"

# IT department unique code
class Ituser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usercode = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return f"Ituser('{self.id}','{self.usercode}')"


# User post. IT depatment also can post
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like_record = db.relationship('LikePostRecord', backref='post', lazy=True)
    dislike_record = db.relationship('DislikePostRecord', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.post_id}', '{self.post_date}', '{self.post_title}', '{self.content}', '{self.user_id}')"

# User withdrawal questionnaire table
class Withdrawal(db.Model):
    withdrawal_id = db.Column(db.Integer, primary_key=True)
    withdrawal_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    qa = db.Column(db.String(40), nullable=False)
    qb = db.Column(db.String(40), nullable=False)
    qc = db.Column(db.String(40), nullable=False)
    qd = db.Column(db.String(40), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"Withdrawal('{self.withdrawal_id}', '{self.withdrawal_date}', '{self.qa}', '{self.qb}', '{self.qc}', '{self.feedback}')"

# Normal user report an attack
class Userreport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    senderemail = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    riskaction = db.Column(db.Text, nullable=False)
    reportstatus = db.Column(db.String(40), nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Userreport('{self.report_id}', '{self.subject}', '{self.senderemail}', '{self.reason}', '{self.riskaction}', '{self.reportstatus}', '{self.read}', '{self.report_date}', '{self.user_id}')"

# IT department submit a solution
class Itreport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    senderemail = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Itreport('{self.report_id}', '{self.subject}', '{self.senderemail}', '{self.reason}', '{self.solution}', '{self.report_date}', '{self.user_id}')"


# Admin Phishing campaign
class Phishingcampaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(100), unique=True, nullable=False)
    campaign_type = db.Column(db.String(100), nullable=False)
    campaign_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    phishresults = db.relationship('Phishingresult', backref='campaign', lazy=True)

    def __repr__(self):
        return f"Phishingcampaign('{self.campaign_id}', '{self.campaign_name}', '{self.campaign_type}', '{self.campaign_date}')"

# Admin check phishing campaign result. If user click the link, the phish_click = 1
class Phishingresult(db.Model):
    presult_id = db.Column(db.Integer, primary_key=True)
    phish_send = db.Column(db.Boolean, nullable=False, default=False)
    phish_click = db.Column(db.Boolean, nullable=False, default=False)
    phish_link = db.Column(db.Text, default='link')
    campaign_id = db.Column(db.Integer, db.ForeignKey('phishingcampaign.campaign_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Phishingresult('{self.presult_id}', '{self.phish_send}', '{self.phish_click}', '{self.phish_link}', '{self.campaign_id}', '{self.user_id}')"


# After Phishing simulation, if user click the link, it will save the token and the user id in this table. 
class Phishinglinkrecord(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    record_link = db.Column(db.Text, default='link')
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Phishingcampaign('{self.campaign_id}', '{self.campaign_name}', '{self.campaign_type}', '{self.campaign_date}')"

class Pointrules(db.Model):
    point_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    add_points = db.Column(db.Integer, nullable=False)
    userpoint = db.relationship('Userpoints', backref='userpoint', lazy=True)

    def __repr__(self):
        return f"pointrules('{self.point_id}', '{self.description}', '{self.add_points}')"


class Achievementrules(db.Model):
    achievement_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    add_points = db.Column(db.Integer, nullable=True)
    userachievement = db.relationship('Userachievements', backref='userachievement', lazy=True)

    def __repr__(self):
        return f"Achievementrules('{self.achievement_id}', '{self.name}', '{self.description}', '{self.add_points}')"

class Badgerules(db.Model):
    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    image_file = db.Column(db.String(200), nullable=False, default='/static/image/GamiSE.png')
    userbadge = db.relationship('Userbadges', backref='userbadge', lazy=True)

    def __repr__(self):
        return f"Badgerules('{self.badge_id}', '{self.name}', '{self.description}')"

class Rewardrules(db.Model):
    reward_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    image_file = db.Column(db.String(200), nullable=False, default='/static/image/GamiSE.png')
    userreward = db.relationship('Userrewards', backref='userreward', lazy=True)

    def __repr__(self):
        return f"Rewardrules('{self.reward_id}', '{self.name}', '{self.description}')"


class Userpoints(db.Model):
    userpoint_id = db.Column(db.Integer, primary_key=True)
    points_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    reason = db.Column(db.Text, nullable=False)
    points_id = db.Column(db.Integer, db.ForeignKey('pointrules.point_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Userpoints('{self.userpoint_id}', '{self.points_date}', '{self.reason}', '{self.points_id}'), '{self.user_id}'"


class Userachievements(db.Model):
    userachievement_id = db.Column(db.Integer, primary_key=True)
    achievement_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievementrules.achievement_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Userachievements('{self.userachievement_id}', '{self.achievement_date}', '{self.achievement_id}', '{self.user_id}')"


class Userbadges(db.Model):
    userbadge_id = db.Column(db.Integer, primary_key=True)
    badge_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    badge_id = db.Column(db.Integer, db.ForeignKey('badgerules.badge_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Userbadges('{self.userbadge_id}', '{self.badge_date}', '{self.badge_id}', '{self.user_id}')"


class Userrewards(db.Model):
    userreward_id = db.Column(db.Integer, primary_key=True)
    reward_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    reward_id = db.Column(db.Integer, db.ForeignKey('rewardrules.reward_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Userrewards('{self.userreward_id}', '{self.reward_date}', '{self.reward_id}', '{self.user_id}')"

class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=True, default='picture1.jpg')

    def __repr__(self):
        return f"Photoselect('{self.photo_id}', '{self.path}')"
