# Generated by Django 5.1.4 on 2024-12-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('type_of_appointment', models.CharField(choices=[('general', 'General Consultation'), ('followup', 'Follow-Up'), ('urgent', 'Urgent Care')], max_length=20)),
                ('place', models.CharField(max_length=100)),
            ],
        ),
    ]
