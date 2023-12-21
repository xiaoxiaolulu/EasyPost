from rest_framework import serializers
from api.models.https import (
    Relation,
    Api
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
