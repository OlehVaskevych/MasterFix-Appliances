"""
Bookings Admin Configuration.

This module configures the Django admin interface for managing
customer booking requests and related notes.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Booking, BookingNote


class BookingNoteInline(admin.TabularInline):
    """
    Inline admin for BookingNote model.

    Allows staff to add notes directly from the booking detail page.
    """
    model = BookingNote
    extra = 1
    readonly_fields = ['created_at']
    fields = ['author', 'content', 'is_customer_visible', 'created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Booking model.

    Features:
        - Color-coded status display
        - Quick filters for status, priority, and date
        - Search by customer name, phone, email
        - Inline notes
        - Quick actions for status changes
        - Date hierarchy for easy navigation
    """

    list_display = [
        'id',
        'name',
        'phone',
        'appliance_type_display',
        'status',
        'priority',
        'scheduled_datetime',
        'created_at',
    ]

    list_filter = [
        'status',
        'priority',
        'appliance_type',
        'source',
        'created_at',
        'scheduled_datetime',
    ]

    search_fields = [
        'name',
        'phone',
        'email',
        'address',
        'city',
        'problem_description',
    ]

    list_editable = [
        'status',
        'priority',
    ]

    ordering = ['-created_at']

    date_hierarchy = 'created_at'

    readonly_fields = [
        'created_at',
        'updated_at',
        'ip_address',
        'user_agent',
    ]

    autocomplete_fields = ['service']

    inlines = [BookingNoteInline]

    # Organize fields into logical sections
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Service Location', {
            'fields': ('address', 'city', 'zip_code'),
            'classes': ('collapse',)
        }),
        ('Service Request', {
            'fields': (
                'service',
                'appliance_type',
                'appliance_brand',
                'appliance_model',
                'problem_description'
            )
        }),
        ('Scheduling', {
            'fields': (
                'preferred_date',
                'preferred_time',
                'scheduled_datetime',
                'completed_at'
            )
        }),
        ('Status & Assignment', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('Marketing', {
            'fields': ('source',),
            'classes': ('collapse',)
        }),
        ('Internal Notes', {
            'fields': ('notes',)
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Custom admin actions
    actions = [
        'mark_as_contacted',
        'mark_as_scheduled',
        'mark_as_completed',
        'mark_as_cancelled',
        'set_priority_urgent',
    ]

    @admin.display(description='Appliance')
    def appliance_type_display(self, obj):
        """Display appliance type."""
        return obj.get_appliance_type_display()

    @admin.display(description='Status')
    def status_badge(self, obj):
        """Display color-coded status badge."""
        colors = {
            'new': '#3498db',  # Blue
            'contacted': '#9b59b6',  # Purple
            'scheduled': '#f39c12',  # Orange
            'in_progress': '#e67e22',  # Dark Orange
            'completed': '#27ae60',  # Green
            'cancelled': '#e74c3c',  # Red
            'no_response': '#95a5a6',  # Gray
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.display(description='Priority')
    def priority_badge(self, obj):
        """Display color-coded priority badge."""
        colors = {
            'low': '#95a5a6',  # Gray
            'normal': '#3498db',  # Blue
            'high': '#f39c12',  # Orange
            'urgent': '#e74c3c',  # Red
        }
        color = colors.get(obj.priority, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_priority_display()
        )

    @admin.action(description='Mark selected as Contacted')
    def mark_as_contacted(self, request, queryset):
        """Bulk action to mark bookings as contacted."""
        updated = queryset.filter(status='new').update(status='contacted')
        self.message_user(request, f'{updated} booking(s) marked as contacted.')

    @admin.action(description='Mark selected as Scheduled')
    def mark_as_scheduled(self, request, queryset):
        """Bulk action to mark bookings as scheduled."""
        updated = queryset.exclude(
            status__in=['completed', 'cancelled']
        ).update(status='scheduled')
        self.message_user(request, f'{updated} booking(s) marked as scheduled.')

    @admin.action(description='Mark selected as Completed')
    def mark_as_completed(self, request, queryset):
        """Bulk action to mark bookings as completed."""
        updated = queryset.exclude(
            status__in=['completed', 'cancelled']
        ).update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} booking(s) marked as completed.')

    @admin.action(description='Mark selected as Cancelled')
    def mark_as_cancelled(self, request, queryset):
        """Bulk action to cancel bookings."""
        updated = queryset.exclude(
            status__in=['completed', 'cancelled']
        ).update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) cancelled.')

    @admin.action(description='Set priority to Urgent')
    def set_priority_urgent(self, request, queryset):
        """Bulk action to set urgent priority."""
        updated = queryset.update(priority='urgent')
        self.message_user(request, f'{updated} booking(s) set to urgent priority.')


@admin.register(BookingNote)
class BookingNoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for BookingNote model.

    Standalone admin for viewing/managing all notes across bookings.
    """

    list_display = [
        'booking',
        'author',
        'content_preview',
        'is_customer_visible',
        'created_at',
    ]

    list_filter = [
        'is_customer_visible',
        'created_at',
        'author',
    ]

    search_fields = [
        'content',
        'author',
        'booking__name',
    ]

    readonly_fields = ['created_at']

    @admin.display(description='Content')
    def content_preview(self, obj):
        """Display truncated content preview."""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
