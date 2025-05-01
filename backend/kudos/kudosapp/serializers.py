from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Kudos, Organization, User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repassword = serializers.CharField(write_only=True)
    organization = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "repassword",
            "organization",
        ]

    def validate(self, data):
        password = data["password"]
        repassword = data["repassword"]

        if password != repassword:
            raise ValidationError(
                {"repassword": "password and repassword do not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("repassword")
        org_name = validated_data.pop("organization")  # Get the org name

        # Get or create the organization by name
        organization, _ = Organization.objects.get_or_create(name=org_name)

        # Create the user with the resolved organization
        user = get_user_model().objects.create_user(
            organization=organization, **validated_data
        )
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
        fields = [
            "id",
            "sender",
            "receiver",
            "sender_first_name",
            "sender_last_name",
            "message",
            "timestamp",
        ]

    def validate(self, data):
        sender = self.context["request"].user  # Get sender from request

        receiver_email = self.initial_data.get(
            "receiver"
        )  #  Use initial_data to get receiver

        if not receiver_email:
            raise ValidationError({"receiver": "This field is required."})

        if sender.email == receiver_email:
            raise ValidationError(
                {"receiver": "Receiver cannot be the sender."}
            )

        try:
            receiver = User.objects.get(email=receiver_email)
        except User.DoesNotExist:
            raise ValidationError({"receiver": "Receiver not found."})

        if sender.organization != receiver.organization:
            raise ValidationError(
                "Users must belong to the same organization to give kudos."
            )

        # Replace receiver email with the actual receiver object before saving
        data["receiver"] = receiver
        return data


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        user = self.context["request"].user
        if not user.check_password(data["old_password"]):
            raise ValidationError(
                {"old_password": "Old password is incorrect."}
            )
        if not len(data["new_password"]) >= 8:
            raise ValidationError(
                {
                    "new_password": "Password must be at least 8 characters long."
                }
            )
        return data

    def update(self, instance, validated_data):
        new_password = validated_data["new_password"]
        instance.set_password(new_password)
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist."
            )
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value


class KudosRemainingSerializer(serializers.Serializer):
    kudos_remaining = serializers.SerializerMethodField()

    def get_kudos_remaining(self, obj):
        """Returns the number of Kudos the user can still give within the 7-day limit."""
        kudos_limit = 3  # Set the weekly limit
        one_week_ago = now() - timedelta(days=7)

        given_kudos_count = Kudos.objects.filter(
            sender=obj, timestamp__gte=one_week_ago
        ).count()

        return max(kudos_limit - given_kudos_count, 0)
