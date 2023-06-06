from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
import pandas as pd
import MyApp.machineLearningModel as ml
import random
#from MyApp.getSymptoms import feed_back_choice, get_symptoms
from django.db.models.signals import post_save
from django.core.cache import cache

# Create your models here.


class UserProfileModel(AbstractBaseUser, PermissionsMixin):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    username = models.CharField(_("username"), max_length=50, unique=True, blank=False, null=False)

    #ID1 = models.PositiveSmallIntegerField(auto_created=True, unique=True)

    class Memberships(models.TextChoices):
        PATIENT = 'L1', _('Patient')
        DOCTOR = 'L2', _('Doctor')
        COMPANY = 'L3', _('Company')

    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female')), default="Male")

    # portfolio_site = models.URLField(blank=True)
    phone_number = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=False, unique=True)
    #password = models.CharField(max_length=16)

    access_level = models.CharField(max_length=3, choices=Memberships.choices, default=Memberships.PATIENT)
    # record_history = models.ForeignKey('Results', on_delete=models.CASCADE)

    # hidden, number of times that a user can use the website
    tokens = models.PositiveSmallIntegerField(default=2)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Unique Identifier to be used for One-Step Login

    uid = models.UUIDField(
        default=None,
        blank=True,
        null=True,
        unique=True,
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "User Profiles"
        ordering = ['access_level', 'last_name']

    def full_name(self):
        return str(
            f"{self.first_name}{' ' + self.middle_name if self.middle_name is None else ''} {self.last_name}")

    def __str__(self):
        return str(f"{self.username}.{self.first_name}  {self.last_name} access level: {self.access_level}")


class Results(models.Model):
    '''
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


    def number():
        count = Results.objects.count()
        if count is None:
            return 1
        else:
            return count + 1
    '''

    report_ID = models.AutoField(primary_key=True)
    input = models.TextField(max_length=3000)
    result = models.TextField(max_length=3000)

    created_by = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hilfen = models.TextField(max_length=3000, default="empty")
    # Requires a ForeignKey to entered symptoms

    class Meta:
        verbose_name_plural = "reports"
        ordering = ['report_ID']

    def __str__(self):
        return str(f"report {self.report_ID}")




class Supervisor(models.Model):
    name = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name="+")
    #name = UserProfileModel.full_name
    list_patients = models.ManyToManyField(UserProfileModel)
    #access_level = models.CharField(UserProfileModel.access_level)

    def __str__(self):
        return str(f"{self.name} supervising profile")


class Hold(models.Model):

    text = models.TextField(max_length=300)

    def __str__(self):
        return str(self.text)


def FindDisease3(inp):
    deses = ml.findDesesFromSymptom(inp)
    return deses

### This is CORRECTED input from user, done by dynamic search in views
### Replace This with your Model(s)
#TODO Replace this Model with ML models to do the calculations and saves the results in ReportsModel
class InputModel(models.Model):
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)

    input_user = models.TextField(max_length=500, default=None)
    str_input = str(input_user)

    def FindDisease1(self, i):
        out = ml.findDesesFromSymptom(i)
        return out

    #out1 = models.TextField(auto_created=(FindDisease1(self=self, i=str_input)))

    disease = models.TextField(max_length=3000, default=None, auto_created=FindDisease3(str_input))

    def FindDisease2(self, inp):
        deses = ml.findDesesFromSymptom(inp)
        return self.objects.update_or_create(disease=deses, user=self.user)

    #symptoms = "itching,skin_rash,nodal_skin_eruptions,continuous_sneezing,shivering,chills,joint_pain,stomach_pain,acidity,ulcers_on_tongue,muscle_wasting,vomiting,burning_micturition,spotting_ urination,fatigue,weight_gain,anxiety,cold_hands_and_feets,mood_swings,weight_loss,restlessness,lethargy,patches_in_throat,irregular_sugar_level,cough,high_fever,sunken_eyes,breathlessness,sweating,dehydration,indigestion,headache,yellowish_skin,dark_urine,nausea,loss_of_appetite,pain_behind_the_eyes,back_pain,constipation,abdominal_pain,diarrhoea,mild_fever,yellow_urine,yellowing_of_eyes,acute_liver_failure,fluid_overload,swelling_of_stomach,swelled_lymph_nodes,malaise,blurred_and_distorted_vision,phlegm,throat_irritation,redness_of_eyes,sinus_pressure,runny_nose,congestion,chest_pain,weakness_in_limbs,fast_heart_rate,pain_during_bowel_movements,pain_in_anal_region,bloody_stool,irritation_in_anus,neck_pain,dizziness,cramps,bruising,obesity,swollen_legs,swollen_blood_vessels,puffy_face_and_eyes,enlarged_thyroid,brittle_nails,swollen_extremeties,excessive_hunger,extra_marital_contacts,drying_and_tingling_lips,slurred_speech,knee_pain,hip_joint_pain,muscle_weakness,stiff_neck,swelling_joints,movement_stiffness,spinning_movements,loss_of_balance,unsteadiness,weakness_of_one_body_side,loss_of_smell,bladder_discomfort,foul_smell_of urine,continuous_feel_of_urine,passage_of_gases,internal_itching,toxic_look_(typhos),depression,irritability,muscle_pain,altered_sensorium,red_spots_over_body,belly_pain,abnormal_menstruation,dischromic _patches,watering_from_eyes,increased_appetite,polyuria,family_history,mucoid_sputum,rusty_sputum,lack_of_concentration,visual_disturbances,receiving_blood_transfusion,receiving_unsterile_injections,coma,stomach_bleeding,distention_of_abdomen,history_of_alcohol_consumption,fluid_overload,blood_in_sputum,prominent_veins_on_calf,palpitations,painful_walking,pus_filled_pimples,blackheads,scurring,skin_peeling,silver_like_dusting,small_dents_in_nails,inflammatory_nails,blister,red_sore_around_nose,yellow_crust_ooze,prognosis"
    #list_symptoms = symptoms.split(',')
    #clean1 = get_symptoms(str_input, list_symptoms)



    # your input should be saved for data analysis processes and later on qualifications

    date = models.DateTimeField(default=timezone.now)
    #clean_input = models.TextField(max_length=300)



    # symptoms : dataframe
    """
    l = {}
    c = [1, 0]
    for a in range(132):
        b = random.choices([1, 0], [1, 3])
        l.update({str(a): b})
    sample_clean_data = pd.DataFrame(data=l, index=[1])
    """

    #sample_clean = pd.DataFrame()

    # your ML model goes here
    #sample_output = 'symptoms_list'
    #diseases = ml.findDesesFromSymptom(clean_input)

    '''
    # this function saves the output in Reports Model
    def save(self, *args, **kwargs):
        output = str((self.sample_output, self.symptoms_list, "This is a text"))
        return Results.objects.create(input=output, created_by=self.user)
    '''

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        #output = str((self.disease))
        output2 = str((self.input_user))
        #output3 = str(self.FindDisease1(i=output))
        #output4 = str(self.FindDisease2(inp=output2))
        #output5 = FindDisease3(self.str_input)
        return Results.objects.create(input=output2, created_by=self.user)


