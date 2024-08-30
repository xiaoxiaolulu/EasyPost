from rest_framework import serializers
from api.models.setting import (
    TestEnvironment,
    DataSource,
    Functions,
    BindDataSource,
    Notice,
    DataStructure
)
from api.schema.user import UserSimpleSerializers


# ULR正则表达式
REGEX_URL_PATH = "(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"


class DataSourceSerializers(serializers.ModelSerializer): # noqa

    id = serializers.IntegerField(read_only=True)
    creator = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DataSource
        fields = "__all__"


class BindDataSourceSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    creator = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BindDataSource
        fields = "__all__"


class TestEnvironmentSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)  # noqa
    data_source = BindDataSourceSerializers(many=True, read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    # def validate(self, attrs):
    #     # 验证url是否合法
    #     host_address = attrs.get('host')
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
        read_only_fields = ('name', 'server', 'variables', 'remarks',
                            'user', 'create_time', 'update_time',
                            'data_source')


class FunctionsSerializers(serializers.ModelSerializer):  # noqa

    id = serializers.IntegerField(read_only=True)
    creator = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Functions
        fields = "__all__"


class NoticeSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    creator = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notice
        fields = "__all__"


class DataStructureSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    creator = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DataStructure
        fields = "__all__"
