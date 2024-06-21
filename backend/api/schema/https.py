from rest_framework import serializers
from api.models.https import (
    Relation,
    Api,
    Case,
    Step,
    ClosedTasks
)
from api.schema.user import UserSimpleSerializers


class RelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relation
        fields = '__all__'


class ApiSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Api
        fields = '__all__'
        read_only_fields = ('name', 'project', 'directory_id', 'method', 'url',
                            'headers', 'priority', 'params', 'raw', 'status',
                            'priority', 'user', 'create_time', 'update_time',
                            'desc', 'setup_script', 'teardown_script', 'validate',
                            'extract')


class CaseStepSerializers(serializers.ModelSerializer):

    user = UserSimpleSerializers(read_only=True)

    class Meta:
        model = Step
        fields = "__all__"


class CaseSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    step = CaseStepSerializers(many=True, read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Case
        fields = "__all__"
        read_only_fields = ('name', 'project', 'directory_id', 'priority',
                            'rerun', 'threads', 'user', 'create_time',
                            'update_time', 'desc', 'step')


class ClosedTasksSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ClosedTasks
        fields = '__all__'
        read_only_fields = ('name', 'project', 'runnability', 'state',
                            'detail', 'user',  'create_time', 'update_time')
