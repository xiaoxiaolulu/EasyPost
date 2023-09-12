import re
from rest_framework import serializers
from api.models.setting import (
    Address,
    TestEnvironment
)
from api.schema.user import UserSimpleSerializers


# ULR正则表达式
REGEX_URL_PATH = "(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"


class TestEnvironmentSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    # def validate(self, attrs):
    #     # 验证url是否合法
    #     host_address = attrs.get('host_address')
    #     if not re.match(REGEX_URL_PATH, host_address):
    #         raise serializers.ValidationError("请输入正确的URL地址")
    #
    #     # if 'user' in self.initial_data.keys():
    #     #     userid = int(self.initial_data.get('user'))
    #     #     attrs['user'] = User.objects.get(id=userid)
    #     return attrs

    class Meta:
        model = TestEnvironment
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        # 验证url是否合法
        host_address = attrs.get('host')
        if not re.match(REGEX_URL_PATH, host_address):
            raise serializers.ValidationError("请输入正确的URL地址")

        # if 'user' in self.initial_data.keys():
        #     userid = int(self.initial_data.get('user'))
        #     attrs['user'] = User.objects.get(id=userid)
        return attrs

    class Meta:
        model = Address
        fields = "__all__"
