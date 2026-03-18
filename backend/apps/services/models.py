"""
Services Models Module.

This module defines database models for managing appliance repair services.
It includes models for service categories (appliance types) and individual
services with pricing information.

Models:
    - ServiceCategory: Groups services by appliance type (e.g., Refrigerator, Washer)
    - Service: Individual repair services with descriptions and pricing
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class ServiceCategory(models.Model):
    """
    Model representing a category of appliances.

    Categories group related services together. For example:
    - Refrigerator Repair
    - Washing Machine Repair
    - Dishwasher Repair
    - Dryer Repair

    Attributes:
        name (str): The display name of the category (max 100 chars)
        slug (str): URL-friendly identifier for the category
        description (str): Detailed description of the category
        icon (str): CSS class or icon name for frontend display
        image (ImageField): Optional image representing the category
        is_active (bool): Whether this category is currently offered
        display_order (int): Order in which categories appear on the website
        created_at (datetime): Timestamp when the category was created
        updated_at (datetime): Timestamp when the category was last modified

    Example:
        >>> category = ServiceCategory.objects.create(
        ...     name="Refrigerator Repair",
        ...     slug="refrigerator-repair",
        ...     description="Professional refrigerator repair services",
        ...     is_active=True,
        ...     display_order=1
        ... )
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Category Name',
        help_text='Display name for this service category (e.g., "Refrigerator Repair")'
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL Slug',
        help_text='URL-friendly version of the name (auto-generated if blank)'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Detailed description of services in this category'
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Icon Class',
        help_text='CSS icon class (e.g., "fa-snowflake" for refrigerator)'
    )

    image = models.ImageField(
        upload_to='services/categories/',
        blank=True,
        null=True,
        verbose_name='Category Image',
        help_text='Representative image for this category (recommended: 400x300px)'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
        help_text='Inactive categories will not be displayed on the website'
    )

    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Order in which this category appears (lower numbers first)'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
        help_text='Timestamp when this category was created'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
        help_text='Timestamp when this category was last modified'
    )

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['display_order', 'name']

        # Database indexes for common queries
        indexes = [
            models.Index(fields=['is_active', 'display_order']),
            models.Index(fields=['slug']),
        ]

    def __str__(self) -> str:
        """Return string representation of the category."""
        return self.name

    def get_active_services(self):
        """
        Return all active services in this category.

        Returns:
            QuerySet: Active Service objects belonging to this category
        """
        return self.services.filter(is_active=True)

    @property
    def services_count(self) -> int:
        """
        Return the count of active services in this category.

        Returns:
            int: Number of active services
        """
        return self.services.filter(is_active=True).count()


class Service(models.Model):
    """
    Model representing an individual repair service.

    Each service belongs to a category and has its own pricing,
    description, and estimated duration.

    Attributes:
        category (FK): The category this service belongs to
        name (str): The display name of the service
        slug (str): URL-friendly identifier
        short_description (str): Brief description for listings (max 200 chars)
        full_description (str): Detailed description with service details
        price_from (Decimal): Starting price for this service
        price_to (Decimal): Maximum price for this service (optional)
        price_type (str): How pricing is displayed (fixed, starting_from, range)
        estimated_duration_minutes (int): Estimated time to complete
        is_featured (bool): Whether to highlight this service
        is_active (bool): Whether this service is currently offered
        display_order (int): Order within the category
        created_at (datetime): Timestamp when created
        updated_at (datetime): Timestamp when last modified

    Example:
        >>> service = Service.objects.create(
        ...     category=refrigerator_category,
        ...     name="Compressor Replacement",
        ...     price_from=Decimal("250.00"),
        ...     price_type="starting_from",
        ...     estimated_duration_minutes=120
        ... )
    """

    # Pricing display type choices
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),  # Exact price: "$150"
        ('starting_from', 'Starting From'),  # Minimum price: "From $150"
        ('range', 'Price Range'),  # Range: "$150 - $300"
        ('call', 'Call for Quote'),  # No price shown: "Call for quote"
    ]

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Category',
        help_text='The category this service belongs to'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Service Name',
        help_text='Display name for this service (e.g., "Compressor Replacement")'
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name='URL Slug',
        help_text='URL-friendly version of the name'
    )

    short_description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Short Description',
        help_text='Brief description for service listings (max 200 characters)'
    )

    full_description = models.TextField(
        blank=True,
        verbose_name='Full Description',
        help_text='Detailed description including what the service covers'
    )

    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Price From',
        help_text='Starting or minimum price for this service (in USD)'
    )

    price_to = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Price To',
        help_text='Maximum price (only used if price_type is "range")'
    )

    price_type = models.CharField(
        max_length=20,
        choices=PRICE_TYPE_CHOICES,
        default='starting_from',
        verbose_name='Price Display Type',
        help_text='How the price should be displayed on the website'
    )

    estimated_duration_minutes = models.PositiveIntegerField(
        default=60,
        validators=[
            MinValueValidator(15),  # Minimum 15 minutes
            MaxValueValidator(480),  # Maximum 8 hours
        ],
        verbose_name='Estimated Duration (minutes)',
        help_text='Estimated time to complete service (15-480 minutes)'
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name='Is Featured',
        help_text='Featured services are highlighted on the homepage'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
        help_text='Inactive services will not be displayed on the website'
    )

    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Order within the category (lower numbers first)'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['category', 'display_order', 'name']

        # Ensure unique slug within each category
        unique_together = [['category', 'slug']]

        # Database indexes for common queries
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self) -> str:
        """Return string representation of the service."""
        return f"{self.category.name} - {self.name}"

    def get_price_display(self) -> str:
        """
        Return formatted price string based on price_type.

        Returns:
            str: Formatted price string for display

        Examples:
            - Fixed: "$150.00"
            - Starting from: "From $150.00"
            - Range: "$150.00 - $300.00"
            - Call: "Call for quote"
        """
        if self.price_type == 'fixed':
            return f"${self.price_from:.2f}"
        elif self.price_type == 'starting_from':
            return f"From ${self.price_from:.2f}"
        elif self.price_type == 'range' and self.price_to:
            return f"${self.price_from:.2f} - ${self.price_to:.2f}"
        elif self.price_type == 'call':
            return "Call for quote"
        else:
            return f"From ${self.price_from:.2f}"

    @property
    def duration_display(self) -> str:
        """
        Return human-readable duration string.

        Returns:
            str: Formatted duration (e.g., "1h 30min" or "45min")
        """
        hours = self.estimated_duration_minutes // 60
        minutes = self.estimated_duration_minutes % 60

        if hours and minutes:
            return f"{hours}h {minutes}min"
        elif hours:
            return f"{hours}h"
        else:
            return f"{minutes}min"
