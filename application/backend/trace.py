import re
from application.model import Phishingcampaign, Phishingresult, Userpoints
from application import db
    
def Click():
    log_path='/var/log/nginx/access.log'
    clicks = Phishingresult.query.all()
    for click in clicks:
        with open(log_path) as log:
            for line in log:
                parseRegex = r"GET \/" + re.escape('index') + click.phish_link
                match = re.search(parseRegex, line)
                if match:
                    if click.phish_click == False:
                        click.phish_click = True
                        db.session.commit()
                        clickrecord = Userpoints(reason='Click the fake hyperlink in phishing simulation' + ' "' + click.campaign.campaign_name + '"', points_id=5, user_id=click.user_id)
                        db.session.add(clickrecord)
                        db.session.commit()
    return clicks, log_path