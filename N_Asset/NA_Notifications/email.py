from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError

from NA_DataLayer.exceptions import NAError, NAErrorConstant


class EmailSubject:
    USER_PASSWORD = 'Your Password'


class EmailNotification(object):

    def __init__(self, subject, body, from_email=settings.FROM_EMAIL):
        self.subject = subject
        self.body = body
        self.from_email = from_email

    def send(self, to=[], attachments=[]):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=to
        )
        if attachments:
            for attachment in attachments:
                email.attach(attachment)
        try:
            email.send()
        except BadHeaderError as e:
            raise NAError(
                error_code=NAErrorConstant.UNCAUGHT_ERROR,
                message=e
            )
