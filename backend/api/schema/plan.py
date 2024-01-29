from rest_framework import serializers
from api.models.plan import Plan
from api.schema.https import CaseSerializers
from api.schema.user import UserSimpleSerializers


class PlanSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = UserSimpleSerializers(required=False, default=serializers.CurrentUserDefault())
    case_list = CaseSerializers(many=True, read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Plan
        fields = "__all__"
