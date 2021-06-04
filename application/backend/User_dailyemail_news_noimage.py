import os
import smtplib, ssl
from flask import url_for
from email.message import EmailMessage
from application.forms import DailyNewsForm
from application.model import User
import time
from application import routes


def dailyemailnews_noimage():
    EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
    EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
    users = User.query.filter_by(position="Normal").all()

    for user in users:
        form = DailyNewsForm()
        title = form.title.data
        description = form.description.data
        link = form.link.data
        uniquelink = routes.createphish_token(user)

        msg = EmailMessage()
        msg['Subject'] = 'Daily Email - GamiSE'
        msg['From'] = 'GamiSE <gamise@fastmail.com>'
        msg['To'] = user.email

        msg.add_alternative("""\
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
                                                        <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:28px;font-family:Helvetica,Arial,sans-serif;color:#000000;">
                                                            <strong>GamiSE</strong>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td  class = "text" style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-weight: 600;color: #292f33;font-size: 32px;line-height: 36px;padding: 0px;">Daily Email </td>
                                                    </tr>
                                                    <tr>
                                                        <br>                                               
                                                    </tr>
                                                    <tr>
                                                        <td  class = "text" style="padding: 0px;font-family: Arial, Helvetica, sans-serif;font-weight: 600;color: #292f33;font-size: 24px;line-height: 36px;padding: 0px;">Hello, """+ user.username +"""</td>
                                                    </tr>
                                                    <tr>
                                                        <br>                                               
                                                    </tr>
                                                    <tr>
                                                        <td align="center" style="padding: 0px">
                                                            <table cellpading="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0px;border: 1px solid #aab8c2;background-color: #ffffff;border-radius: 4px">
                                                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="padding: 0px">
                                                                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="12" style="padding: 0px;width: 24px;min-width: 12px"></td>
                                                                                                            <td style="padding: 0px">
                                                                                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                                    <tbody>                                                       
                                                                                                                        <tr>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:28px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                Experience sharing:
                                                                                                                            </td>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                Do you have any experience or defending tips that related to social engineering and want to share on the GamiSE? Feel free to share 
                                                                                                                                your experience to help others defending the attacks.
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                            <br>
                                                                                                                                <a href="""+ url_for('pexperience', token=uniquelink, _external=True) +""" style="text-align:center;width:30%;min-width:20%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;padding:5px 18px;border:1px solid#3071A9;background-color: #3071A9; display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                    Share on GamiSE 
                                                                                                                                </a>
                                                                                                                                <br><br><hr>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td height="14" style="height: 14px;padding: 0px"></td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:28px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                Submit a Report:
                                                                                                                            </td>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                Do you have face any attacks recently, or do you find any phishing email elements in the emails that you received these days? After you forward the phishing email to the IT department,
                                                                                                                                would you like to submit a report to help the IT department to analyze the social enginering attacks?
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                            <br>
                                                                                                                                <a href="""+ url_for('userreport', token=uniquelink, _external=True) +""" style="text-align:center;width:30%;min-width:20%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;padding:5px 18px;border:1px solid#3071A9;background-color: #3071A9; display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                    Report on GamiSE 
                                                                                                                                </a>
                                                                                                                                <br><br><hr>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="padding: 0px">
                                                                                                                                <br>
                                                                                                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding: 0px">
                                                                                                                                    <tbody>
                                                                                                                                        <tr>
                                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:28px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                                News:
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td height="14" style="height: 14px;padding: 0px"></td>
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
                                                                                                                                                            <td valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                                                                <br>
                                                                                                                                                                <a href="""+ link +""" style="text-align:center;width:20%;min-width:10%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;padding:5px 18px;border:1px solid#3071A9;background-color: #3071A9; display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                                                    Read More
                                                                                                                                                                </a>
                                                                                                                                                                <br><br><hr>
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
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:28px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                Want to Withdrawal:
                                                                                                                            </td>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px;">
                                                                                                                                <br>
                                                                                                                                If you don't want to use GamiSE anymore, please click the link to submit a withdrawal questionnaire to the GamiSE, then withdrawal the training. 
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                                <br>
                                                                                                                                <a href="""+ url_for('withdrawal', token=uniquelink, _external=True) +""" style="text-align:center;width:35%;min-width:20%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;padding:5px 18px;border:1px solid#3071A9;background-color: #3071A9; display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                    Request a Withdrawal 
                                                                                                                                </a>
                                                                                                                                <br><br>
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
        """,subtype = 'html')

        with smtplib.SMTP_SSL('smtp.fastmail.com', 465) as smtp:
            smtp.login(EMAIL_USERFASTMAIL, EMAIL_PASSWORDFASTMAIL)
            time.sleep(2)
            smtp.send_message(msg)
            print(user.email)
    return user, title, description, link