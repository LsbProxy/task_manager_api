from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, Comment, Sprint, Dashboard


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = [
            'id',
            'title',
            'description',
            'created_date',
            'updated_date',
            'members',
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']

    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        return list(map(lambda member: member.username, obj.members.all()))


class CreateUpdateDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = [
            'id',
            'title',
            'description',
            'created_date',
            'updated_date',
            'members',
        ]
        read_only_fields = ['id', 'created_date', 'updated_date', 'members']

    members = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=150), write_only=True, allow_empty=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance.members:
            username_list = []

            for user in instance.members.all():
                username_list.append(user.username)

            ret['members'] = username_list

        return ret


class ListCreateSprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'id',
            'title',
            'description',
            'dashboard',
            'created_date',
            'updated_date',
            'end_date',
        ]
        read_only_fields = ['id',
                            'created_date', 'updated_date']


class RetrieveUpdateDestroySprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'id',
            'title',
            'description',
            'created_date',
            'updated_date',
            'end_date',
            'tasks',
        ]
        read_only_fields = ['id', 'end_date',
                            'created_date', 'updated_date', 'tasks']

    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = TaskSerializer(obj.task_set.all(), many=True)
        return tasks.data


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status',
                  'created_date', 'updated_date', 'id', 'author', 'sprint']
        read_only_fields = ['created_date', 'updated_date', 'id']

    def get_author(self, obj):
        return obj.author.username if obj.author else obj.author


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status',
                  'created_date', 'updated_date', 'author', 'assigned_to', 'sprint']
        read_only_fields = ['id', 'created_date', 'updated_date']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance.assigned_to:
            ret['assigned_to'] = instance.assigned_to.username

        if instance.author:
            ret['author'] = instance.author.username

        return ret


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'created_date',
                  'updated_date', 'task', 'id', 'author']
        read_only_fields = ['created_date', 'updated_date', 'id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.username
        return ret

    def to_internal_value(self, data):
        if not int(data['author']):
            user = User.objects.get(username=data['author'])
            data['author'] = user.id

        ret = super().to_internal_value(data)

        return ret
