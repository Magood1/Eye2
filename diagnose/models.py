from django.db import models
from django.utils import timezone
 
def getFullDisease(a1, a2, a3, a4):
    return {
        'complete_diagnosis' : 'Happy',
        'confidence_score': 0.94,
    }


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Diagnose(models.Model):
    diagnose_id = models.AutoField(primary_key=True)
    complete_diagnosis = models.TextField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    diagnosis_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diagnosis {self.diagnose_id}"

    


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    
    #Edit 1)
    #More reliable to use choices to avoid free-text inputs:
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    address = models.TextField()
    phone = models.CharField(max_length=15)
    insurance_info = models.CharField(max_length=100)
    personal_photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    contact_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #Edit 3) add "related_name" to make it easier to access related data.
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()

    def __str__(self):
        return f"Appointment {self.patient.first_name} {self.patient.last_name} - {self.appointment_datetime}"

    #Edit 2)     
    class Meta:
        """ to ensure that a patient and doctor cannot have multiple 
           appointments at the same time and that each appointment can only have one bill."""
        unique_together = ('patient', 'doctor', 'appointment_datetime')    


class MedicalData(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    appointment_date = models.OneToOneField(Appointment, on_delete=models.CASCADE, blank=True, null=True)
    diagnose = models.OneToOneField(Diagnose, on_delete=models.CASCADE, blank=True, null=True)
    
    left_fundus = models.ImageField(upload_to='fundus_images/', blank=True, null=True)
    right_fundus = models.ImageField(upload_to='fundus_images/', blank=True, null=True)
    left_diagnostic = models.CharField(max_length=255)
    right_diagnostic = models.CharField(max_length=255)
    medical_notes = models.TextField(blank=True, null=True)


    def save(self, *args, **kwargs):
        # Check if an appointment needs to be created
        if not self.appointment_date:
            self.appointment_date = Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                appointment_datetime=timezone.now()  # Current datetime
            )

        # Check if a diagnose needs to be created
        if not self.diagnose:
            # Call the getDisease function using parameters from MedicalData instance
            diagnosis_result = getFullDisease(self.left_fundus, self.right_fundus, self.left_diagnostic, self.right_diagnostic)
            
            # Create Diagnose object from getDisease output
            self.diagnose = Diagnose.objects.create(
                complete_diagnosis=diagnosis_result['complete_diagnosis'],
                confidence_score=diagnosis_result['confidence_score'],
                diagnosis_notes=" "
            )

        # Call the original save method to save the instance with the linked Appointment and Diagnose
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Medical Record {self.record_id} for {self.patient.first_name} {self.patient.last_name}"



class TreatmentPlan(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    #Edit 4) each record in MedicalData only has one treatment plan.
    record = models.OneToOneField(MedicalData, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dose = models.CharField(max_length=100)
    daily_activities = models.TextField()
    surgical_intervention = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment Plan {self.treatment_id} for Record {self.record_id}"


class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Bill {self.bill_id} - ${self.amount}"





