# Generated by Django 2.0 on 2018-01-03 16:13

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('notes', models.TextField()),
                ('visited', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('registration_date', models.DateField()),
                ('last_visit', models.DateField(blank=True, null=True)),
                ('appointment_reminder_attempt', models.IntegerField(default=0)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile_phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PatientRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkup_interval', models.IntegerField(default=180)),
                ('next_required_visit', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='record',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patient.PatientRecord'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Provider'),
        ),
    ]
