# Generated by Django 4.2 on 2025-03-16 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_profile_picture'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_messages', to='users.studygroup'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
