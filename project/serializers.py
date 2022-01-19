from rest_framework import serializers
from project import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"
        read_only_fields = ["user"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = "__all__"
