# Generated by Django 4.2.5 on 2023-10-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0005_alter_programm_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedition',
            name='DateApproving',
            field=models.DateTimeField(auto_now=True, help_text='Дата утверждения экспедиции', null=True),
        ),
    ]
