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
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('DOCX', 'DOCX'),
        ('PPTX', 'PPTX'),
        ('TXT', 'TXT'),
        ('PNG', 'PNG'),
        ('JPG', 'JPG'),
        ('HEIC', 'HEIC'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_materials')
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='PDF')
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


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='votes')
    vote = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'material')

    def __str__(self):
        return f"{self.user.username} voted {self.vote} on {self.material.title}"
