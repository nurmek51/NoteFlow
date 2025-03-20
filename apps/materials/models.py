from django.core.exceptions import ValidationError
from django.db import models
from ..users.models import User

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lecturers = models.ManyToManyField('Lecturer', related_name='subjects', blank=True)

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def validate_material_extension(value):
    ALLOWED_MATERIAL_EXTENSIONS = ['pdf','docx','pptx','txt','png','jpg','jpeg','heic']
    ext = value.name.split('.')[-1]
    if ext not in ALLOWED_MATERIAL_EXTENSIONS:
        raise ValidationError(f"Invalid file extension: {ext}. Extension must be one of {ALLOWED_MATERIAL_EXTENSIONS}")

def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("File is to big! (maximum 5MB)")

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class StudyMaterial(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_materials')
    file = models.FileField(upload_to='materials/', validators=[validate_material_extension, validate_file_size], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("materials.Tag",related_name="study_mater_of_tag", max_length=255, blank=True)

    def __str__(self):
        return self.title

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
