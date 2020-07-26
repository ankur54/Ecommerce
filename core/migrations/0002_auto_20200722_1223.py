# Generated by Django 2.1.5 on 2020-07-22 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='color',
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=10, null=True),
        ),
        migrations.DeleteModel(
            name='Color',
        ),
    ]
