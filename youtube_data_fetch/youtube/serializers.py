from rest_framework import serializers
from .models import ChannelData

class ChannelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelData
        fields = '__all__'
