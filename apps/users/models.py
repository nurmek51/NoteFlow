from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
def validate_avatar_extension(value):
    ALLOWED_AVATAR_EXTENSIONS = ['jpg', 'jpeg', 'png']
    ext = value.name.split('.')[-1]
    if ext.lower() not in ALLOWED_AVATAR_EXTENSIONS:
        raise ValidationError(f"Invalid extension: {ext}. Extension must be one of {ALLOWED_AVATAR_EXTENSIONS}")
def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("File is to big! (maximum 5MB)")

class User(AbstractUser):
    profile_picture = models.FileField(upload_to="users/",validators=[validate_avatar_extension, validate_file_size],blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    favorite_subjects = models.ManyToManyField('materials.Subject', related_name='favorite_users', blank=True)


    favorite_lecturer = models.ForeignKey("materials.Lecturer", related_name='favoriting_users',null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='study_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name