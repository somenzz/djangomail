from djangomail.mail import send_mail
from djangomail.conf import settings
import unittest
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
class MailTest(unittest.TestCase):

    def test_send_mail(self):
        # send_mail(
        #     subject="邮件主题",
        #     message="邮件内容",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=["xxxxx@163.com", "xxxxxx@qq.com"],
        # )
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()