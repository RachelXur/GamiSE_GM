import os
import smtplib, ssl
from flask import url_for
from email.message import EmailMessage
from application.forms import SimulationNoteForm
from application.model import User

def simulation_note_IT():
    EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
    EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
    users = User.query.filter_by(position="IT").all()

    for user in users:
        form = SimulationNoteForm()
        subject = form.subject.data
        sender = form.sender.data
        path = '/static/images/GamiSE.png'

        msg = EmailMessage()
        msg['Subject'] = 'Simulation Notification - GamiSE'
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
                                                                                                                                This week's phishing simulation:
                                                                                                                            </td>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px; white-space: pre-wrap;">
                                                                                                                                <br>
                                                                                                                                Here  the subject of this week's phishing simulation:<br>
                                                                                                                                <div style="font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px; white-space:"><p>"""+ subject +"""</p></div>
                                                                                                                            </td>
                                                                                                                            <td style="text-decoration:none;width:89%;min-width:86%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px; white-space: pre-wrap;">
                                                                                                                                <br>
                                                                                                                                Here  the email sender of this week's phishing simulation:<br>
                                                                                                                                <div style="font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;padding: 0px; white-space: pre-wrap;"><p>"""+ sender +"""</p></div>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td valign="middle" style="padding: 0px;border-radius: 100px;line-height: 18px;">
                                                                                                                            <br>
                                                                                                                                <a href="""+ url_for('rattack', _external=True) +""" style="text-align:center;width:30%;min-width:20%;display:block;font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;padding:5px 18px;border:1px solid#3071A9;background-color: #3071A9; display:inline-block;font-weight:bold;white-space:nowrap">
                                                                                                                                    Check report and Solve 
                                                                                                                                </a>
                                                                                                                                <br><br><hr>
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
            smtp.send_message(msg)
            smtp.quit()
    return form, path, subject, sender