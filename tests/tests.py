from djangomail import send_mail,send_mass_mail
from djangomail.conf import settings
import unittest
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
class MailTest(unittest.TestCase):
    receivers = ["xxxxx@163.com", "xxxxxx@qq.com"]
    def test_send_mail(self):
        x = send_mail(
            subject="邮件主题",
            message="邮件内容",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list= self.receivers,
        )
        self.assertTrue(x > 0)

    def test_send_mass_mail(self):
        x =send_mail(
            subject="邮件主题",
            message="邮件内容",
            html_message= '''<h1>邮件内容</h1>
        <h2>副标题</h2>
        <p>段落</p>''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=self.receivers,
        )
        self.assertTrue(x > 0)


    def test_send_html_mail(self):
        message1 = ('Subject here', 'Here is the message', settings.DEFAULT_FROM_EMAIL, self.receivers,)
        message2 = ('Another Subject', 'Here is another message', settings.DEFAULT_FROM_EMAIL, self.receivers,)
        x = send_mass_mail((message1, message2), fail_silently=False)

        self.assertTrue(x > 0)



if __name__ == '__main__':
    unittest.main()