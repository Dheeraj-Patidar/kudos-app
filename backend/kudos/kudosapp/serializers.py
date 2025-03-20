from rest_framework import serializers
from .models import User, Kudos, Organization
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repassword = serializers.CharField(write_only=True)
    organization = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "repassword", "organization"]

    def validate(self, data):
        password = data['password']
        repassword = data['repassword']

        if password != repassword:
            raise ValidationError({"password": "password and repassword do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop("repassword") 
        org_name = validated_data.pop("organization")  # Get the org name

        # Get or create the organization by name
        organization, _ = Organization.objects.get_or_create(name=org_name)

        # Create the user with the resolved organization
        user = get_user_model().objects.create_user(organization=organization, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "organization_name"]
    
    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = ["id", "name"]


class KudosSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = serializers.CharField(source="receiver.email", read_only=True)

    class Meta:
        model = Kudos
        fields = ["id", "sender", "receiver", "message", "timestamp"]
    
    def validate(self, data):
        sender = self.context["request"].user  # Get sender from request

        receiver_email = self.initial_data.get("receiver")  #  Use initial_data to get receiver

        if not receiver_email:
            raise ValidationError({"receiver": "This field is required."})

        if sender.email == receiver_email:
            raise ValidationError({"receiver": "Receiver cannot be the sender."})

        try:
            receiver = User.objects.get(email=receiver_email)
        except User.DoesNotExist:
            raise ValidationError({"receiver": "Receiver not found."})

        if sender.organization != receiver.organization:
            raise ValidationError("Users must belong to the same organization to give kudos.")

        # Replace receiver email with the actual receiver object before saving
        data["receiver"] = receiver  
        return data
    

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data["old_password"]):
            raise ValidationError({"old_password": "Incorrect password."})

        return data
    
    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance