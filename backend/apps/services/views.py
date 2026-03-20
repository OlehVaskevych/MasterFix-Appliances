"""
Services Views Module.

This module contains views for displaying and managing services.
Views will be implemented in Phase 2.
"""

from django.views.generic import ListView, DetailView
from .models import ServiceCategory, Service


class ServiceCategoryListView(ListView):
    """
    View for displaying all active service categories.

    Template: services/category_list.html
    Context: 'categories' - queryset of active ServiceCategory objects
    """

    model = ServiceCategory
    template_name = "services/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        """Return only active categories ordered by display_order."""
        return ServiceCategory.objects.filter(is_active=True).prefetch_related(
            "services"
        )


class ServiceListView(ListView):
    """
    View for displaying all active services.

    Template: services/service_list.html
    Context: 'services' - queryset of active Service objects
    """

    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        """Return only active services with their categories."""
        return Service.objects.filter(is_active=True).select_related("category")


class ServiceDetailView(DetailView):
    """
    View for displaying a single service detail.

    Template: services/service_detail.html
    Context: 'service' - the Service object
    """

    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        """Return only active services."""
        return Service.objects.filter(is_active=True).select_related("category")
