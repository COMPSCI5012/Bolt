# Generated by Django 3.2.6 on 2021-08-06 20:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bolt', '0005_auto_20210806_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='adoption_date',
        ),
        migrations.RemoveField(
            model_name='animal',
            name='adoption_status',
        ),
        migrations.AlterField(
            model_name='adopt',
            name='adoption_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='adopt',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bolt.animal'),
        ),
        migrations.AlterField(
            model_name='adopt',
            name='caretaker',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='caretaker', to='bolt.userprofile'),
        ),
        migrations.AlterField(
            model_name='adopt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adopter', to='bolt.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='shelter',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='caretaker', to='bolt.shelter'),
        ),
    ]