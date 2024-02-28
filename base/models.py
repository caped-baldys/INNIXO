from email.policy import default
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
import time
from datetime import datetime
from django.utils.text import slugify
import phonenumbers
from django.conf import settings
# from django_resized import ResizedImageField
# Create your models here.
def participant_event_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/event_name/participant_name/filename
    event_name = slugify(instance.event.name)  # Accessing the related Event instance
    teamleader = slugify(instance.teamleader)  # Assuming 'participant' field exists
    base_filename, file_extension = filename.rsplit('.', 1)
    new_filename = f"{teamleader}.{file_extension}"
    return f'uploads/{event_name}/{new_filename}'


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    hackathon_participant = models.BooleanField(default=True, null=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    twitter = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    facebook = models.URLField(max_length=500, null=True, blank=True)
    github = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['name']

def qr_upload_to(instance, filename):
   
    upload_to = settings.UPLOADS_QR_ROOT
    ext = filename.split('.')[-1]
    # Generate a unique filename using UUID
    filename = slugify(instance.name)
    return f'{upload_to}{filename}'



class Event(models.Model):
    name = models.CharField(max_length=200)
    preview = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='events')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    ordering_filter = models.IntegerField(unique=True)
    max_members = models.IntegerField(null=True) 
    min_members = models.IntegerField(null=True)
    QR_code = models.ImageField(upload_to=qr_upload_to, blank=True, null=True)
    
    #image = ResizedImageField(size=[300,300], default=)
    
    # image = models.ImageField(upload_to='backgrounds/', default='background.jpg')


    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is new
            # Get the current maximum order value
            max_order = Event.objects.aggregate(Max('ordering_filter'))['ordering_filter__max']
            if max_order is not None:
                self.order = max_order + 1
            else:
                self.order = 1  # This is the first object
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering_filter']


    @property
    def event_status(self):
        status = None
        
        present = datetime.now().timestamp()
        deadline = self.registration_deadline.timestamp()
        past_deadline = (present > deadline)

        if past_deadline:
            status = 'Finished'
        else:
            status = 'Ongoing'

        return status


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    teamleader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='TeamLeader')
    ## For adding members to group based event
    team_name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    memeber_1 = models.CharField(max_length=200, blank=True, null=True)
    memeber_2 = models.CharField(max_length=200, blank=True, null=True)
    memeber_3 = models.CharField(max_length=200, blank=True, null=True)
    memeber_4 = models.CharField(max_length=200, blank=True, null=True)
    memeber_5 = models.CharField(max_length=200, blank=True, null=True)

    payment = models.ImageField(upload_to=participant_event_directory_path, blank=True, null=True)


    # def clean(self):
    #     super().clean()
    #     if self.phone_number:
    #         try:
    #             phone_number_obj = phonenumbers.parse(self.phone_number, "IN")
    #             if not phonenumbers.is_valid_number(phone_number_obj):
    #                 raise ValidationError({'phone_number': 'Phone number is not valid'})
                
    #             if phone_number_obj.country_code != 91:
    #                 raise ValidationError({'phone_number': 'Phone number must be an Indian phone number'})
    #         except phonenumbers.NumberParseException:
    #             raise ValidationError({'phone_number': 'Phone number is not valid'})



class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="submissions")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    details = models.TextField(null=True, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.event) + ' --- ' + str(self.participant)

class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comments")
    event =  models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]