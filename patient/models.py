import datetime
import logging
from django.db import models

from annoying.fields import AutoOneToOneField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class PatientRecord(models.Model):

	checkup_interval = models.IntegerField(default=180)
	next_required_visit = models.DateField(blank=True, null=True)

	def __str__(self):
		try:
			return "Record: {} {}".format(self.patient.first_name, self.patient.last_name)
		except Patient.DoesNotExist:
			return 'unlinked patient record'


	@property
	def next_due_appointment(self):

		print("Checking patient record")

		last_checkup_date = self.patient.last_visit or self.patient.registration_date
		next_checkup_date = datetime.timedelta(days=self.checkup_interval) + last_checkup_date
		print("Last Checkup date: %s" % last_checkup_date)
		print("Next Checkup date: %s" % next_checkup_date)
		if self.next_required_visit:
			print(min([next_checkup_date, next_required_visit]))
			return min([next_checkup_date, next_required_visit])

		return next_checkup_date


class Patient(models.Model):

	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	# date_of_birth = models.DateField()
	record = models.OneToOneField(PatientRecord, on_delete=models.CASCADE)

	registration_date = models.DateField()
	last_visit = models.DateField(blank=True, null=True)

	# Keep track of how many times we're sending messsages to people
	# to make sure we don't spam them
	appointment_reminder_attempt = models.IntegerField(default=0)

	email_address = models.EmailField(blank=True, null=True)
	mobile_phone_number = PhoneNumberField()


	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)

	@property
	def name(self):
		return str(self)

	def is_due_appointment_booking(self):
		# Do we have an appointment scheduled in the records?

		appointments = Appointment.objects.filter(
			patient=self,
			time__date__gte=datetime.datetime.today()
		)
		print("Apppointment for this patient: %s" % appointments)
		if appointments:
			return False
		else:
			return self.record.next_due_appointment < datetime.date.today()


class Provider(models.Model):
	# Deliberately not calling this "Doctor"
	# to allow for nurse/optometrist/someone else appointments
	name = models.CharField(max_length=64)
	title = models.CharField(max_length=64)

class Appointment(models.Model):

	time = models.DateTimeField()
	provider = models.ForeignKey(Provider, blank=True, null=True, on_delete=models.SET_NULL)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	notes = models.TextField()

	visited = models.NullBooleanField()


	def __str__(self):
		return "{} {}: {}".format(self.patient.first_name, self.patient.last_name, self.time)


	def complete_visit(self):
		updated = False
		if datetime.datetime.now() >= self.time:
			try:
				self.visited = True
				self.patient.last_visit = datetime.datetime.now()
				self.save()
				self.patient.save()
			except Exception as e:
				logging.execption("Failed to update patient visit times")
			else:
				updated = True
		else:
			logging.info(
				"You can't complete this appointment before it has happened"
			)

		return updated