from .models import Doctor, Patient, Appointment, Bill, MedicalData, Diagnose, TreatmentPlan
from rest_framework import serializers
from datetime import date


"""
  1.Optimizing Nested Serializers Using select_related or prefetch_related
    In your views, when retrieving patients with their doctor, you can optimize
    When using nested serializers, select_related and prefetch_related in views can improve database efficiency.
    queryset = Patient.objects.select_related('doctor').all()
  
  2.Use Partial=True for Update Operations
    Explanation: For PATCH operations, allow partial updates to only update specified fields.
    Implementation: In your views, remember to set partial=True in update calls if you want to allow partial updates. 
    For instance, when updating a Patient:
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs, partial=True)
    These changes will enhance the functionality, robustness, and usability of your serializers.

 """

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'first_name', 'last_name', 'specialty', 'phone', 'email']


class PatientSerializer(serializers.ModelSerializer):

    doctor = serializers.PrimaryKeyRelatedField(read_only=True)  # Embed detailed doctor data
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'patient_id', 'first_name', 'last_name', 'birthday', 'gender',
            'address', 'phone', 'insurance_info', 'personal_photo', 
            'contact_info', 'created_at', 'doctor', 'age',
        ]

        read_only_fields = ['patient_id', 'doctor', 'created_at', ]

    def get_age(self, obj):
        return date.today().year - obj.birthday.year


class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = [
            'record_id', 'patient', 'left_fundus', 'right_fundus', 
            'left_diagnostic', 'right_diagnostic', 
            'doctor', 'medical_notes', 'diagnose',
        ]

        read_only_fields = ['record_id', 'doctor', 'left_diagnostic', 'right_diagnostic','appointment_date']


class AppointmentSerializer(serializers.ModelSerializer):
    
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)  # Embed detailed doctor data
    
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient', 'appointment_datetime', 'doctor']

        read_only_fields = ['appointment_id', ]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['appointment_datetime'] = instance.appointment_datetime.strftime('%Y-%m-%d %H:%M')
        return representation


class TreatmentPlanSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)  # Embed detailed doctor data

    class Meta:
        model = TreatmentPlan
        fields = [
            'treatment_id', 'record', 'medication', 'dose', 
            'daily_activities', 'surgical_intervention', 'doctor', 
        ]


class DiagnoseSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)  # Embed detailed doctor data

    class Meta:
        model = Diagnose
        fields = ['diagnose_id', 'complete_diagnosis', 'confidence_score', 'diagnosis_notes', 'doctor']

        read_only_fields = ['diagnose_id', 'complete_diagnosis', 'confidence_score']


class BillSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)  # Embed detailed doctor data

    class Meta:
        model = Bill
        fields = ['bill_id', 'appointment', 'amount', 'issue_date', 'doctor']

        read_only_fields = ['bill_id', 'issue_date']




















