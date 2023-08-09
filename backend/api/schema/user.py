from rest_framework import serializers
from api.models.user import User


class UserSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'nickname',
            'avatar'
        )
