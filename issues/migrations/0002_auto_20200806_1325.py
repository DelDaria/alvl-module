# Generated by Django 3.0.7 on 2020-08-06 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Pending', 'Pending'), ('Declined', 'Declined'), ('In progress', 'In progress'), ('Done', 'Done')], default='Dr', max_length=11),
        ),
    ]
