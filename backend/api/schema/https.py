from rest_framework import serializers
from api.models.https import Relation


class RelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relation
        fields = '__all__'
