from django.contrib import admin
from . models import Sentence, UserProfile

admin.site.register(Sentence)
admin.site.register(UserProfile)



from django.contrib import admin
# from . models import SentenceTest, UserProfileTest


class UserProfileAdmin(admin.ModelAdmin):
    pass
# admin.site.register(Sentence)
# admin.site.register(UserProfile,UserProfileAdmin)
