from django.contrib import admin


from .models import ServUser, Category, DesignRequest

admin.site.register(ServUser)

admin.site.register(Category)

admin.site.register(DesignRequest)
