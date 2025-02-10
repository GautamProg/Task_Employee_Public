# employee_management/serializers/serializers.py
from rest_framework import serializers

class ContactDetailsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()

class AddressDetailsSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=255)
    landmark = serializers.CharField(max_length=255)

class EmployeeCreateSerializer(serializers.Serializer):
    personal_details = serializers.DictField()
    contact_details = ContactDetailsSerializer()
    address_details = AddressDetailsSerializer()

class EmployeeResponseSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    password = serializers.CharField()
    employee_name = serializers.CharField()
    department = serializers.CharField()
    manager = serializers.DictField()