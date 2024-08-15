from rest_framework import serializers
from api.models.report import (
    Main,
    Detail,
    DetailStep
)


class ReportMainSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Main
        fields = '__all__'
        read_only_fields = ('name', 'state', 'all', 'success', 'error',
                            'fail', 'runtime', 'begin_time', 'argtime',
                            'pass_rate', 'tester', 'detail')


class ReportDetailStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetailStep
        fields = '__all__'


class ReportDetailSerializers(serializers.ModelSerializer):

    steps = ReportDetailStepSerializer(many=True, read_only=True)

    class Meta:
        model = Detail
        fields = '__all__'
