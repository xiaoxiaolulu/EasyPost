from rest_framework import serializers
from api.models.project import Project
from api.schema.user import UserSimpleSerializers


class ProjectSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class UpdateAvatarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['avatar']
