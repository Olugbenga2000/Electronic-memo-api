from django.contrib import admin
from .models import Department, Memo, Staff, ReadMemo, StarMemo

# Register your models here.
admin.site.register(Department)
admin.site.register(Memo)
admin.site.register(Staff)
admin.site.register(ReadMemo)
admin.site.register(StarMemo)
