from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(CheckQuestion)
admin.site.register(CheckTest)
