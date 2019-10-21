import datetime
import re

WEB_SCRAPPING_PARSER = 'html.parser'
HOUR_REGEX = r'([01]\d|2[0-3]):[0-5]\d'
AIRPORT_SCHEDULE_UPDATE_TAG_ID = 'ctl00_rptIncomingFlights_ctl00_pInformationStatusMessage'


def extract_airport_schedule_update_time(update_message):
    current_datetime = datetime.datetime.now()
    year, month, day = current_datetime.year, current_datetime.month, current_datetime.day
    last_update_hour_string = re.search(HOUR_REGEX, update_message).group(0)
    hour, seconds = map(int, last_update_hour_string.split(':'))
    return datetime.datetime(year, month, day, hour, seconds)
