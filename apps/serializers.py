import os
from datetime import timedelta

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from rest_framework import serializers

from apps.models import Stadium, Order
from root import settings


# Create your views here.
class BookStadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'stadium', 'date', 'start_time', 'end_time', 'phone_number')

    def validate_phone_number(self, value):
        if value[0] == '+' and value[1:].isdigit():
            return value
        raise serializers.ValidationError('Contact phone number must be entered as +998...')

    def validate_start_time(self, value):
        if value.minute == 0 and value.second == 0:
            return value
        raise serializers.ValidationError('Choose only hours')

    def validate_end_time(self, value):
        if value.minute == 0 and value.second == 0:
            return value
        raise serializers.ValidationError('Choose only hours')

    def validate(self, attrs):
        validate = super().validate(attrs)
        stadium: Stadium = validate['stadium']
        boolean = stadium.order_set.filter(
            Q(start_time__lte=validate['start_time'], end_time__gt=validate['start_time']),
            date=validate['date'],

        ).exists()
        if boolean:
            raise serializers.ValidationError('Order already booked')
        return validate

    def create(self, validated_data):
        validated_data['hours'] = validated_data['end_time'].hour - validated_data['start_time'].hour
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def save(self, **kwargs):
        path = settings.MEDIA_ROOT
        storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, path))
        f = self.validated_data.get('image')
        self._file = storage.save(f.name, f)
        protocol = 'https' if self.context.get('request').is_secure() else 'http'
        file_url = f"{protocol}://{self.context.get('request').META['HTTP_HOST']}/media/{self._file}"
        return {'file': file_url}


class StadiumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('id', 'name', 'contact_name', 'contact_phone', 'price', 'address', 'images')

    def validate_contact_phone(self, value):
        if value[0] == '+' and value[1:].isdigit():
            return value
        raise serializers.ValidationError('Contact phone number must be entered as +998...')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_images(self, values):
        if len(values) == 1:
            values = values[0].split(',')
        for image in values:
            if image.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
                raise serializers.ValidationError('Only jpg, jpeg and png images are allowed')
        return values


class StadiumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('id', 'name', 'address', 'contact_name', 'price', 'images')


class StadiumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('id', 'name', 'contact_name', 'contact_phone', 'price', 'address', 'images')


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'stadium', 'date', 'start_time', 'end_time', 'phone_number', 'user')
