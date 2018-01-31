from rest_framework import serializers

class KeyDonationSerializer(serializers.Serializer):
    steamid64 = serializers.CharField()
    amount = serializers.IntegerField()
