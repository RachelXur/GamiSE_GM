import os
import smtplib
from flask import url_for
from smtplib import SMTPException
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.model import Phishingresult, Phishingcampaign
from application.forms import SimulationForm
from application import routes
from application import db

def Discount_Apple(usersapple):
    EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
    EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
    form = SimulationForm()
    campaign = Phishingcampaign.query.filter_by(campaign_name=form.campaign_name.data).first()
    for user in usersapple:
        sender = 'Apple Pay <gamise@fastmail.com>'
        receiver = user.email
        username = user.username
        #randomly create a token
        uniquelink = routes.createphish_token(user)

        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'Take 10 dollars off delivery with DooorDash.'
        msg['From'] = 'Apple Pay <gamise@fastmail.com>'
        msg['To'] = user.email

        html = """


        <!DOCTYPE html><html lang="en-GB">
            <head><meta http-equiv=Content-Type content="text/html; charset=UTF-8"></head>
            <style type="text/css">
            body,td,div,p,a,input 
            {
                font-family: arial, sans-serif;
            }
            </style>
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <style type="text/css" nonce="D5/Wy8VDdS0/Sir+YFmEBQ">
            body, td 
            {
                font-size:13px
            } 
            a:link, a:active 
            {
                color:#1155CC; 
                text-decoration:none
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
            <body>
                <div class="bodycontainer">
                    <div class="maincontent">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center">
                            <tbody>
                                <tr>
                                    <td align="center" valign="middle" bgcolor="#f2f2f2">
                                        <table border="0" cellpadding="0" cellspacing="0" width="640" align="center" style="min-width:320px;max-width:640px">
                                            <tbody id="m_591092369271924123m_4435424273711280593base"> 
                                                <tr>
                                                    <br><br>
                                                </tr> 
                                                <tr>
                                                    <td align="center" valign="middle" bgcolor="#ffffff" style="background-color:#ffffff">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="min-width:320px">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:10px 0px 10px 0px;vertical-align:middle">
                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="middle" height="70" style="vertical-align:middle">
                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none">
                                                                                            <img src="https://www.apple.com/v/apple-pay/m/images/shared/hero_logo__eo41ol524ga6_large.png" alt="Apple Pay" title="Apple Pay" width="115" height="45" border="0" style="display:block;">
                                                                                        </a>
                                                                                    </td>
                                                                                    <td align="center" valign="middle" width="20" style="vertical-align:middle">
                                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="middle" style="border-left:solid 1px #cdcdcd" height="40">
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                    <td align="center" valign="middle" style="padding-left:10px;vertical-align:middle">
                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""">
                                                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/5hj4geTkkgHYYJTK4BWodh/cf869761c737536afe6489f1965335cf/doordash_logo.png" alt="DoorDash" title="DoorDash" width="140" height="50" border="0" style="display:block;">
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="middle"  style="background-color:#ffffff;padding:40px 35px 0px 35px">
                                                        <table width="520" border="0" cellpadding="0" cellspacing="0" align="center" style="min-width:280px;max-width:520px">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding-bottom:20px">
                                                                        <h1 style="font-weight:normal;font-size:40px;line-height:1.3;color:#000000; margin:0px;font-family:&#39; pp-sans-big-light &#39;,Tahoma,Arial,sans-serif;">Take $10 off your next delivery with DoorDash.</h1>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="middle">
                                                                        <p style="font-size:18px;line-height:1.5;color:#000000; margin:0px;font-family:&#39;pp-sans-small-regular &#39;,Tahoma,Arial,sans-serif;">Ready for a break from cooking? Pay with Apple Pay <span><br></span>and get $10 off your order of $25+.</p>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" style="padding:30px 0 0 0">
                                                                        <table width="100%" align="center" cellspacing="0" cellpadding="0" border="0" style="vertical-align:top">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" style="font-family:Helvetica,Tahoma,sans-serif;font-size:14px;line-height:60px;font-weight:bold;columns: #000000;;padding:20px 0px 0px">
                                                                                        <div style="text-align:center;line-height:60px">
                                                                                            <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="display:inline-block;width:250px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:18px;font-weight:bold;color:#ffffff;line-height:50px;text-align:center;text-decoration:none;background-color:#0070ba;border-radius:50px" title="Order Now">Order Now</a>
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:30px 30px 30px 30px;text-align:center;">
                                                                        <p style="font-size:13px;line-height:1.5;color:#000000; margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;">Limited offer of 4000 rewards available. Expires 06/01/21. Exclusions apply. <span><a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:underline;color:rgb(255,255,255);font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif" title="Order Now">See offer terms below</a>.</span><span style="display:none">See offer terms below.</span></p>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="middle" bgcolor="#009cde" style="color:rgb(0,156,222)">
                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" title="Order Now">
                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/5R6Lq1jcsLMYtldMFq9gbf/b0c1e503cc4aaa2b630531d2aebf6558/PP_DOORDASH_BELT_003.gif?w=1280&amp;q=80" alt="Take $10 off your next delivery with DoorDash." width="640" height="auto" border="0" style="display:block;text-align:center;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:18px;color:#000000" title="Take $10 off your next delivery with DoorDash.">
                                                        </a>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="middle" style="padding:0px 0px 0px 0px;background-color:#ffffff" bgcolor="#ffffff">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="max-width:640px">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center" valign="middle">
                                                                        <img src="https://images.ctfassets.net/7rifqg28wcbd/7nKjA3DMTWWvlpKgtxePy7/c4ce455c57b05be8c93b407f4a65a646/spacer.gif" alt="" width="50" height="50" border="0" style="display:block">
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="middle" bgcolor="#ffffff" style="background-color:#ffffff">
                                                        <table width="560" border="0" cellpadding="0" cellspacing="0" align="center" style="max-width:560px">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:5px 20px 25px 20px">
                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="top">
                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="left">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="top">
                                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="center" width="100%">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td align="left" valign="top" width="120" style="vertical-align:top">
                                                                                                                        <img src="https://images.ctfassets.net/7rifqg28wcbd/5MLy9ebmEyuzeFirMDBdwA/98796b361e7e4b73ec99044fa0d82b93/pp_doordash_icon1.png" width="80" height="80" border="0" style="display:block;text-align:center;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:12px;color:#000000" title="Add to cart" alt="Add to cart">
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table cellpadding="0" cellspacing="0" border="0" width="400" align="right">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="left" valign="middle" style="padding:0px 0px 10px 0px">
                                                                                                        <p style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:16px;line-height:1.5;color:#6c7378">Order by 06/01/21 through <a hhref="""+ url_for('disount', token=uniquelink, _external=True) +""" title="doordash" style="font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif;text-decoration:underline;color:rgb(51,122,183)">DoorDash</a>.
                                                                                                        </p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:0px 0px 0px 0px">
                                                                        <table width="560" border="0" cellpadding="0" cellspacing="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="middle" style="padding:0px 20px 0px 20px">
                                                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="middle" style="border-top:solid 1px #dddddd;font-size:12px;line-height:25px">&nbsp; 
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:0px 20px 25px 20px">
                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="top">
                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="left">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="top">
                                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="center" width="100%">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td align="left" valign="top" width="120" style="vertical-align:top">
                                                                                                                        <img src="https://images.ctfassets.net/7rifqg28wcbd/2v6CpNafoHUnJNqbnODdnK/ef5847aede0d6143a6cfb862ab3612f4/pp_doordash_icon2.png" alt="Order with Apple Pay" width="80" height="80" border="0" style="display:block;text-align:center;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:12px;color:#000000" title="Order with Apple Pay">
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table cellpadding="0" cellspacing="0" border="0" width="400" align="right">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="left" valign="middle" style="padding:0px 0px 10px 0px">
                                                                                                        <p style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:16px;line-height:1.5;color:#6c7378">Pay for your order with Apple Pay. Your discount will be automatically applied.</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:0px 0px 0px 0px">
                                                                        <table width="560" border="0" cellpadding="0" cellspacing="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="middle" style="padding:0px 20px 0px 20px">
                                                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="middle" style="border-top:solid 1px #dddddd;font-size:12px;line-height:25px">&nbsp; 
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:0px 20px 0px 20px">
                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="top" style="padding-bottom:0px">
                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="left">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="top">
                                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="center" width="100%">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td align="left" valign="top" width="120" style="vertical-align:top">
                                                                                                                        <img src="https://images.ctfassets.net/7rifqg28wcbd/3ccLtXSQsTm7G7nAsdbQOS/36576dac0bf09fb983e3131caddf97e6/pp_doordash_icon3.png" alt="Account Transaction" width="80" height="80" border="0" style="display:block;text-align:center;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:12px;color:#000000" title="Account Transaction">
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table cellpadding="0" cellspacing="0" border="0" width="400" align="right">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="left" valign="middle" style="padding:0px 0px 10px 0px">
                                                                                                        <p style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:16px;line-height:1.5;color:#6c7378">Savings will be reflected on your Apple Pay email receipt and account transaction details. You must log in to Apple Pay to see your account transaction details.</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="middle" style="padding:0px 0px 0px 0px;background-color:#ffffff" bgcolor="#ffffff">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="max-width:640px">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center" valign="middle">
                                                                        <img src="https://images.ctfassets.net/7rifqg28wcbd/7nKjA3DMTWWvlpKgtxePy7/c4ce455c57b05be8c93b407f4a65a646/spacer.gif" alt="" width="50" height="50" border="0" style="display:block">
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="middle" style="padding:0px 0px 0px 0px;background-color:#f5f7fa" bgcolor="#f5f7fa">
                                                        <table width="620" border="0" cellpadding="0" cellspacing="0" align="center" style="max-width:620px;background-color:inherit">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center" valign="middle" style="padding:25px 20px 25px 20px">
                                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="middle" style="padding-bottom:20px;border-bottom:solid 1px #dddddd">
                                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center" width="160">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="middle">
                                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" title="Facebook">
                                                                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/1e1NIwIzTYaicUMqKV7eqf/eda4183269ab4b803f9e7fe61f57bbe7/fb.png" alt="Facebook" width="40" height="40" border="0" style="display:block;" title="Facebook">
                                                                                                        </a>
                                                                                                    </td>
                                                                                                    <td align="center" valign="middle">
                                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" title="Twitter">
                                                                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/79B7K3pQth0QZM95LrE4lI/0b63ee526bee9ad6ee9f89f0ddeb1785/twitter.png" alt="Twitter" width="40" height="40" border="0" style="display:block;">
                                                                                                        </a>
                                                                                                    </td>
                                                                                                    <td align="center" valign="middle">
                                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" title="Instagram">
                                                                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/5WZHOOAbG3gX4WtbqC3H2i/dec7ee347f25df0257bbaceed10a346a/insta.png" alt="Instagram" width="40" height="40" border="0" style="display:block;">
                                                                                                        </a>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="center" valign="middle" style="border-bottom:solid 1px #dddddd;background-color:inherit">
                                                                                        <table border="0" cellpadding="0" cellspacing="0" align="center" style="background-color:inherit">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center" valign="middle" style="background-color:inherit">
                                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="left" style="background-color:inherit">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td align="center" valign="middle" style="padding-top:20px;padding-bottom:20px;padding-left:10px;padding-right:10px;background-color:inherit">
                                                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" title="Download on the App Store">
                                                                                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/6YJOyJDkuDLtfnKuD0jIRs/a55299cdc15150064703229a6db53a09/english_apple_store_badge.png" alt="Download on the App Store" height="40" border="0" style="display:block;">
                                                                                                                        </a>
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                        <table cellpadding="0" cellspacing="0" border="0" align="right" style="background-color:inherit">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td align="center" valign="middle" style="padding-top:20px;padding-bottom:20px;padding-left:10px;padding-right:10px;background-color:inherit">
                                                                                                                        <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" title="Get it on Google Play">
                                                                                                                            <img src="https://images.ctfassets.net/7rifqg28wcbd/45zulEItNtk29JYZJgFlZ7/537970be2be551f7fe88136e70a87b56/english_Google_Play_badge.png" alt="Get it on Google Play" height="40" border="0" style="display:block;">
                                                                                                                        </a>
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="center" valign="middle" style="font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:15px;line-height:150%;color:#6c7378;padding-top:20px;padding-bottom:20px;border-bottom:solid 1px #dddddd;white-space:nowrap">
                                                                                        <a title="Account" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none;color:#6c7378" title="Account">
                                                                                            <strong style="font-weight:bold">Account</strong>
                                                                                        </a>
                                                                                        <span> </span>
                                                                                        <a title="Help" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none;color:#6c7378" title="Help">
                                                                                            <strong style="font-weight:bold">Help</strong>
                                                                                        </a>
                                                                                        <span> </span>
                                                                                        <a title="Fees" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none;color:#6c7378" title="Fees">
                                                                                            <strong style="font-weight:bold">Fees</strong>
                                                                                        </a>
                                                                                        <span> </span>
                                                                                        <a title="Security" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none;color:#6c7378" title="Security">
                                                                                            <strong style="font-weight:bold">Security</strong>
                                                                                        </a><span> </span>
                                                                                        <a title="App" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none;color:#6c7378" title="App">
                                                                                            <strong style="font-weight:bold">App</strong>
                                                                                        </a><span> </span>
                                                                                        <a title="Shop" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="text-decoration:none;color:#6c7378;white-space:nowrap" title="Shop">
                                                                                            <strong style="font-weight:bold">Shop</strong>
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="left" valign="middle" style="padding:20px 0px 0px">
                                                                                        <div style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:13px;line-height:150%;color:#6c7378">
                                                                                            <a name="m_591092369271924123_m_4435424273711280593_terms" href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif;text-decoration:underline;color:rgb(51,122,183)">
                                                                                            </a>
                                                                                            <b>“Eligible Participant”:</b> Open only to residents of Canada who: (1) are eighteen (18) years of age or older; and (2) are holders of a Canadian Apple Pay account in good standing (“Valid Account”) and (3) receive an authorized email containing the invitation to participate in the offer (eligibility for/those who receive such an email will be determined solely by Apple Pay). 
                                                                                            <br><br>
                                                                                            <b>“Eligible Purchase(s)”:</b> Purchases made at DoorDash in CAD using a Valid Account. Eligible Purchases do not include: (1) send/receive money transactions (including those marked as a “Goods and Services” payments), (2) charitable donations, (3) purchases made using Apple Pay.me; (4) Visa Debit or credit card purchases made using the card directly and not through your Apple Pay account, and (5) Apple Pay transaction fees. 
                                                                                            <br><br>
                                                                                            <b>“Offer Period”:</b> Starts at 12:01 a.m Eastern Time (“ET”) on February 5, 2021 and ends at 11:50 p.m ET on June 30, 2021. 
                                                                                            <br><br>
                                                                                            <b>“Reward”:</b> $10 CAD voucher that will be viewable in the “Offers” section of the Eligible Participant’s Apple Pay account for personal or premier accounts. For business accounts, the Reward will only be visible during checkout and on the purchase transaction receipt(s). <b>Only 4000 Rewards are available during the Offer Period; Rewards will no longer be awarded once the limit is reached.</b> 
                                                                                            <br><br>
                                                                                            <b>How to Qualify: </b>Eligible Participants must make $25 CAD of Eligible Purchases during the Offer Period. For certain offers as described in the invitation for the offer, Eligible Participants must activate the offer by following the steps in the invitation prior to qualifying. 
                                                                                            <br><br>
                                                                                            <b>How to Redeem</b>: Once received, activated (where applicable), and qualified for, the Reward will be applied automatically to the Eligible Participant’s Eligible Purchase that qualified for the Reward. The Reward must be redeemed during the Offer Period and may only be redeemed as described in these terms &amp; conditions. Use of the Reward will be reflected on the Eligible Participant’s Apple Pay receipt and/or in the transaction details of his/her Apple Pay account. There is a limit of one (1) Reward per Valid Account. 
                                                                                            <br><br>
                                                                                            <b>Miscellaneous:</b> Redemptions are final, will not be returned, and are subject to review and verification. The Reward has no cash value and cannot be redeemed for cash or withdrawn from the Eligible Participant’s Apple Pay account, except in Apple Pay’s sole discretion. If item(s) purchased using a Reward are returned and the Offer Period has expired, Apple Pay will first refund the money spent to the payment method used to complete the Eligible Purchase and purchase amount in excess of the money spent (i.e., the value of the Reward) will not be refunded. If the Offer Period has not expired, the value of the Reward will be returned to the Offers section of the Valid Account and will be available for use by the account holder. Apple Pay may provide an alternate reward of equal value if it is unable for any reason to fulfill the Reward. Apple Pay reserves the right to cancel, suspend or modify this offer in part or in its entirety at any time without notice, for any reason in its sole discretion. Similar offers may run at the same time; qualification for this offer does not constitute qualification for any other offer. Apple Pay is not responsible and/or liable for any lost, stolen, late, incomplete, illegible, interrupted, delayed, or misdirected e-mail, Reward, or offer-related materials or correspondence or if any Eligible Participant’s e-mail address, Valid Account, or other contact information does not work, is deleted, or is changed without Eligible Participant giving prior written notice to Apple Pay. Eligible Participant acknowledges that the Offer is in no way sponsored, endorsed, administered or associated with DoorDash in any way and hereby releases DoorDash from any and all claims in connection with the Offer. Offer is void where prohibited, if Eligible Purchases are not completed through legitimate channels, or if any offer-related materials are counterfeit, altered, defective, tampered with or irregular in any way. Certain offers may not be transferable. Any questions relating to the offer will be resolved in Apple Pay’s sole discretion and its decisions related to the offer will be final and binding.
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="left" valign="middle" style="padding:20px 0px 0px 0px">
                                                                                        <div style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:13px;line-height:150%;color:#6c7378">Google Play and the Google Play logo are trademarks of Google Inc. </div>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="left" valign="middle" style="padding:20px 0px 0px 0px">
                                                                                        <div style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:13px;line-height:150%;color:#6c7378">Apple and the Apple logo are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc., registered in the U.S. and other countries.
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="left" valign="middle" style="padding:20px 0px 0px 0px">
                                                                                        <div style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:13px;line-height:150%;color:#6c7378">This email was sent to  
                                                                                            <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="color:rgb(0,156,222);text-decoration:underline;font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif">"""+ receiver +"""
                                                                                            </a>  , because your email preferences are set to receive &#39;News and Promotions&#39;. Click here to 
                                                                                            <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="color:rgb(0,156,222);text-decoration:underline;font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif">Unsubscribe
                                                                                            </a>.
                                                                                            <br><br>To manage your communication preferences, please visit our 
                                                                                            <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="color:rgb(0,156,222);text-decoration:underline;font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif">preference centre
                                                                                            </a>.
                                                                                            <br><br>Please do not reply to this email. We are unable to respond to inquiries sent to this address. For immediate answers to your questions, visit our Help Centre by clicking &#39;Help&#39; located on any Apple Pay page or email.
                                                                                            <br><br>Apple Pay is committed to your privacy, learn more about our 
                                                                                            <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="color:rgb(0,156,222);text-decoration:underline;font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif">privacy policy
                                                                                            </a>.
                                                                                            <br><br>Copyright © 2020 
                                                                                            <a href="""+ url_for('disount', token=uniquelink, _external=True) +""" style="color:rgb(0,156,222);text-decoration:underline;font-family:pp-sans-small-regular,Tahoma,Arial,sans-serif">661 University Ave, Toronto, ON M5G 1M1
                                                                                            </a>. All rights reserved.
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="left" valign="middle" style="padding:20px 0px 0px 0px">
                                                                                        <div style="margin:0px;font-family:&#39;pp-sans-small-regular&#39;,Tahoma,Arial,sans-serif;font-size:13px;line-height:150%;color:#6c7378">
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <table cellpadding="0" cellspacing="0" border="0" align="center" width="640">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="height:1px;width:1px">
                                                                        <img src="https://pixel.app.returnpath.net/pixel.gif?r=2f6be46d47e11b222de691bd456fc58eb37b72dd" width="1" height="1">
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="line-height:2px;height:2px;min-width:640px">
                                                                        <img src="https://images.ctfassets.net/7rifqg28wcbd/7nKjA3DMTWWvlpKgtxePy7/c4ce455c57b05be8c93b407f4a65a646/spacer.gif" height="2" width="640" style="max-height:2px;min-height:2px;display:block;width:640px;min-width:640px">
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>    
                        </table>
                    </div>
                </div>
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