
# Whether to send SMTP 'Date' header in the local time zone or in UTC.
EMAIL_USE_LOCALTIME = True

# for test
EMAIL_BACKEND = 'djangomail.backends.console.EmailBackend'

# for prod
# EMAIL_BACKEND = 'djangomail.backends.smtp.EmailBackend'


EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '***'
EMAIL_HOST_PASSWORD = '***'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

