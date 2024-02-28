from django.contrib import admin
from .models import User, Event, Submission, Comment, EventRegistration
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display =['user', 'body']
    # Let you to search 
    search_fields = ['user']
    # There will be a filter on release year 
    list_filter = ['event']

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_participants']

    def count_participants(self, obj):
        return obj.participants.count()
    count_participants.short_description = 'Participants Count'

    # def count_participants(self, obj):
    #     # Assuming Submission has a ForeignKey to Event and User
    #     return Submission.objects.filter(event=obj).distinct('user').count()
    # count_participants.short_description = 'Participants Count'

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'teamleader' , 'memeber_1' , 'memeber_2' , 'memeber_3' , 'memeber_4', 'memeber_5','phone_number', 'payment']
    # Assuming other configurations remain the same
    readonly_fields = ['image_preview',]
    # If you have other fields to display in detail view, include them as well

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="auto" />', obj.image.url)
        return "No Image Uploaded"
    image_preview.short_description = 'Image Preview'

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:  # editing an existing object
    #         return self.readonly_fields + ['payment',]
    #     return self.readonly_fields




admin.site.site_header = "INNIXO Admin"
admin.site.site_title = "INNIXO Admin Portal"
admin.site.index_title = "Welcome to INNIXO Admin Portal"

admin.site.register(User)
admin.site.register(Event,EventAdmin)
admin.site.register(Submission)
admin.site.register(Comment,CommentAdmin)
admin.site.register(EventRegistration,EventRegistrationAdmin)