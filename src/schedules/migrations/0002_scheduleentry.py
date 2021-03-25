# Generated by Django 3.1.7 on 2021-03-25 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.schedule')),
            ],
            options={
                'verbose_name_plural': 'Schedule entries',
            },
        ),
    ]