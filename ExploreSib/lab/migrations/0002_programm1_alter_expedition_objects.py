# Generated by Django 4.2.5 on 2023-10-15 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programm1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.IntegerField(help_text='Порядковый номер', null=True)),
                ('ID_Exp', models.ForeignKey(db_column='ID_Exp', on_delete=django.db.models.deletion.CASCADE, to='lab.expedition')),
                ('ID_Obj', models.ForeignKey(db_column='ID_Obj', on_delete=django.db.models.deletion.CASCADE, to='lab.object')),
            ],
        ),
        migrations.AlterField(
            model_name='expedition',
            name='Objects',
            field=models.ManyToManyField(through='lab.Programm1', to='lab.object'),
        ),
    ]