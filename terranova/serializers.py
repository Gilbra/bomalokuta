from rest_framework import serializers
from .models import CustomUser, Dechet, PointCollecte, Evenement, Statistique, Recompense
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'avatar',
            'email_verified',
            'email_validation_token',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined'
        ]
        read_only_fields = ['email_verified', 'email_validation_token', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            avatar=validated_data.get('avatar', None),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_associated', 'points', 'role']

class DechetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dechet
        fields = ['id', 'utilisateur', 'photo', 'description', 'latitude', 'longitude', 'statut', 'date_signalement']
        read_only_fields = ['date_signalement']
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("La latitude doit être comprise entre -90 et 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("La longitude doit être comprise entre -180 et 180.")
        return value
    
class PointCollecteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointCollecte
        fields = ['id', 'nom', 'latitude', 'longitude', 'niveau_remplissage', 'type']

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = ['id', 'utilisateur', 'titre', 'description', 'date', 'lieu']

class StatistiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistique
        fields = ['utilisateur', 'dechets_signalés', 'dechets_recyclés', 'date']
        read_only_fields = ['date']

class RecompenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recompense
        fields = ['id', 'nom', 'description', 'points']