# Generated by Django 4.2.5 on 2023-10-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_programm1_alter_expedition_objects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedition',
            name='Objects',
            field=models.ManyToManyField(through='lab.Programm', to='lab.object'),
        ),
    ]