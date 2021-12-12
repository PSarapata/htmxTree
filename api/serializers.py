from rest_framework import serializers
from api import models

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tree
        fields = ('id', 'parent_row_id', 'row_id', 'row_description')

    parent_row_id = serializers.SerializerMethodField('_get_parent_row_id')
    row_id = serializers.SerializerMethodField('_get_row_id')
    row_description = serializers.SerializerMethodField('_get_row_description')

    def _get_parent_row_id(self, obj):
        return obj.parent_row_id

    def _get_row_id(self, obj):
        return obj.row_id

    def _get_row_description(self, obj):
        return f'{obj.row.name}'
