from rest_framework import serializers
from main.models import (
    Indicator,
    Report,
    Row,
    Target,
    Scale,
    Account,
    RowType,
    RowGroup1,
    RowGroup2,
    RowGroup3,
)


class AccountSerializer(serializers.ModelSerializer):
    """Account model serializer."""

    class Meta:
        model = Account
        fields = ('id', 'email',)


class FilterScaleAccountSerializer(serializers.ListSerializer):
    """Filter select unique accounts."""
    def to_representation(self, data):
        data = data.filter(year=self.context['year'], row_position=1)
        return super().to_representation(data)


class ScaleSerializer(serializers.ModelSerializer):
    """
    Scale model serializer.
    Nested serializer for Account model.
    Serializer connects Indicator model and Account model.
    Filter select only unique related accounts.
    """
    account = AccountSerializer(read_only=True)

    class Meta:
        list_serializer_class = FilterScaleAccountSerializer
        model = Scale
        fields = ('indicator', 'account')


class RowTypeSerializer(serializers.ModelSerializer):
    """RowType model serializer."""
    class Meta:
        model = RowType
        fields = ('name',)


class RowGroup1Serializer(serializers.ModelSerializer):
    """RowGroup1 model serializer."""
    class Meta:
        model = RowGroup1
        fields = ('name',)


class RowGroup2Serializer(serializers.ModelSerializer):
    """RowGroup2 model serializer."""
    class Meta:
        model = RowGroup2
        fields = ('name',)


class RowGroup3Serializer(serializers.ModelSerializer):
    """RowGroup3 model serializer."""
    class Meta:
        model = RowGroup3
        fields = ('name',)


class RowSerializer(serializers.ModelSerializer):
    """
    Row model serializer.
    Nested serializers for RowType, RowGroup1, RowGroup2, RowGroup3 serializers.
    """
    row_type = RowTypeSerializer(read_only=True)
    row_group1 = RowGroup1Serializer(read_only=True)
    row_group2 = RowGroup2Serializer(read_only=True)
    row_group3 = RowGroup3Serializer(read_only=True)

    class Meta:
        model = Row
        fields = ('id', 'name', 'row_type', 'row_type', 'row_group1', 'row_group2', 'row_group3')


class FilterReportRowSerializer(serializers.ListSerializer):
    """
    Filter Report model by <year> and <row_code> field.
    Filter(year=year and row_code__isnull=False).
    """
    def to_representation(self, data):
        data = data.filter(row_code__isnull=False, year=self.context['year'])
        return super().to_representation(data)


class ReportSerializer(serializers.ModelSerializer):
    """
    Report model serializer.
    Nested field for Row model serializer.
    Filter select rows by <year> and <row_code> fields.
    """
    row_code = RowSerializer(read_only=True)

    class Meta:
        list_serializer_class = FilterReportRowSerializer
        model = Report
        fields = ('row_code',)


class IndicatorLongDetailSerializer(serializers.ModelSerializer):
    """
    Indicator model serializer.
    Nested fields for Report and Scale model serializers.

    Get extra args as context dict. {'id': int, 'year': int}.
    """
    report_set = ReportSerializer(many=True)
    scale_set = ScaleSerializer(many=True)

    class Meta:
        model = Indicator
        fields = ('id', 'name', 'scale_set', 'report_set',)
