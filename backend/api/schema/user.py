from rest_framework import serializers
from api.models.user import (
    User,
    UserRole
)


class UserSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'nickname',
            'avatar'
        )


class UserRoleSerializers(serializers.ModelSerializer):

    user = UserSimpleSerializers(read_only=True)

    class Meta:
        model = UserRole
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    roles = UserRoleSerializers(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
