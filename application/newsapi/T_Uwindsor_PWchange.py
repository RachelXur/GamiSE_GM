import os
import smtplib
from flask import url_for
from smtplib import SMTPException
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.model import User, Phishingresult, Phishingcampaign
from application.forms import SimulationForm
from application import routes
from application import db
import random
import webbrowser

def PWchange(userspw):
    form = SimulationForm()
    campaign = Phishingcampaign.query.filter_by(campaign_name=form.campaign_name.data).first()
    for user in userspw:
        sender = 'IT services <noreply@uwindsor.ca>'
        receiver = [user.email]
        username = user.username
        #randomly create a token
        uniquelink = routes.createphish_token(user)

        EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
        EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "MFA Password Malicious Acticity"
        msg["From"] = 'IT services <noreply@uwindsor.ca>'
        msg["To"] = user.email

        html = """
        <!DOCTYPE html>
        <html lang="en-GB">
        <head>
        <meta http-equiv=Content-Type content="text/html; charset=UTF-8">
            <style type="text/css" nonce="BOBlc+hlRjdIGW1093nMfw">
            body,td,div,p,a,input 
            {
                font-family: arial, sans-serif;
            }
            </style>
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>Gmail - Fwd: Action Required: Set up your MFA options</title>
            <style type="text/css" nonce="BOBlc+hlRjdIGW1093nMfw">
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
                color:##6611CC
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
                <div class="bodycontainer">
                    <div class="maincontent">
                        <table width=100% cellpadding=0 cellspacing=0 border=0 class="message">
                            <tr>
                                <td colspan=2>
                                    <table width=100% cellpadding=12 cellspacing=0 border=0>
                                        <tr>
                                            <td>
                                                <div style="overflow: hidden;">
                                                    <font size=-1>
                                                        <div dir="ltr">
                                                            <br>
                                                            <br>
                                                            <div lang="EN-CA" link="#0563C1" vlink="#954F72">
                                                                <div>
                                                                    <p style="margin:0cm;margin-bottom:.0001pt;vertical-align:baseline">
                                                                        <span>
                                                                            <p lang="EN-US" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                Hello, """+ username +"""
                                                                                <b><u></u><u></u></b>
                                                                            </p>
                                                                        </span>
                                                                    </p>
                                                                    <p style="margin:0cm;margin-bottom:.0001pt;vertical-align:baseline">
                                                                        <span>
                                                                            <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                Multi-factor authentication (MFA) has enabled on your UWin Account for several months.
                                                                                <b><u></u><u></u></b>
                                                                            </span>
                                                                        </span>
                                                                    </p>
                                                                    <p style="margin:0cm;margin-bottom:.0001pt;vertical-align:baseline">
                                                                        <span>
                                                                            <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                <u></u> <u></u>
                                                                            </span>
                                                                        </span>
                                                                    </p>
                                                                    <p style="margin:0cm;margin-bottom:.0001pt;vertical-align:baseline">
                                                                        <span>
                                                                            <p style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                IT Services’ records show your account has changed password.<br>
                                                                            </p>
                                                                        </span>
                                                                        <span>
                                                                            <p style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                If it is you, please ignore this email.<br>
                                                                            </p>
                                                                        </span>
                                                                        <span>
                                                                            <p style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif"> 
                                                                                <strong>If it is not you, please check your account status and change the password. </strong>
                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" target="_blank" style="font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif;">
                                                                                    Click here to change the password.
                                                                                </a>
                                                                            </p>
                                                                        </span>
                                                                    </p>
                                                                    <p style="margin:0cm;margin-bottom:.0001pt;vertical-align:baseline">
                                                                        <span>
                                                                            <span style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                <u></u> <u></u>
                                                                            </span>
                                                                        </span>
                                                                    </p>
                                                                    <p style="margin:0cm;margin-bottom:.0001pt;vertical-align:baseline">
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            <b>
                                                                                <br><br>
                                                                                Signing in with MFA
                                                                                <u></u><u></u>
                                                                            </b>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            After MFA has been enabled, if you need to access Blackboard, Office 365, or UWinsite Student from an off-campus location you will be prompted for your:
                                                                            <u></u><u></u>
                                                                        </p>
                                                                        <ol style="margin-top:0cm" start="1" type="1">
                                                                            <li style="margin-left:0cm" >
                                                                                <a href="mailto:MFA@uwindsor.ca" target="_blank" style="font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif;">
                                                                                    UWinID@uwindsor.ca
                                                                                </a> 
                                                                                <u></u><u></u>
                                                                            </li>
                                                                            <li style="margin-left:0cm">
                                                                                <p style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">UWin Account password</p>
                                                                                <u></u><u></u>
                                                                            </li>
                                                                            <li style="margin-left:0cm" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                <p style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                    Secondary authentication token (a six-digit verification code texted or shared with you 
                                                                                    if you signed up for text messaging or the Microsoft Authenticator app)
                                                                                </p>
                                                                                <u></u><u></u>
                                                                            </li>
                                                                        </ol>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            Once these credentials and token are entered, you’ll be able to access UWindsor’s MFA-protected online resources.
                                                                            <u></u><u></u>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            For complete details about signing in with MFA, please 
                                                                            <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" target="_blank" style="font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif;">
                                                                                review this article
                                                                            </a>. 
                                                                            <u></u><u></u>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            <b>
                                                                                UWin Account Password
                                                                                <u></u><u></u>
                                                                            </b>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            With MFA enabled on your UWin Account, your password change interval will be extended from 120 days (or once per semester) to 365 days (or once per year).
                                                                            <u></u><u></u>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            <b>
                                                                                MFA Assistance
                                                                                <u></u><u></u>
                                                                            </b>
                                                                        </p>
                                                                        <p class="MsoNormal" style="margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal;vertical-align:baseline">
                                                                            <span style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                If you need assistance with MFA, please 
                                                                            </span>
                                                                            <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" target="_blank" style="font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif;">
                                                                                <span style="background:white;font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                    ask a question
                                                                                </span>
                                                                            </a>,
                                                                            <span style="color:black;background:white"> 
                                                                            </span>
                                                                            <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" target="_blank" style="font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif;">
                                                                                <span style="background:white;font-size:12.0pt;color:#4285f4;text-decoration-line: none;font-family:&quot;Calibri&quot;,sans-serif">
                                                                                    open a UWin Account ticket
                                                                                </span>
                                                                            </a>
                                                                            <span style="color:black;background:white;font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif"> 
                                                                                or contact the IT Service Desk during University business hours (8:30 a.m. – 4:30 p.m. Monday – Friday) at 519-256-3000 ext 4440. 
                                                                            </span>
                                                                            <span style="font-size:9.0pt;font-family:&quot;Segoe UI&quot;,sans-serif">
                                                                                <u></u><u></u>
                                                                            </span>
                                                                        </p>
                                                                        <p class="MsoNormal" style="margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal;vertical-align:baseline">
                                                                            <span style="font-size:9.0pt;font-family:&quot;Segoe UI&quot;,sans-serif">
                                                                                <u></u> <u></u>
                                                                            </span>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">
                                                                            Thank you,
                                                                            <u></u><u></u>
                                                                        </p>
                                                                        <p class="MsoNormal" style="font-size:12.0pt;font-family:&quot;Calibri&quot;,sans-serif">IT Services<br>
                                                                            University of Windsor
                                                                            <span> </span>
                                                                            <u></u><u></u>
                                                                        </p>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </font>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
            </body>
        </html>

                    
                                                                
                                                    
        """

        part2 = MIMEText(html, "html")

        msg.attach(part2)

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

    return sender, receiver, username, form, campaign