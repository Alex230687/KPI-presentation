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
    """User info."""

    class Meta:
        model = Account
        fields = ('id', 'email',)


class FilterScaleAccountSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(year=self.context['year'], row_position=1)
        return super().to_representation(data)


class ScaleSerializer(serializers.ModelSerializer):
    """Scale info."""
    account = AccountSerializer(read_only=True)

    class Meta:
        list_serializer_class = FilterScaleAccountSerializer
        model = Scale
        fields = ('indicator', 'account')


class RowTypeSerializer(serializers.ModelSerializer):
    """Row type info."""
    class Meta:
        model = RowType
        fields = ('name',)


class RowGroup1Serializer(serializers.ModelSerializer):
    """Row group #1 info."""
    class Meta:
        model = RowGroup1
        fields = ('name',)


class RowGroup2Serializer(serializers.ModelSerializer):
    """Row group #2 info."""
    class Meta:
        model = RowGroup2
        fields = ('name',)


class RowGroup3Serializer(serializers.ModelSerializer):
    """Row group #3 info."""
    class Meta:
        model = RowGroup3
        fields = ('name',)


class RowSerializer(serializers.ModelSerializer):
    """Detailed row information."""
    row_type = RowTypeSerializer(read_only=True)
    row_group1 = RowGroup1Serializer(read_only=True)
    row_group2 = RowGroup2Serializer(read_only=True)
    row_group3 = RowGroup3Serializer(read_only=True)

    class Meta:
        model = Row
        fields = ('id', 'name', 'row_type', 'row_type', 'row_group1', 'row_group2', 'row_group3')


class FilterReportRowSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(row_code__isnull=False, year=self.context['year'])
        return super().to_representation(data)


class ReportSerializer(serializers.ModelSerializer):
    """Indicator report serializer."""
    row_code = RowSerializer(read_only=True)

    class Meta:
        list_serializer_class = FilterReportRowSerializer
        model = Report
        fields = ('row_code',)


class IndicatorLongDetailSerializer(serializers.ModelSerializer):
    """View selected indicator info."""
    report_set = ReportSerializer(many=True)
    scale_set = ScaleSerializer(many=True)

    class Meta:
        model = Indicator
        fields = ('id', 'name', 'scale_set', 'report_set',)
