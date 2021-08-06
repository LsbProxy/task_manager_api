from .utils import remove_list_serializer_fields
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, Comment, Sprint, Dashboard


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
        user = User.objects.get(username=data['author'])
        data['author'] = user.id

        ret = super().to_internal_value(data)

        return ret


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status',
                  'created_date', 'updated_date', 'author', 'assigned_to', 'sprint', 'comments', 'dashboard']
        read_only_fields = ['created_date',
                            'updated_date', 'id', 'comments']

    comments = CommentSerializer(
        source='comment_set', many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)
        remove_list_serializer_fields(self, fields=['comments'], **kwargs)

    def to_internal_value(self, data):

        for key, username in data.items():
            if key in ['author', 'assigned_to']:
                data[key] = User.objects.get(username=username).id

        ret = super().to_internal_value(data)

        return ret

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance.assigned_to:
            ret['assigned_to'] = instance.assigned_to.username

        if instance.author:
            ret['author'] = instance.author.username

        return ret


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'id',
            'title',
            'description',
            'created_date',
            'updated_date',
            'end_date',
            'dashboard',
            'tasks',
        ]
        read_only_fields = ['id', 'created_date', 'updated_date', 'tasks']

    tasks = TaskSerializer(source='task_set', many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super(SprintSerializer, self).__init__(*args, **kwargs)
        remove_list_serializer_fields(self, fields=['tasks'], **kwargs)


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
            'sprints'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date', 'sprints']

    sprints = SprintSerializer(
        source='sprint_set', many=True, read_only=True)

    members = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=150), write_only=True, allow_empty=False)

    def __init__(self, *args, **kwargs):
        super(DashboardSerializer, self).__init__(*args, **kwargs)
        remove_list_serializer_fields(self, fields=['sprints'], **kwargs)

    def to_internal_value(self, data):
        if 'members' in data and data['members']:
            data['members'] = list(map(lambda username: User.objects.get(
                username=username).id, data['members']))

        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance.members:
            ret['members'] = list(
                map(lambda user: user.username, instance.members.all()))

        return ret
