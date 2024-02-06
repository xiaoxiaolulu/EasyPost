from rest_framework import serializers
from api.models.report import (
    Main,
    Detail,
    DetailStep
)


class ReportDetailStepSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DetailStep
        fields = '__all__'
        read_only_fields = ('name', 'log_data', 'method', 'url', 'status_code',
                            'response_header', 'requests_header', 'response_body',
                            'requests_body', 'state', 'run_time', 'validate_extractor',
                            'extras')


class ReportDetailSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    step = ReportDetailStepSerializer(many=True, read_only=True)

    class Meta:
        model = Detail
        fields = "__all__"
        read_only_fields = (
            'name',
            'state',
            'all',
            'success',
            'error',
            'fail',
            'step'
        )


class ReportMainSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    detail = ReportDetailSerializers(many=True, read_only=True)

    class Meta:
        model = Main
        fields = '__all__'
        read_only_fields = ('name', 'state', 'all', 'success', 'error',
                            'fail', 'runtime', 'begin_time', 'argtime',
                            'pass_rate', 'tester', 'detail')
