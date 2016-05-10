import smtplib

GOOGLE_ACCOUNT = "noreply@arientosend.com"
GOOGLE_PASSWORD = "passwordhere"

class emailer:
    # maybe rewrite this class to have email connection persist throughout emails
    def sendmail(to_email, subject, content):

        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (GOOGLE_ACCOUNT, ", ".join(to_email), subject, content)
        
        mail = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail.login(GOOGLE_ACCOUNT,GOOGLE_PASSWORD)
        mail.sendmail(GOOGLE_ACCOUNT, to_email, message)
        mail.close()