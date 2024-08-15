from rest_framework import serializers
from api.dao.project import ProjectDao
from api.models.project import (
    Project,
    ProjectRole
)
from api.schema.user import UserSimpleSerializers


class ProjectRoleSerializers(serializers.ModelSerializer):

    user = UserSimpleSerializers(read_only=True)

    class Meta:
        model = ProjectRole
        fields = "__all__"


class ProjectSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    roles = ProjectRoleSerializers(many=True, read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    # @staticmethod
    # def validate_name(value):
    #     if ProjectDao.project_name_validate(value):
    #         raise serializers.ValidationError('项目名称已存在!')
    #     return value

    def create(self, validated_data):
        name = validated_data.get("name")
        if ProjectDao.project_name_validate(name):
            raise serializers.ValidationError('项目名称已存在!❌')
        instance = ProjectDao.create_project_role(validated_data)
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Project
        fields = "__all__"


class UpdateAvatarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['avatar']


class ProjectListSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)  # noqa
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
