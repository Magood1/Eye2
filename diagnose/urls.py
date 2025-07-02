from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( DoctorViewSet, PatientViewSet, AppointmentViewSet, 
                        BillViewSet, MedicalDataViewSet, DiagnoseViewSet, TreatmentPlanViewSet
)

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'bills', BillViewSet)
router.register(r'medical-data', MedicalDataViewSet)
router.register(r'diagnoses', DiagnoseViewSet)
router.register(r'treatment-plans', TreatmentPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
