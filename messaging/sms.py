import requests
import re


class SMSLiveManager(object):

	def __init__(self, login_user, sub_acct, sub_acct_password):
		self.session_id = None
		self.login_user = login_user
		self.sub_acct = sub_acct
		self.sub_acct_password = sub_acct_password
		self.api_url = 'http://www.smslive247.com/http/index.aspx'

	def execute(self, cmd, data, method='get'):
		if cmd != 'login':
			if not self.session_id:
				self.session_id = self.login(
					self.login_user,
					self.sub_acct,
					self.sub_acct_password
				)
			data.update({'sessionid': self.session_id})
		data.update({'cmd': cmd})

		if method == 'get':
			execute_resp = requests.get(
				self.api_url,
				data
			)
		else:
			execute_resp = requests.post(
				self.api_url,
				data
			)

		# TO DO: Some top level error handling here
		return execute_resp.content

	def login(self, login_user, sub_acct, sub_acct_password):
		data = {
			'owneremail': login_user,
			'subacct': sub_acct,
			'subacctpwd': sub_acct_password
		}

		# Session ID in the form:
		# b'OK: b46e89b4-49b7-4158-9fac-214828874c9e'
		# Currently assuming a utf-8 encoding
		session_info = re.match(
			'^OK: (?P<session_id>.*)$',
			self.execute('login', data, 'post').decode('utf-8')
		)
		session_id = None
		if session_info:
			session_id = session_info.groupdict()['session_id']
		return session_id

	def send_message(self, message, recipients=None):
		if not recipients:
			recipients = []


		recipient_str = ','.join(recipients)


		data = {
			'sendto': recipient_str,
			'message': message,
			'msgtype': 0,
		}
		msg_info = self.execute('sendmsg', data, 'post')
		if 'OK' in msg_info:
			res = True
		else:
			res = False
		return (res, msg_info)


class SMSDummyManager(object):

	def send_message(self, message, recepients):
		print("Sending messages!!")
		for i in recepients:
			print("Sent message to %s" % i)