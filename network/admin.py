from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Product, Network


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house_number')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_supplier_link', 'get_city', 'level', 'debt', 'created_at')
    list_filter = ('contact__city',)
    actions = ['clear_debt']

    def get_supplier_link(self, obj):
        if obj.supplier:
            url = f'/admin/{obj.supplier._meta.app_label}/{obj.supplier._meta.model_name}/{obj.supplier.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.supplier)
        return '-'
    get_supplier_link.short_description = 'Поставщик'

    def get_city(self, obj):
        return obj.contact.city if obj.contact else '-'
    get_city.short_description = 'Город'

    def clear_debt(self, request, queryset):
        count = queryset.update(debt=0)
        self.message_user(request, f'Задолженность у {count} объектов(а) успешно очищена.')
    clear_debt.short_description = 'Очистить задолженность перед поставщиком'
