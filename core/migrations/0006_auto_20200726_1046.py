# Generated by Django 2.1.5 on 2020-07-26 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_item_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='MODELNAME',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'MODELNAME',
                'verbose_name_plural': 'MODELNAMEs',
            },
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Transaction', 'verbose_name_plural': 'Transaction'},
        ),
    ]
