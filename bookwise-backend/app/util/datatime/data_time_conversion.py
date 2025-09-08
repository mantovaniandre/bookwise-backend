import pytz
from datetime import datetime
from decouple import config


class DateTimeHelper:
    @staticmethod
    def get_current_datetime(timezone_str=None):
        """
        Get current datetime in specified timezone or UTC
        
        Args:
            timezone_str: Timezone string (e.g., 'America/Sao_Paulo', 'UTC')
                         If None, uses UTC
        
        Returns:
            datetime: Current datetime in specified timezone
        """
        if timezone_str is None:
            timezone_str = config('DEFAULT_TIMEZONE', default='UTC')
            
        target_timezone = pytz.timezone(timezone_str)
        utc_timezone = pytz.timezone('UTC')
        
        utc_now = datetime.utcnow().replace(tzinfo=utc_timezone)
        local_now = utc_now.astimezone(target_timezone)
        
        return local_now
    
    @staticmethod
    def get_utc_datetime():
        """Get current UTC datetime"""
        return datetime.utcnow().replace(tzinfo=pytz.UTC)
    
    @staticmethod
    def convert_to_timezone(dt, timezone_str):
        """
        Convert datetime to specified timezone
        
        Args:
            dt: datetime object
            timezone_str: Target timezone string
            
        Returns:
            datetime: Converted datetime
        """
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
        
        target_timezone = pytz.timezone(timezone_str)
        return dt.astimezone(target_timezone)


# Backward compatibility
class DataTimeConversion:
    @staticmethod
    def dataTimeConversionToSaoPaulo():
        """Deprecated: Use DateTimeHelper.get_current_datetime('America/Sao_Paulo')"""
        return DateTimeHelper.get_current_datetime('America/Sao_Paulo')
