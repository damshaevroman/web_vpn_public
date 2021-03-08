from rest_framework import serializers
from backupsender.models import ReportBackupBase


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportBackupBase
        fields = '__all__'
