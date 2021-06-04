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

def tablet_TD(userstd):
    EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
    EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
    form = SimulationForm()
    campaign = Phishingcampaign.query.filter_by(campaign_name=form.campaign_name.data).first()
    for user in userstd:
        sender = 'TD <email@e.email-td.com>'
        receiver = user.email
        username = user.username
        #randomly create a token
        uniquelink = routes.createphish_token(user)

        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'TD - Chance to get a Tabllet!'
        msg['From'] = 'TD <email@e.email-td.com>'
        msg['To'] = user.email

        html = """


        <!DOCTYPE html>
        <html lang="en-GB">
            <head>
                <meta http-equiv=Content-Type content="text/html; charset=UTF-8">
                <style type="text/css">
                body,td,div,p,a,input 
                {
                    font-family: arial, sans-serif;
                }
                </style>
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <style type="text/css">
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
                .ribbon 
                {
                display: inline-block;
                height: 0;
                padding: 0 7.5px;
                line-height: 0.15rem;
                font-size: 24px;
                background-color: #ffc400;
                border-top: 18px solid #ffc400;border-bottom: 18px solid #ffc400;
                border-right: 11px solid #fff;
                }
                </style>
            </head>
            <body>
                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0" style="margin:0px auto;background-color:rgb(230,230,230)" bgcolor="#e6e6e6">
                    <tbody>
                        <tr>
                            <td valign="top" align="center" style="background-color:rgb(230,230,230)" bgcolor="#e6e6e6">
                                <table cellpadding="0" cellspacing="0" width="600" align="center" border="0" style="margin:0px auto;width:100%;max-width:600px">
                                    <tbody>
                                        <tr>
                                            <br><br>
                                        </tr>
                                        <tr>
                                            <td valign="top" style="font-size:0px;background-color:rgb(230,230,230)" bgcolor="#e6e6e6">
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0" style="width:100%;max-width:600px">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" style="padding:10px 20px;text-align:left;background-color:#1a5336" bgcolor="#006ac3">
                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="border:0px">
                                                                    <img src="https://image.e.email-td.com/lib/fe9a12747762077d75/m/1/1d074aee-2f1e-446d-bac5-ccc9a88e41d7.png" width="150" alt="TD" style="border-width:0px;width:67px;max-width:150px;height:60px">
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" bgcolor="#ffffff" style="font-size:0px;text-align:center;background-color:rgb(255,255,255)">
                                                                <table cellpadding="0" cellspacing="0" width="260" border="0">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td valign="top" style="padding:30px 0px 0px;background-color:rgb(255,255,255);">
                                                                                <div class="ribbon text-script">Limited Time Offer</div>
                                                                            </td>
                                                                        </tr>
                                                                </table>
                                                                <table cellpadding="0" cellspacing="0" width="260" align="center" border="0">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td valign="top" style="padding:20px 0px 30px;background-color:rgb(255,255,255)">
                                                                                <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/11/04a1d4c5-3084-4f15-b0c3-7a63868e8bc4.jpg" width="260" alt="iPad" style="border:0px;width:100%;max-width:260px;height:auto">
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" style="padding:0px 20px 20px;text-align:center;background-color:rgb(255,255,255);color:rgb(0,0,0)" bgcolor="#ffffff;">
                                                                <h1 style="text-align:center;margin:0px;font-size:24px;font-family:Roboto,Arial,sans-serif;color:rgb(0,0,0)">
                                                                    <strong style="font-family:Roboto,Arial,sans-serif">Get the Latest 10.2” iPad in Your <br>Choice of Colour at No Cost.</strong>
                                                                </h1>
                                                                <p>When you open an eligible TD bank account.
                                                                </p>
                                                                <p>
                                                                    Offer ends June 1, 2021. Conditions apply.
                                                                </p>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" style="background-color:rgb(255,255,255)" bgcolor="#ffffff">
                                                                <table cellpadding="0" cellspacing="0" width="15%" align="center" border="0">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td valign="top" style="padding-top:0px;padding-bottom:30px;border-top-width:1px;border-top-style:solid;font-size:10px;border-top-color:#008a00">
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" style="padding:0px 20px 0px;text-align:left;background-color:rgb(255,255,255);color:rgb(0,0,0)">
                                                                <p style="margin:0px 0px 20px;font-family:Roboto,Arial,sans-serif;font-size:18px;line-height:24px">
                                                                    Hello """+ username +""",
                                                                </p>
                                                                <p style="margin:0px 0px 20px;font-size:18px;line-height:24px;font-family:Roboto,Arial,sans-serif">
                                                                    <strong>How To Get Started</strong>
                                                                </p>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" style="padding:0px 20px;text-align:left;background-color:rgb(255,255,255);color:rgb(0,0,0)" bgcolor="#ffffff;">
                                                                <table cellpadding="0" cellspacing="0" width="90%" align="center" border="0">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td valign="top" style="font-size:24px;line-height:24px;padding-right:15px;color:#008a00">
                                                                                <strong>1</strong>
                                                                            </td>
                                                                            <td valign="top" style="font-family:Roboto,Arial,sans-serif;font-size:16px;line-height:24px">
                                                                                Open an eligible TD bank account by 
                                                                                <Strong>
                                                                                    June 1, 2021
                                                                                </Strong><br>
                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Roboto,Arial,sans-serif;color:rgb(0,106,195); text-decoration:none">
                                                                                    <strong style="font-family:Roboto,Arial,sans-serif;color:#008a00;">> Get Started</strong>
                                                                                </a> 
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td valign="top" colspan="2" style="padding-bottom:10px">
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td valign="top" style="font-size:24px;line-height:24px;padding-right:15px;color:#008a00">
                                                                                <strong>2</strong>
                                                                            </td>
                                                                            <td valign="top" style="font-family:Roboto,Arial,sans-serif;font-size:16px;line-height:24px;">
                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Roboto,Arial,sans-serif;color:rgb(0,106,195);text-decoration:none" >
                                                                                    <strong style="font-family:Roboto,Arial,sans-serif;color:rgb(0, 0, 0)">Set up and complete two of the following by June 1, 2021:</strong>
                                                                                </a>
                                                                                <li style="color: #008a00;">
                                                                                    <span style="color:rgb(0, 0, 0)">
                                                                                        Your payroll as a direct deposit
                                                                                    </span>
                                                                                </li>
                                                                                <li style="color: #008a00;">
                                                                                    <span style="color:rgb(0, 0, 0)">
                                                                                        Two pre-authorized monthly payments (PAPs)
                                                                                    </span>
                                                                                </li>
                                                                                <li style="color: #008a00;">
                                                                                    <span style="color:rgb(0, 0, 0)">
                                                                                        Two bill payments to a service provider
                                                                                    </span>
                                                                                </li>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td valign="top" style="font-size:24px;line-height:24px;padding-right:15px;color:#008a00">
                                                                                <strong>3</strong>
                                                                            </td>
                                                                            <td valign="top" style="font-family:Roboto,Arial,sans-serif;font-size:16px;line-height:24px">
                                                                                We’ll send you an email shortly after you qualify with instructions on how to order your 
                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Roboto,Arial,sans-serif;color:#008a00;text-decoration:none">10.2”  iPad Wi-Fi 32GB (8th Generation)</a>. 
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table cellpadding="0" cellspacing="0" width="100%" align="center" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td valign="top" style="padding:20px 20px 60px;text-align:left;background-color:rgb(255,255,255);color:rgb(0,0,0)" bgcolor="#ffffff;">
                                                            <br><br>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table align="center" cellpadding="0" cellspacing="0" border="0" style="border-spacing:0px;margin:0px auto;width:100%;max-width:600px" bgcolor="#e6e6e6">
                                                    <tbody>
                                                        <tr>
                                                            <td style="padding:0px">
                                                                <table cellpadding="0" cellspacing="0" width="600" align="center" border="0" style="width:100%;max-width:600px">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td valign="middle" style="font-size:0px;padding-bottom:0px;padding-top:0px;border-top-width:1px;border-top-style:solid;text-align:center;background-color:rgb(230,230,230);border-top-color:rgb(153,153,153)" bgcolor="#e6e6e6">
                                                                                <table cellpadding="0" cellspacing="0" border="0" style="display:inline-block;vertical-align:middle">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="padding:0px 0px">
                                                                                                <table align="center" cellspacing="0" width="240" cellpadding="0" border="0">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td bgcolor="#1a5336" valign="top" align="center" style="border-collapse:collapse">
                                                                                                                <table valign="middle" width="600" style="border-collapse:collapse;border-collapse:collapse;color:#ffffff;font-size:16px;font-family:Arial,Helvetica,sans-serif;text-align:left;padding-right:55px">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center" valign="middle" style="border-collapse:collapse;padding-left:30px" >
                                                                                                                                <img alt="" width="124" border="0" style="display:block;max-width:124px;margin-left:20px;min-width:75px" src="https://image.e.email-td.com/lib/fe9a12747762077d75/m/1/bc1dfdea-b315-492b-ac21-e9c1726b80ef.png">
                                                                                                                            </td>
                                                                                                                            <td valign="middle" style="border-collapse:collapse;border-collapse:collapse;color:#ffffff;font-size:16px;font-family:Arial,Helvetica,sans-serif;text-align:left;padding-right:55px;padding-left: 20px;">
                                                                                                                                <span style="white-space:nowrap">
                                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="color:inherit;color:#ffffff;text-decoration:underline">
                                                                                                                                        Contact Us
                                                                                                                                    </a> 
                                                                                                                                    <span> </span>
                                                                                                                                    |<span> </span>
                                                                                                                                </span>
                                                                                                                                <span style="white-space:nowrap">
                                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="color:inherit;color:#ffffff;text-decoration:underline">
                                                                                                                                        Privacy and Security
                                                                                                                                    </a> 
                                                                                                                                    <span> </span>
                                                                                                                                    |
                                                                                                                                    <span> </span>
                                                                                                                                </span>
                                                                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="color:inherit;color:#ffffff;text-decoration:underline">
                                                                                                                                    Legal
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
                                                                                    </tbody>
                                                                                </table>
                                                                                <table border="0" cellspacing="0" cellpadding="0" align="center" width="100%" bgcolor="#e6e6e6">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td valign="top" align = "left" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:14px;color:#555555;padding-top:11px; border-bottom:1px solid #a7a7a7">
                                                                                                <br>
                                                                                                    Safeguarding our customers’ information is a fundamental principle of TD Bank Group. For security reasons, certain information including account number has been masked. 
                                                                                                    TD will not ask you to provide personal information or login information, such as username, passwords, PINs, IdentificationPlus
                                                                                                <sup style="line-height:0.01;font-size:0.8em">®</sup> security questions and answers or account numbers, through unsolicited email. 
                                                                                                    TD will not share sensitive data through regular email nor will TD request this type of information be sent from you through regular email. 
                                                                                                    If you suspect an email to be fraudulent, please forward a copy to us at
                                                                                                <a href="mailto:"""+ username +"""" style="color:inherit;text-decoration:underline;color:#1a5336;white-space:nowrap" >
                                                                                                    phishing@td.com
                                                                                                </a>
                                                                                                <span> and </span>
                                                                                                    then delete the email.
                                                                                                <br>
                                                                                                <br>
                                                                                                <sup style="line-height:0.01;font-size:0.8em">®</sup> 
                                                                                                    The TD logo and other trademarks are the property of The Toronto‑Dominion Bank or its subsidiaries.
                                                                                                <br>
                                                                                                <br>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td valign="top" align = "left" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:14px;color:#555555;padding-top:11px; border-bottom:1px solid #a7a7a7">
                                                                                                    You have received this email at 
                                                                                                <a href="mailto:"""+ receiver +"""" style="color:inherit;text-decoration:underline;color:#1a5336">"""+ receiver +"""
                                                                                                </a> because you are a customer of TD Canada Trust. To ensure delivery to your inbox (and not to your junk or bulk mail folders), add
                                                                                                <a href="mailto:"""+ username +"""" style="color:inherit;text-decoration:underline;color:#1a5336;white-space:nowrap">email@e.email-td.com
                                                                                                </a> 
                                                                                                    to your address book. 
                                                                                                <br>
                                                                                                <br>
                                                                                                <strong>If you wish to unsubscribe from receiving commercial electronic messages from TD Canada Trust, please
                                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="color:inherit;text-decoration:underline;color:#1a5336">click here
                                                                                                </a> 
                                                                                                    or go to the following web address: 
                                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="color:inherit;text-decoration:underline;color:#1a5336;white-space:nowrap">
                                                                                                    td.com/<wbr>tdcanadatrustunsubscribe
                                                                                                </a>. 
                                                                                                </strong>
                                                                                                <br>
                                                                                                <br>
                                                                                                    Please do not reply to this email – this mailbox is not monitored. <br>
                                                                                                <br>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td valign="top" align = "left" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:14px;color:#555555;padding-top:11px;">
                                                                                                TD Canada Trust <br>
                                                                                                <a style="color:inherit;color:#555555;text-decoration:none">80 King Street West,
                                                                                                    <span id="m_-8818074052111377902x_floor_number">14</span>
                                                                                                    <sup style="line-height:0.01!important;font-size:0.8em!important">th</sup> Floor<br>
                                                                                                    Toronto, Ontario<br>
                                                                                                    M5K 1A2
                                                                                                </a><br>
                                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="color:inherit;text-decoration:underline;color:#1a5336">
                                                                                                    td.com
                                                                                                </a><br><br><br>
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
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
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