from rest_framework import serializers
from train.models import Train, DoneMaiDate, Maintenance, Serial, Cases


class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('serial', 'slug',)


class TrainSerializer(serializers.ModelSerializer):
    serial = SerialSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ('id', 'serial', 'number', 'renter',
                  'mileage', 'mileage_date', 'day_mileage',)


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ('type', 'number',)


class DoneMaiDateSerializer(serializers.ModelSerializer):
    maintenance = MaintenanceSerializer(read_only=True)
    train = TrainSerializer(read_only=True)

    class Meta:
        model = DoneMaiDate
        exclude = ('musthave',)


class CaseSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)

    class Meta:
        model = Cases
        fields = ('author', 'train', 'name', 'text',)
