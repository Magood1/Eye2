from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, filters, viewsets
from .models import Doctor, Patient, Appointment, Bill, MedicalData, Diagnose, TreatmentPlan
from .serializers import (DoctorSerializer, PatientSerializer,  AppointmentSerializer,
                                BillSerializer, MedicalDataSerializer,  DiagnoseSerializer, TreatmentPlanSerializer, )


from .classifier.classifier_component import EyesModel, Diagnoser
from .classifier.preprocessingStrategy import ( CataractPreprocessing, DiabetesPreprocessing, GlaucomaPreprocessing,
                                                     HypertensionPreprocessing, PathologicalMyopiaPreprocessing, AgeIssuesPreprocessing)

diagnoser = Diagnoser()
diagnoser.add_model(EyesModel("cataract.h5", CataractPreprocessing()))
diagnoser.add_model(EyesModel("diabetes.h5", DiabetesPreprocessing()))
diagnoser.add_model(EyesModel("glaucoma.h5", GlaucomaPreprocessing()))
diagnoser.add_model(EyesModel("hypertension.h5", HypertensionPreprocessing()))
diagnoser.add_model(EyesModel("myopia.h5", PathologicalMyopiaPreprocessing()))
diagnoser.add_model(EyesModel("age.h5", AgeIssuesPreprocessing()))

"""
remaind: add  predictions = diagnoser.predict(left_image_data, right_image_data)
in the MedicalData ViewSet instate of classification = getPartialDisease(left_fundus, right_fundus) 
but we before do that we should to modify formal 'predictions' and make it as 'classification' to serialize it to db and response

we may need import this here or in classifier's files:
from django.db import models
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import tensorflow as tf
import numpy as np
import os
from abc import ABC, abstractmethod

import threading
from django.core.files.uploadedfile import InMemoryUploadedFile
from .utils import ModelLoaderFactory, PreprocessingFactory


"""



def getPartialDisease(a1,a2):
    return {
        'left_diagnostic' : 'Happy',
        'right_diagnostic': 'Sad',
    }

# Doctor ViewSet
class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Doctor instances.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
        
    def get_queryset(self):
        return self.queryset


# Patient ViewSet
class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Patient instances.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data['doctor'] = Doctor.objects.get(doctor_id=1)
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.validated_data['doctor'] = Doctor.objects.get(doctor_id=1)
        serializer.save()
    

# Appointment ViewSet
class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Appointment instances.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data['doctor'] = Doctor.objects.get(doctor_id=1)
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.validated_data['doctor'] = Doctor.objects.get(doctor_id=1)
        serializer.save()

# Bill ViewSet
class BillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Bill instances.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
        
    def get_queryset(self):
        return self.queryset


# MedicalData ViewSet
class MedicalDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing MedicalData instances.
    """
    queryset = MedicalData.objects.all()
    serializer_class = MedicalDataSerializer

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        left_fundus = self.request.data.get("left_fundus")
        right_fundus = self.request.data.get("right_fundus")

        if left_fundus and right_fundus:
            
            classification = getPartialDisease(left_fundus, right_fundus)
            # Update validated data with classification and pneumonia status
            serializer.validated_data['doctor'] = Doctor.objects.get(doctor_id=1)
            serializer.validated_data['left_diagnostic'] = classification['left_diagnostic']
            serializer.validated_data['right_diagnostic'] = classification['right_diagnostic']
        
            serializer.save()
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        left_fundus = self.request.data.get("left_fundus")
        right_fundus = self.request.data.get("right_fundus")

        if left_fundus and right_fundus:
            
            classification = getPartialDisease(left_fundus, right_fundus)
            # Update validated data with classification and pneumonia status
            serializer.validated_data['doctor'] = Doctor.objects.get(doctor_id=1)
            serializer.validated_data['left_diagnostic'] = classification['left_diagnostic']
            serializer.validated_data['right_diagnostic'] = classification['right_diagnostic']
        
            serializer.save()
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Diagnose ViewSet
class DiagnoseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Diagnose instances.
    """
    queryset = Diagnose.objects.all()
    serializer_class = DiagnoseSerializer

    def get_queryset(self):
        return self.queryset

    
# TreatmentPlan ViewSet
class TreatmentPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing TreatmentPlan instances.
    """
    queryset = TreatmentPlan.objects.all()
    serializer_class = TreatmentPlanSerializer
    
    def get_queryset(self):
        return self.queryset
