from django.contrib import admin
from .models import RequestConsultation, Articles, Receipts


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')


class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date')
    list_filter = ('date',)
    search_fields = ('name',)


admin.site.register(RequestConsultation, RequestAdmin)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Receipts)
