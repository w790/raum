from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'stock')
    list_filter = ('is_active', 'category', 'shape', 'frame_material')
    search_fields = ('name', 'description', 'collection')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('General Info', {
            'fields': ('category', 'name', 'slug', 'description', 'price', 'stock', 'is_active')
        }),
        ('Specifications', {
            'fields': ('collection', 'frame_material', 'lens_type', 'shape', 'uv_protection', 'country_of_origin')
        }),
        ('Dimensions (mm)', {
            'fields': ('lens_width', 'bridge_width', 'frame_front_width', 'temple_length', 'lens_height')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')
