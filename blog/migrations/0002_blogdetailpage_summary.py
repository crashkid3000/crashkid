# Generated by Django 2.2.9 on 2020-02-05 20:35

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogdetailpage',
            name='summary',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A short summary to get the user into reading more', verbose_name='Blog summary'),
        ),
    ]
