# Generated by Django 4.2 on 2025-03-12 15:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('materials', '0003_vote_studymaterial_file_format_delete_like_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_lecturer',
            field=models.ManyToManyField(blank=True, related_name='favorite_lecturers', to='materials.lecturer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favorite_subjects',
            field=models.ManyToManyField(blank=True, related_name='favorite_users', to='materials.subject'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(related_name='study_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
