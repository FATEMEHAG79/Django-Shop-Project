from rest_framework import serializers
from apps.user.models import Address

class AdressSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=["province","zip","apartment_address","phone_number_reciver","first_name_recivier","last_name_recivier","id"]