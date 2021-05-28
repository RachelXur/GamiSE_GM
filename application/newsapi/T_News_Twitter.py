import os
import smtplib, ssl
from flask import url_for
from smtplib import SMTPException, SMTP_SSL
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from application.newsapi.news import NewsofCA
from application.model import User, Phishingresult, Phishingcampaign
from application.forms import SimulationForm
from application import routes
from application import db
import random
import webbrowser
import requests

def Twitternews():
    title,description,links,date,image,name = NewsofCA()

    EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
    EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
    users = User.query.filter_by(position='Normal').filter_by(qb='Twitter').all()
    form = SimulationForm()
    campaign = Phishingcampaign.query.filter_by(campaign_name=form.campaign_name.data).first()

    if users:
        for user in users:
            # news api 
            inmain_url = " http://newsapi.org/v2/everything?language=en&q="+ user.interest +"&SortBy=publishedAt&apiKey=1564aed20da04500abfa72dad9b1354f "
        
            # fetching data in json format 
            interests_news_page = requests.get(inmain_url).json() 
        
            # getting all articles in a string article 
            inarticle = interests_news_page["articles"] 
        
            # empty list which will  
            # contain all trending news 
            inresults = [] 
            inlists = []
            inurls = []
            indate = []
            inimage = []
            inname = []
        
            for ar in inarticle: 
                inresults.append(ar["title"])
                inlists.append(ar["description"])
                inurls.append(ar["url"])
                indate.append(ar["publishedAt"])
                inimage.append(ar["urlToImage"])
                inname.append(ar["source"])

            intitle = inresults[0]
            indescription = inlists[0]
            inlinks = inurls[0]
            indate = indate[0]
            inimage = inimage[0]
            inname = inname[0]["name"]

            # send email
            sender = 'Daily News <personal@fastmail.com>'
            receiver = user.email
            username = user.username
            #randomly create a token
            uniquelink = routes.createphish_token(user)

            msg = MIMEMultipart("alternative")
            msg['Subject'] = 'Hi, ' + username + '. Check Daily News'
            msg['From'] = 'Daily News <personal@fastmail.com>'
            msg['To'] = user.email


            html = """
            <!DOCTYPE html>
                <style>
                    a{
                        text-decoration:none;
                    }
                </style>
                <head>
                </head>
                <table lang="en" role="presentation" aria-hidden="true" border="0" style="width: 100%;background-color: #ffffff;padding: 0px" align="center">
                    <tbody>
                        <tr>
                            <td align="center" style="padding: 0px">
                                <table border="0" align="center" style="padding: 0px">
                                    <tbody>
                                        <tr>
                                            <td width="12" style="padding: 0px">&nbsp; </td>
                                            <td style="padding: 0px">
                                                <table border="0" style="padding: 0px;width: 650px">
                                                    <tbody>
                                                        <tr>
                                                            <td height="12" style="padding: 0px"></td>
                                                        </tr>
                                                        <tr>
                                                            <td  class = "text" style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-weight: 600;color: #292f33;font-size: 30px;line-height: 36px;padding: 0px;">Hi, """+ username +"""</td>
                                                        </tr>
                                                        <tr>
                                                            <td  class = "text" style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-weight: 600;color: #292f33;font-size: 28px;line-height: 36px;padding: 0px;">What's New </td>
                                                        </tr>
                                                        <tr>
                                                            <td height="18" style="padding: 0px"></td>                                                
                                                        </tr>
                                                        <tr>
                                                            <td align="center" style="padding: 0px">
                                                                <table cellpading="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding: 0px;border: 1px solid #aab8c2;background-color: #ffffff;border-radius: 4px">
                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" title="Twitterr">
                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td height="24" style="padding: 9px;height: 24px"></td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td style="padding: 0px">
                                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td width="24" style="padding: 0px;width: 24px;min-width: 12px"></td>
                                                                                                                <td style="padding: 0px">
                                                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                                        <tbody>
                                                                                                                            <tr><img src= "https://ea.twimg.com/email/self_serve/media/logo_twitter-1497383721365.png"
                                                                                                                                height="36" alt="Twitter" title="Twitter" style="margin-left: auto;margin-right: auto;padding: 0px;display:block;border: none;outline: none;">
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <br><br>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;">
                                                                                                                                    <img src = """+ image +""" width="598.89" height="399.25">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="14" style="height: 14px;padding: 0px"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-size: 14px;line-height: 18px;color: #657786;">
                                                                                                                                    """+ name +""" </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="8" style="height: 8px;padding: 0px;"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-size: 20px;line-height: 24px;font-weight: bold;color: #292f33;">
                                                                                                                                """+ title +""" </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="8" style="height: 8px;padding: 0px;"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-size: 14px;line-height: 18px;color: #292f33;">
                                                                                                                                """+ description +""" </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="14" style="height: 14px;padding: 0px;"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;">
                                                                                                                                    <table border="0" cellspacing="0" cellpadding="0" align="left" width="100%" style="padding: 0px;">
                                                                                                                                        <tbody>
                                                                                                                                            <tr>
                                                                                                                                                <td align="center" valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" title="Twitterr"
                                                                                                                                                        style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#ffad1f;text-decoration:none;border-radius:100px;padding:5px 18px;border:1px solid #ffad1f;display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                                        Read more at Twitterr 
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
                                                                                                                <td width="24" style="padding: 0px;width: 24px;min-width: 12px;"></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td height="20" style="padding: 0px; height: 20px"></td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </a>                                   
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td height="18" style="padding: 0px"></td>                                                
                                                        </tr>
                                                        <tr>
                                                            <td align="center" style="padding: 0px">
                                                                <table cellpading="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding: 0px;border: 1px solid #aab8c2;background-color: #ffffff;border-radius: 4px">
                                                                                <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" title="Twitterr">
                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td height="24" style="padding: 9px;height: 24px"></td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td style="padding: 0px">
                                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td width="24" style="padding: 0px;width: 24px;min-width: 12px"></td>
                                                                                                                <td style="padding: 0px">
                                                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;">
                                                                                                                                    <img src = """+ inimage +""" width="598.89" height="399.25">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="14" style="height: 14px;padding: 0px"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-size: 14px;line-height: 18px;color: #657786;">
                                                                                                                                    """+ inname +""" </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="8" style="height: 8px;padding: 0px;"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-size: 20px;line-height: 24px;font-weight: bold;color: #292f33;">
                                                                                                                                """+ intitle +""" </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="8" style="height: 8px;padding: 0px;"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-size: 14px;line-height: 18px;color: #292f33;">
                                                                                                                                """ + indescription + """ </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td height="14" style="height: 14px;padding: 0px;"></td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="padding: 0px;">
                                                                                                                                    <table border="0" cellspacing="0" cellpadding="0" align="left" width="100%" style="padding: 0px;">
                                                                                                                                        <tbody>
                                                                                                                                            <tr>
                                                                                                                                                <td align="center" valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" title="Twitterr"
                                                                                                                                                        style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#ffad1f;text-decoration:none;border-radius:100px;padding:5px 18px;border:1px solid #ffad1f;display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                                        Read more at Twitterr 
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
                                                                                                                <td width="24" style="padding: 0px;width: 24px;min-width: 12px;"></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td height="20" style="padding: 0px; height: 20px"></td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </a>                                   
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding:0px;margin:0px auto;font-family:'Helvetica Neue Light',Helvetica,Arial,sans-serif;font-size:12px;padding:0px;margin:0px;font-weight:normal;line-height:16px;text-align:center;margin:auto;color:#8899a6" align="center">
                                                                We sent this to """+ username +""".
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding:0px;margin:0px auto;font-family:'Helvetica Neue Light',Helvetica,Arial,sans-serif;font-size:12px;padding:0px;margin:0px;font-weight:normal;line-height:16px;text-align:center;margin:auto;color:#8899a6" align="center">
                                                                Twitterr, Inc. 1355 Market Street, Suite 900 San Francisco, CA 94103.
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
            </html>
            """

            content = MIMEText(html, "html")
            msg.attach(content)

            try:
                smtpObj = SMTP_SSL('smtp.fastmail.com', 465)
                smtpObj.login(EMAIL_USERFASTMAIL, EMAIL_PASSWORDFASTMAIL)
                smtpObj.sendmail(sender, receiver, msg.as_string().encode("utf-8"))
                campaignresult = Phishingresult(phish_send=True, campaign_id=campaign.campaign_id, phish_link = uniquelink, user_id=user.id)
                db.session.add(campaignresult)
                db.session.commit()
                print ("send successfully")
            except SMTPException:
                print ("Error: Enable to send mail")

    return title, description, date, image, name, intitle, indescription, indate, inimage, inname, username, sender, receiver,form, campaign, uniquelink