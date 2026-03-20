"""
Services application configuration.

This app handles all service-related functionality including:
- Service categories (appliance types)
- Individual services offered
- Pricing information
"""

from django.apps import AppConfig


class ServicesConfig(AppConfig):
    """Configuration for the services application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.services"
    verbose_name = "Services Management"
