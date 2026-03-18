"""
Services Admin Configuration.

This module configures the Django admin interface for managing
service categories and individual services.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for ServiceCategory model.

    Features:
        - List view with key fields and service count
        - Search by name and description
        - Filter by active status
        - Prepopulated slug field
        - Ordering controls
    """

    list_display = [
        'name',
        'slug',
        'services_count_display',
        'is_active',
        'display_order',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'created_at',
    ]

    search_fields = [
        'name',
        'description',
    ]

    prepopulated_fields = {
        'slug': ('name',),
    }

    list_editable = [
        'is_active',
        'display_order',
    ]

    ordering = ['display_order', 'name']

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'image', 'is_active', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Services')
    def services_count_display(self, obj):
        """Display count of active services in this category."""
        count = obj.services_count
        return format_html(
            '<span style="font-weight: bold;">{}</span>',
            count
        )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Service model.

    Features:
        - List view with category, pricing, and status
        - Filter by category, active status, featured
        - Search by name and description
        - Inline category selection
        - Price formatting in list view
    """

    list_display = [
        'name',
        'category',
        'price_display',
        'duration_display_admin',
        'is_featured',
        'is_active',
        'display_order',
    ]

    list_filter = [
        'category',
        'is_active',
        'is_featured',
        'price_type',
        'created_at',
    ]

    search_fields = [
        'name',
        'short_description',
        'full_description',
        'category__name',
    ]

    prepopulated_fields = {
        'slug': ('name',),
    }

    list_editable = [
        'is_active',
        'is_featured',
        'display_order',
    ]

    ordering = ['category', 'display_order', 'name']

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    autocomplete_fields = ['category']

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug')
        }),
        ('Description', {
            'fields': ('short_description', 'full_description')
        }),
        ('Pricing', {
            'fields': ('price_type', 'price_from', 'price_to'),
            'description': 'Set price_to only if price_type is "range"'
        }),
        ('Service Details', {
            'fields': ('estimated_duration_minutes',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Price')
    def price_display(self, obj):
        """Display formatted price."""
        return obj.get_price_display()

    @admin.display(description='Duration')
    def duration_display_admin(self, obj):
        """Display formatted duration."""
        return obj.duration_display
