import os
import smtplib
from flask import url_for
from smtplib import SMTPException
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from application.model import User, Phishingresult, Phishingcampaign
from application.forms import SimulationForm
from application import routes
from application import db
import random
import webbrowser

def PW_Google():

    EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
    EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
    users = User.query.filter_by(position='Normal').filter_by(qi='No').all()
    form = SimulationForm()
    campaign = Phishingcampaign.query.filter_by(campaign_name=form.campaign_name.data).first()

    if users:
        for user in users:
            sender = 'Google Account Security <no-reply@account.google.com>'
            receiver = user.email
            username = user.username
            #randomly create a token
            uniquelink = routes.createphish_token(user)

            msg = MIMEMultipart("alternative")
            msg['Subject'] = 'Important changes to your Google Account and services.'
            msg['From'] = 'Google Account Security <no-reply@account.google.com>'
            msg['To'] = user.email

            html = """



            <!DOCTYPE html >
            <html lang="en-GB">
                <head>
                    <meta http-equiv=Content-Type content="text/html; charset=UTF-8">
                    <style type="text/css" nonce="H9nEFFMi1cK8iXhSv6wofg">
                    body,td,div,p,a,input 
                    {
                        font-family: arial, sans-serif;
                    }
                    </style>
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <title>Gmail - Security alert</title>
                    <style type="text/css" nonce="H9nEFFMi1cK8iXhSv6wofg">
                    body, td 
                    {
                        font-size:13px
                    } 
                    a:link, a:active 
                    {
                        color:#1155CC; text-decoration:none
                    } 
                    a:hover 
                    {
                        text-decoration:underline; 
                        cursor: pointer
                    } 
                    a:visited
                    {
                        color:#6611CC
                    } 
                    img
                    {
                        border:0px
                    } 
                    pre 
                    { 
                        white-space: pre; 
                        white-space: -moz-pre-wrap; 
                        white-space: -o-pre-wrap; 
                        white-space: pre-wrap; 
                        word-wrap: break-word; 
                        max-width: 800px; 
                        overflow: auto;
                    } 
                    .logo 
                    { 
                        left: -7px; 
                        position: relative; 
                    }
                    </style>
                </head>
                <body>
                    <table width=100% cellpadding=0 cellspacing=0 border=0 class="message">
                        <tr>
                            <td colspan=2>
                                <table width=100% cellpadding=12 cellspacing=0 border=0>
                                    <tr>
                                        <td>
                                            <div style="overflow: hidden;">
                                                <font size=-1>
                                                    <u></u>
                                                    <br><br> 
                                                </font>
                                            </div>
                                        </td>
                                    </tr>        
                                    <tr align="center">
                                        <td>
                                            <table border="0" cellspacing="0" cellpadding="0" style="padding-bottom:20px;max-width:516px;min-width:220px">
                                                <tr>
                                                    <h3> Hello, """+ username +""". </h3>
                                                    <p>
                                                        Here is an important notification about your account """+ receiver +""".
                                                    </p>
                                                </tr> 
                                                <tr>
                                                    <td width="8" style="width:8px">
                                                    </td>
                                                    <td>
                                                        <div style="border-style:solid;border-width:thin;border-color:#dadce0;border-radius:8px;padding:40px 20px" align="center" class="m_-3655603911522678998mdv2rw">
                                                            <img src="https://www.gstatic.com/images/branding/googlelogo/2x/googlelogo_color_74x24dp.png" width="74" height="24" aria-hidden="true" style="margin-bottom:16px" alt="Google">
                                                            <div style="font-family:&#39;Google Sans&#39;,Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;text-align:center;word-break:break-word">
                                                                <div style="font-size:24px">
                                                                    Your password was changed
                                                                </div>
                                                                <table align="center" style="margin-top:8px">
                                                                    <tr style="line-height:normal">
                                                                        <td align="right" style="padding-right:8px">
                                                                            <img width="20" height="20" style="width:20px;height:20px;vertical-align:sub;border-radius:50%" src="https://www.gstatic.com/accountalerts/email/anonymous_profile_photo.png" alt="">
                                                                        </td>
                                                                        <td>
                                                                            <a style="font-family:&#39;Google Sans&#39;,Roboto,RobotoDraft,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.87);font-size:14px;line-height:20px">
                                                                                """+ receiver +"""
                                                                            </a>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </div>
                                                            <div style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:20px;padding-top:20px;text-align:left">
                                                                The password for your Google Account 
                                                                <a href="mailto:"""+ receiver +"""" target="_blank" style="text-decoration:none;color:#4285f4">
                                                                    """+ receiver +"""
                                                                </a> was changed. If you didn&#39;t change it, you should 
                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" title="Setting" style="text-decoration:none;color:#4285f4">
                                                                    recover your account
                                                                </a>.
                                                            </div>
                                                        </div>
                                                        <div style="text-align:left">
                                                            <div style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center">
                                                                <div>
                                                                    You received this email to let you know about important changes to your Google Account and services.
                                                                </div>
                                                                <div style="direction:ltr">© 2020 Google LLC, 
                                                                    <a class="m_-3655603911522678998afal" style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center">
                                                                        1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
                                                                    </a>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </td>
                                                    <td width="8" style="width:8px">
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr height="32" style="height:32px">
                                        <td></td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>          
                                                                    
                                                        
            """

            content = MIMEText(html, "html")
            msg.attach(content)

            try:
                smtpObj = SMTP('smtp.fastmail.com', 465)
                smtpObj.login(EMAIL_USERFASTMAIL, EMAIL_PASSWORDFASTMAIL)
                smtpObj.sendmail(sender, receiver, msg.as_string().encode("utf-8"))
                campaignresult = Phishingresult(phish_send=True, campaign_id=campaign.campaign_id, phish_link = uniquelink, user_id=user.id)
                db.session.add(campaignresult)
                db.session.commit()
                print ("send successfully")
            except SMTPException:
                print ("Error: Enable to send mail")
    return sender, receiver, username, form, campaign, uniquelink