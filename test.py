import datetime 
from datetime import timedelta
import pytz

utc=pytz.UTC

ad_post_time = datetime.datetime.now()
ad_duration =timedelta(seconds =50)
expiration = ad_post_time + ad_duration

print utc.localize(expiration)