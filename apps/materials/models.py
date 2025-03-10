from django.db import models
from ..users.models import User

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lecturers = models.ManyToManyField('Lecturer', related_name='subjects', blank=True)

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_materials')
    file = models.FileField(upload_to='materials/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    materials = models.ManyToManyField(StudyMaterial, related_name='tags', blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.material.title}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'material')

    def __str__(self):
        return f'{self.user.username} liked {self.material.title}'
