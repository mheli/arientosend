import smtplib
from django.conf import settings

GOOGLE_ACCOUNT = getattr(settings, "GOOGLE_ACCOUNT", None)
GOOGLE_PASSWORD = getattr(settings, "GOOGLE_PASSWORD", None)

class emailer:
    # maybe rewrite this class to have email connection persist throughout emails
    def sendmail(self, to_email, subject, content):

        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (GOOGLE_ACCOUNT, to_email, subject, content)
        
        mail = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail.login(GOOGLE_ACCOUNT,GOOGLE_PASSWORD)
        mail.sendmail(GOOGLE_ACCOUNT, to_email, message)
        mail.close()