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

def tablet_RBC():
    users = User.query.filter_by(position='Normal').filter_by(qc='RBC').all()
    form = SimulationForm()
    campaign = Phishingcampaign.query.filter_by(campaign_name=form.campaign_name.data).first()

    if users:
        for user in users:
            sender = 'RBC <rbcroyalbank@offers.rbc.com>'
            receiver = [user.email]
            username = user.username
            #randomly create a token
            uniquelink = routes.createphish_token(user)

            EMAIL_USERFASTMAIL = os.environ.get('EMAIL_USERFASTMAIL')
            EMAIL_PASSWORDFASTMAIL = os.environ.get('EMAIL_PASSWORDFASTMAIL')
            msg = MIMEMultipart("alternative")
            msg['Subject'] = 'RBC - Chance to get a Tabllet!'
            msg['From'] = 'RBC <rbcroyalbank@offers.rbc.com>'
            msg['To'] = user.email

            html = """
            <!DOCTYPE html >
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
                                                                <td valign="top" style="padding:10px 20px;text-align:left;background-color:rgb(0,106,195)" bgcolor="#006ac3">
                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="border:0px">
                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/11/507ca2e3-a774-4584-b28a-e18ab9cd7dcc.jpg" width="150" alt="Royal Bank" style="border-width:0px;width:150px;max-width:150px;height:auto">
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
                                                                    <p>When you open an eligible RBC bank account.
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
                                                                                <td valign="top" style="padding-top:0px;padding-bottom:30px;border-top-width:1px;border-top-style:solid;font-size:10px;border-top-color:rgb(0,106,195)">
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
                                                                                <td valign="top" style="font-size:24px;line-height:24px;padding-right:15px;color:rgb(0,106,195)">
                                                                                    <img src="https://www.rbcroyalbank.com/dms/pba/open-an-account/_assets-custom/images/1-transparent.png" alt="1" style="width: 30px !important;">
                                                                                </td>
                                                                                <td valign="top" style="font-family:Roboto,Arial,sans-serif;font-size:16px;line-height:24px">
                                                                                    Open an eligible RBC bank account by 
                                                                                    <Strong>
                                                                                        December 18, 2020
                                                                                    </Strong><br>
                                                                                    <a hhref="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Roboto,Arial,sans-serif;color:rgb(0,106,195)">
                                                                                        <strong style="font-family:Roboto,Arial,sans-serif;color:rgb(0,106,195);">> Get Started</strong>
                                                                                    </a> 
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td valign="top" colspan="2" style="padding-bottom:10px">
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td valign="top" style="font-size:24px;line-height:24px;padding-right:15px;color:rgb(0,106,195)">
                                                                                    <img src="https://www.rbcroyalbank.com/dms/pba/open-an-account/_assets-custom/images/2-transparent.png" alt="2" style="width: 30px !important;">
                                                                                </td>
                                                                                <td valign="top" style="font-family:Roboto,Arial,sans-serif;font-size:16px;line-height:24px">
                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Roboto,Arial,sans-serif;color:rgb(0,106,195)">
                                                                                        <strong style="font-family:Roboto,Arial,sans-serif;color:rgb(0, 0, 0)">Set up and complete two of the following by June 1, 2021:</strong>
                                                                                    </a>
                                                                                    <li style="color: rgb(0,106,195);">
                                                                                        <span style="color:rgb(0, 0, 0)">
                                                                                            Your payroll as a direct deposit
                                                                                        </span>
                                                                                    </li>
                                                                                    <li style="color: rgb(0,106,195);">
                                                                                        <span style="color:rgb(0, 0, 0)">
                                                                                            Two pre-authorized monthly payments (PAPs)
                                                                                        </span>
                                                                                    </li>
                                                                                    <li style="color: rgb(0,106,195);">
                                                                                        <span style="color:rgb(0, 0, 0)">
                                                                                            Two bill payments to a service provider
                                                                                        </span>
                                                                                    </li>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td valign="top" style="font-size:24px;line-height:24px;padding-right:15px;color:rgb(0,106,195)">
                                                                                    <img src="https://www.rbcroyalbank.com/dms/pba/open-an-account/_assets-custom/images/3-transparent.png" alt="3" style="width: 30px !important;">
                                                                                </td>
                                                                                <td valign="top" style="font-family:Roboto,Arial,sans-serif;font-size:16px;line-height:24px">
                                                                                    We’ll send you an email shortly after you qualify with instructions on how to order your 
                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Roboto,Arial,sans-serif;color:rgb(0,106,195)">10.2”  iPad Wi-Fi 32GB (8th Generation)</a>. 
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
                                                                                                <td style="padding:10px 20px">
                                                                                                    <table align="center" cellspacing="0" width="240" cellpadding="0" border="0">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center" valign="middle">
                                                                                                                    <span style="font-size:14px;font-family:Arial,sans-serif,Roboto;font-style:italic;color:rgb(0,0,0)">
                                                                                                                        Join us / 
                                                                                                                    </span>
                                                                                                                </td>
                                                                                                                <td align="center" valign="middle" style="padding-left:10px">
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""">
                                                                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/9/7e0e5a9b-eedf-495b-8782-164ce8343873.jpg" width="32" alt="RBC on Facebook" style="border-width:0px;margin:0px auto;display:inline-block;vertical-align:middle">
                                                                                                                    </a>
                                                                                                                </td>
                                                                                                                <td align="center" valign="middle" style="padding-left:10px">
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""">
                                                                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/9/4dba4ecc-ca13-4f88-8279-315f6fd0fde5.jpg" width="32" alt="RBC on Twitter" style="border-width:0px;margin:0px auto;display:inline-block;vertical-align:middle">
                                                                                                                    </a>
                                                                                                                </td>
                                                                                                                <td align="center" valign="middle" style="padding-left:10px">
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""">
                                                                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/9/846c8f41-494f-4a5f-bfaf-6cc990f06e00.jpg" width="32" alt="RBC on YouTube" style="border-width:0px;margin:0px auto;display:inline-block;vertical-align:middle">
                                                                                                                    </a>
                                                                                                                </td>
                                                                                                                <td align="center" valign="middle" style="padding-left:10px">
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""">
                                                                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/9/f2d5f73f-857d-4599-ae5c-e08a2eb7bb69.jpg" width="32" alt="RBC on LinkedIn" style="border-width:0px;margin:0px auto;display:inline-block;vertical-align:middle">
                                                                                                                    </a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                    <table cellpadding="0" cellspacing="0" border="0" style="display:inline-block;vertical-align:middle">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td style="padding:10px 0px;text-align:center">
                                                                                                    <table align="center" width="300" cellpadding="0" border="0" style="width:300px">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center" valign="middle" style="text-align:right">
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="text-decoration:none;border:0px">
                                                                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/11/69965cc7-321d-4637-9e26-6340df3c6acf.png" width="120" alt="Download on the App Store" title="Download on the App Store" style="border-width:0px;margin:0px auto;display:inline-block;vertical-align:middle">
                                                                                                                    </a>
                                                                                                                </td>
                                                                                                                <td width="20"></td>
                                                                                                                <td align="center" valign="middle" style="text-align:left">
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="text-decoration:none;border:0px">
                                                                                                                        <img src="https://image.website.rbc.com/lib/fe921570736c0c7b75/m/11/ecab41a9-a95e-42d7-8c73-82b974be6a33.png" width="130" alt="Get it on Google Play" title="Get it on Google Play" style="border-width:0px;margin:0px auto;display:inline-block;vertical-align:middle">
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
                                                                                <td style="border-top-width:1px;border-top-style:solid;padding:15px 20px;border-bottom-width:1px;border-bottom-style:solid;text-align:left;font-size:12px;font-family:Arial,sans-serif,Roboto;line-height:18px;border-top-color:rgb(153,153,153);border-bottom-color:rgb(153,153,153);color:rgb(0,106,195)">
                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="text-decoration:underline;font-family:Arial,sans-serif,Roboto;color:rgb(0,106,195)">
                                                                                        Privacy &amp; Security
                                                                                    </a> 
                                                                                    | 
                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="text-decoration:underline;font-family:Arial,sans-serif,Roboto;color:rgb(0,106,195)">
                                                                                        Legal
                                                                                    </a> 
                                                                                    | 
                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="text-decoration:underline;font-family:Arial,sans-serif,Roboto;color:rgb(0,106,195)">
                                                                                        Unsubscribe
                                                                                    </a>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                    <table border="0" cellspacing="0" cellpadding="0" align="center" width="100%" bgcolor="#e6e6e6">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="36" valign="top" bgcolor="#e6e6e6" style="text-align:left;padding-left:20px;padding-right:6px;padding-top:15px;line-height:16px;font-family:Arial,sans-serif;font-size:11px;color:rgb(0,0,0)"> 
                                                                                </td>
                                                                                <td valign="top" style="text-align:left;padding-right:20px;padding-top:15px;padding-bottom:6px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;color:rgb(0,0,0)">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;font-family:Arial,sans-serif">
                                                                                        <tbody style="font-family:Arial,sans-serif">
                                                                                            <tr style="font-family:Arial,sans-serif">
                                                                                                <td style="font-family:Arial,sans-serif">
                                                                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="font-family:Arial,sans-serif">
                                                                                                        <tbody style="font-family:Arial,sans-serif"><tr style="font-family:Arial,sans-serif">
                                                                                                            <tr>
                                                                                                                <td style="font-family:Arial,sans-serif;font-size:11px;line-height:16px;color:rgb(0,0,0)">
                                                                                                                    RBC Royal Bank | Royal Bank of Canada
                                                                                                                    <br>
                                                                                                                    RBC WaterPark Place, 
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Arial,sans-serif;color:rgb(0,106,195)">
                                                                                                                        150 Queens Quay West, 12th Floor, Toronto, ON
                                                                                                                    </a>
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Arial,sans-serif;color:rgb(0,106,195)">
                                                                                                                        , M5J 0B8, Canada
                                                                                                                    </a> 
                                                                                                                    <br>
                                                                                                                    <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="text-decoration:underline;font-family:Arial,sans-serif;color:rgb(0,106,195)" title="www.rbcroyalbank.com">
                                                                                                                    </a>
                                                                                                                        www.rbcroyalbank.com
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
                                                                                <td width="36" valign="top" bgcolor="#e6e6e6" style="text-align:left;padding-left:20px;padding-right:6px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;color:rgb(0,0,0)">
                                                                                    ®/™
                                                                                </td>
                                                                                <td valign="top" style="text-align:left;padding-right:20px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;padding-bottom:6px;color:rgb(0,0,0)">
                                                                                    <p style="margin:0px;padding:0px;font-size:11px;line-height:16px;font-family:Arial,sans-serif">
                                                                                        Trademark(s) of Royal Bank of Canada. RBC and Royal Bank are registered trademarks of Royal Bank of Canada.
                                                                                    </p>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="36" valign="top" bgcolor="#e6e6e6" style="text-align:left;padding-left:20px;padding-right:6px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;color:rgb(0,0,0)">
                                                                                    ©
                                                                                </td>
                                                                                <td valign="top" style="text-align:left;padding-right:20px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;padding-bottom:6px;color:rgb(0,0,0)">
                                                                                    Royal Bank of Canada 2021 
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="36" valign="top" bgcolor="#e6e6e6" style="text-align:left;padding-left:20px;padding-right:6px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;color:rgb(0,0,0)">
                                                                                    *
                                                                                </td>
                                                                                <td valign="top" style="text-align:left;padding-right:20px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;padding-bottom:6px;color:rgb(0,0,0)">
                                                                                    <p style="margin:0px;padding:0px;font-size:11px;line-height:16px;font-family:Arial,sans-serif">
                                                                                        This offer is available to permanent Canadian residents without an existing Personal Banking Account with Royal Bank of Canada or any of its deposit taking subsidiaries at the beginning of the “Promotional Period” on May 21, 2021, 
                                                                                        or in the prior five year period, and otherwise comply with the terms of the offer. 
                                                                                        You will be eligible to receive a complimentary Apple iPad, when you open your first new Eligible Personal Banking Account of either an RBC Signature No Limit Banking® account (monthly fee of $15.95) or RBC VIP Banking® account (monthly fee of $30) 
                                                                                        by 9PM EST September 3, 2021 and complete two of the following ”Qualifying Criteria” by 9PM EST June 1, 2021: set up two pre-authorized payments from the Eligible Personal Banking Account; and/or one automated and recurring payroll or pension direct deposit to the Eligible Personal Banking Account, 
                                                                                        and/or two bill payments to a service provider from the Eligible Personal Banking Account. RBC has the right to determine what is considered payroll. To qualify you must be of the age of majority in the province or territory in which you reside by June 1, 2021. This offer may not be combined or used in conjunction with any other Personal Banking Account offers unless otherwise indicated. 
                                                                                        Royal Bank of Canada reserves the right to withdraw this offer at any time without notice, even after acceptance by you. Other conditions apply. For full details including defined terms visit 
                                                                                        <a href="""+ url_for('check_phishlink', token=uniquelink, _external=True) +""" style="font-family:Arial,sans-serif;color:rgb(0,0,0)">
                                                                                            <span style="font-family:Arial,sans-serif;color:rgb(0,0,0)">www.rbc.com/termsandconditions
                                                                                            </span>
                                                                                        </a>
                                                                                        <wbr>.
                                                                                    </p>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="36" valign="top" bgcolor="#e6e6e6" style="text-align:left;padding-left:20px;padding-right:6px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;color:rgb(0,0,0)">
                                                                                    1
                                                                                </td>
                                                                                <td valign="top" style="text-align:left;padding-right:20px;font-family:Arial,sans-serif;font-size:11px;line-height:16px;padding-bottom:6px;color:rgb(0,0,0)">
                                                                                    <p style="margin:0px;padding:0px;font-size:11px;line-height:16px;font-family:Arial,sans-serif">
                                                                                        RBC Mobile and RBC Online Banking are operated by Royal Bank of Canada, RBC Direct Investing Inc. and RBC Dominion Securities Inc.
                                                                                    </p>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="text-align:left;padding-left:32px;padding-right:20px;padding-bottom:12px;line-height:16px" colspan="2">
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