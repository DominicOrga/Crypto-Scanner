from django.test import TestCase
from strata.views import email
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

# Create your tests here.
# class UtilTest(TestCase):

# 	def test_rsi(self):
# 		close_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 
# 						46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46, 46.03, 46.41, 46.22, 
# 						45.64, 46.21]

# 		a, b, c = scanner.rsi(close_prices)
# 		self.assertTrue(abs(c - 62.93) < 1)

# 		a, b, c = scanner.update_rsi(a, b, 46.25 - close_prices[-1])
# 		self.assertTrue(abs(c - 63.26) < 1)

# 		a, b, c = scanner.update_rsi(a, b, 45.71 - 46.25)
# 		self.assertTrue(abs(c - 56.06) < 1)

# 		a, b, c = scanner.update_rsi(a, b, 46.45 - 45.71)
# 		self.assertTrue(abs(c - 62.38) < 1)

class EmailTest(TestCase):
	
	def test_email(self):

		subject = "Strata A: New Buy Signal"
		message = ""
		sender = settings.EMAIL_HOST_USER
		receiver = ["dominicorga@gmail.com"]

		# send_mail(subject, message, sender, receiver)
		# print(sender)
		email = EmailMessage(subject, message, receiver)
		email.send()
		pass