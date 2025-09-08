from decouple import config
import os

class Config(object):
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    ENVIRONMENT = config('ENVIRONMENT', default='development')
    DEBUG = config('DEBUG', default=True, cast=bool)
    
    # Stripe Configuration
    STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
    STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
    STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
    
    # Email Configuration
    SMTP_SERVER = config('SMTP_SERVER', default='')
    SMTP_PORT = config('SMTP_PORT', default=587, cast=int)
    EMAIL_USER = config('EMAIL_USER', default='')
    EMAIL_PASSWORD = config('EMAIL_PASSWORD', default='')
    
    # CORS Configuration
    CORS_ORIGINS = config('CORS_ORIGINS', default='http://localhost:4200').split(',')
    
    # Application Configuration
    HOST = config('HOST', default='localhost')
    PORT = config('PORT', default=5000, cast=int)

