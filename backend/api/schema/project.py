from rest_framework import serializers
from api.dao.project import ProjectDao
from api.models.project import Project
from api.schema.user import UserSimpleSerializers


class ProjectSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    @staticmethod
    def validate_name(value):
        if ProjectDao.project_name_validate(value):
            raise serializers.ValidationError('项目名称已存在!')
        return value

    class Meta:
        model = Project
        fields = "__all__"


class UpdateAvatarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['avatar']
