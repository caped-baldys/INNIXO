from django.contrib import admin
from .models import User, Event, Submission, Comment
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


admin.site.site_header = "INNIXO Admin"
admin.site.site_title = "INNIXO Admin Portal"
admin.site.index_title = "Welcome to INNIXO Admin Portal"

admin.site.register(User)
admin.site.register(Event,EventAdmin)
admin.site.register(Submission)
admin.site.register(Comment,CommentAdmin)