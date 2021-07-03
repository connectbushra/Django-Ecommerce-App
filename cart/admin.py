from django.contrib import admin
from .models import items,OrderItem,Order,Address,Payment,Category,Review,Color,Brand,Person
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ['title' ,'img','price','color']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code']

class PersonAdmin(admin.ModelAdmin):
    list_display = ['type']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['comment','rate','user','item', 'create_at']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['address','full_name','country','zip']


admin.site.register(Review,ReviewAdmin)
admin.site.register(items,ItemsAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Address,AddressAdmin)

