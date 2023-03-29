import pytz
from datetime import datetime


class DataTimeConversion:
    @staticmethod
    def dataTimeConversionToSaoPaulo():
        local_timezone = pytz.timezone('America/Sao_Paulo')
        utc_timezone = pytz.timezone('UTC')

        utc_now = datetime.utcnow().replace(tzinfo=utc_timezone)

        local_now = utc_now.astimezone(local_timezone)

        return local_now
