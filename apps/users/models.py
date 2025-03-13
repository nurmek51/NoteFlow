from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    favorite_subjects = models.ManyToManyField('materials.Subject', related_name='favorite_users', blank=True)


    favorite_lecturers = models.ManyToManyField("materials.Lecturer", related_name='favorite_lecturers', blank=True)
    def __str__(self):
        return self.username

class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='study_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name