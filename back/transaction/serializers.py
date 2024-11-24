from account.serializers import UserSerializer
from post.serializers import PostSerializer
from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    cancelled_by = UserSerializer(read_only=True)

    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['coins_spent'] = instance.coins_spent
        data['status'] = instance.status
        data['seller_accepted'] = instance.seller_accepted
        return data
    class Meta:
        model = Reservation
        fields = ['id', 'buyer', 'post', 'quantity', 'coins_spent', 'status', 
                 'created_at', 'updated_at', 'reported_at_formatted', 'report_reason',  'seller_accepted', 'cancelled_by','coins_spent',]
        read_only_fields = [ 'status', 'seller_accepted', 'cancelled_by', 'reported_at_formatted']
