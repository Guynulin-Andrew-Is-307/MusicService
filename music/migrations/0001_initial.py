# Generated by Django 3.1.3 on 2020-11-11 14:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('artist', models.CharField(max_length=128)),
                ('path_to_file', models.FileField(upload_to='static/')),
                ('favority_by', models.ManyToManyField(related_name='favorite_song', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
