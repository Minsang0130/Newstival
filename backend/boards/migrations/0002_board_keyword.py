# Generated by Django 4.2.16 on 2024-11-20 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='keyword',
            field=models.CharField(default='default_keyword', max_length=50, verbose_name=''),
            preserve_default=False,
        ),
    ]