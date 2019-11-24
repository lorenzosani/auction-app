from rest_framework import serializers

from .models import Item

class ActiveAuctionsSerializer(serializers.ModelSerializer):
 class Meta:
    model = Item
    fields = ['title', 'end_time', 'description']