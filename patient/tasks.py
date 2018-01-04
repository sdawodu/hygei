from .models import Patient
from celery import shared_task
from django.conf import settings
from messaging.sms import SMSLiveManager, SMSDummyManager


@shared_task
def send_booking_reminders():
	"""
	Send a reminder about appointments to every patient
	who is overdue a visit and hasn't booked an appointment
	"""
	if settings.DEBUG:
		sms_manager = SMSDummyManager()
	else:
		sms_manager = SMSLiveManager(
			settings.ROUTESMS_USER,
			settings.ROUTESMS_SUBACCT,
			settings.ROUTESMS_SUBACCT_PASSWORD,
		)
	# Don't want to send more than 3 reminders
	to_send = [
		patient
		for patient in Patient.objects.all()
		if (
			patient.is_due_appointment_booking() and
			patient.appointment_reminder_attempt <= 3
		)
	]

	print(to_send)
	# To do: Message personalisation
	# To do: Allow admin defined templates
	reminder = (
		"This is a test message. No action needed"
	)

	sent, msg_info = sms_manager.send_message(
		reminder,
		[i.mobile_phone_number for i in to_send]
	)
	if sent:
		for recipient in to_send:
			recipient.appointment_reminder_attempt += 1
			recipient.save()

