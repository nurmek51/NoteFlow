from rest_framework import serializers
from .models import Subject, Lecturer, StudyMaterial, Tag, Comment, Vote

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = '__all__'

    def create(self, validated_data):
        tags_data = validated_data.pop('tags',[])
        study_material = StudyMaterial.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.get_or_create(name=tag_data['name'])
            study_material.tags.add(tag[0])

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
