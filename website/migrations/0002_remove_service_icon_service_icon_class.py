# Generated by Django 5.1.3 on 2024-11-12 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='icon',
        ),
        migrations.AddField(
            model_name='service',
            name='icon_class',
            field=models.CharField(default='icon-laptop2', help_text="Enter the icon CSS class (e.g., 'icon-laptop2')", max_length=50),
        ),
    ]
