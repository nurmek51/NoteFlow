from django.contrib import admin
from .models import Comment, Subject, StudyMaterial, Tag, Lecturer, Vote

admin.site.register(Comment)
admin.site.register(Subject)
admin.site.register(Tag)
admin.site.register(StudyMaterial)
admin.site.register(Lecturer)
admin.site.register(Vote)