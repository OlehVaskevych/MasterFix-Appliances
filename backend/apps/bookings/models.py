"""
Bookings Models Module.

This module defines database models for managing customer booking requests
submitted through the landing page contact form.

Models:
    - Booking: Customer service request with contact info and problem description
    - BookingNote: Internal notes added by staff to bookings

The booking workflow:
    1. Customer submits form (status: 'new')
    2. Staff contacts customer (status: 'contacted')
    3. Appointment scheduled (status: 'scheduled')
    4. Service completed (status: 'completed')
    5. Or cancelled at any point (status: 'cancelled')
"""

from django.db import models
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField


class Booking(models.Model):
    """
    Model for storing customer booking/service requests.

    This model captures all information submitted through the landing page
    booking form, plus additional fields for tracking the request status
    and scheduling.

    Attributes:
        name (str): Customer's full name (2-100 characters)
        email (str): Customer's email address (optional)
        phone (PhoneNumber): US phone number for contact
        address (str): Service address (optional, for scheduling)
        city (str): City name (optional)
        zip_code (str): US ZIP code (optional)
        service (FK): Related service being requested (optional)
        appliance_type (str): Type of appliance needing repair
        appliance_brand (str): Brand/manufacturer of the appliance
        problem_description (str): Detailed description of the issue
        preferred_date (date): Customer's preferred service date
        preferred_time (str): Preferred time slot
        status (str): Current status of the booking
        priority (str): Priority level for scheduling
        source (str): How the customer found us
        ip_address (str): IP address for spam prevention
        user_agent (str): Browser info for analytics
        notes (str): Internal notes (staff only)
        assigned_to (str): Staff member assigned (future: FK to User)
        scheduled_datetime (datetime): Confirmed appointment time
        completed_at (datetime): When service was completed
        created_at (datetime): When booking was submitted
        updated_at (datetime): Last modification timestamp

    Example:
        >>> booking = Booking.objects.create(
        ...     name="John Smith",
        ...     phone="+12025551234",
        ...     problem_description="Refrigerator not cooling properly",
        ...     appliance_type="refrigerator"
        ... )
    """

    # === Status Choices ===
    # Defines the workflow stages for a booking
    STATUS_CHOICES = [
        ('new', 'New'),                 # Just submitted, not yet reviewed
        ('contacted', 'Contacted'),     # Staff has reached out to customer
        ('scheduled', 'Scheduled'),     # Appointment date/time confirmed
        ('in_progress', 'In Progress'), # Technician is working on it
        ('completed', 'Completed'),     # Service successfully completed
        ('cancelled', 'Cancelled'),     # Cancelled by customer or staff
        ('no_response', 'No Response'), # Customer didn't respond to contact attempts
    ]

    # === Priority Levels ===
    # Used for scheduling and dispatch prioritization
    PRIORITY_CHOICES = [
        ('low', 'Low'),           # Standard request, flexible timing
        ('normal', 'Normal'),     # Default priority
        ('high', 'High'),         # Needs attention soon
        ('urgent', 'Urgent'),     # Emergency - same day if possible
    ]

    # === Preferred Time Slots ===
    # Time windows customer prefers for service
    TIME_SLOT_CHOICES = [
        ('morning', 'Morning (8AM - 12PM)'),
        ('afternoon', 'Afternoon (12PM - 5PM)'),
        ('evening', 'Evening (5PM - 8PM)'),
        ('anytime', 'Anytime'),
    ]

    # === Appliance Type Choices ===
    # Common household appliances we service
    APPLIANCE_TYPE_CHOICES = [
        ('refrigerator', 'Refrigerator'),
        ('washer', 'Washing Machine'),
        ('dryer', 'Dryer'),
        ('dishwasher', 'Dishwasher'),
        ('oven', 'Oven/Range'),
        ('microwave', 'Microwave'),
        ('freezer', 'Freezer'),
        ('garbage_disposal', 'Garbage Disposal'),
        ('ice_maker', 'Ice Maker'),
        ('wine_cooler', 'Wine Cooler'),
        ('other', 'Other'),
    ]

    # === Lead Source Options ===
    # Tracks marketing effectiveness
    SOURCE_CHOICES = [
        ('google', 'Google Search'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('yelp', 'Yelp'),
        ('referral', 'Friend/Family Referral'),
        ('repeat', 'Repeat Customer'),
        ('flyer', 'Flyer/Print Ad'),
        ('other', 'Other'),
    ]

    # ==========================================
    # Customer Contact Information
    # ==========================================

    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        verbose_name='Customer Name',
        help_text='Full name of the customer (2-100 characters)'
    )

    email = models.EmailField(
        blank=True,
        verbose_name='Email Address',
        help_text='Optional email for confirmation and follow-up'
    )

    phone = PhoneNumberField(
        region='US',
        verbose_name='Phone Number',
        help_text='US phone number (primary contact method)'
    )

    # ==========================================
    # Service Location
    # ==========================================

    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Street Address',
        help_text='Service location street address'
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='City',
        help_text='City name'
    )

    zip_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='ZIP Code',
        help_text='US ZIP code (5 or 9 digit format)'
    )

    # ==========================================
    # Service Information
    # ==========================================

    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
        verbose_name='Requested Service',
        help_text='Specific service requested (if known)'
    )

    appliance_type = models.CharField(
        max_length=50,
        choices=APPLIANCE_TYPE_CHOICES,
        default='other',
        verbose_name='Appliance Type',
        help_text='Type of appliance needing repair'
    )

    appliance_brand = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Appliance Brand',
        help_text='Brand/manufacturer (e.g., Samsung, LG, Whirlpool)'
    )

    appliance_model = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Model Number',
        help_text='Appliance model number (if available)'
    )

    problem_description = models.TextField(
        validators=[MinLengthValidator(10)],
        verbose_name='Problem Description',
        help_text='Detailed description of the issue (minimum 10 characters)'
    )

    # ==========================================
    # Scheduling Preferences
    # ==========================================

    preferred_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Preferred Date',
        help_text='Customer\'s preferred service date'
    )

    preferred_time = models.CharField(
        max_length=20,
        choices=TIME_SLOT_CHOICES,
        default='anytime',
        verbose_name='Preferred Time',
        help_text='Preferred time slot for service'
    )

    # ==========================================
    # Status & Priority
    # ==========================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True,
        verbose_name='Status',
        help_text='Current status of this booking request'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name='Priority',
        help_text='Priority level for scheduling'
    )

    # ==========================================
    # Marketing & Analytics
    # ==========================================

    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES,
        blank=True,
        verbose_name='Lead Source',
        help_text='How the customer heard about us'
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='IP Address',
        help_text='Captured for spam prevention'
    )

    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent',
        help_text='Browser/device information'
    )

    # ==========================================
    # Internal Management
    # ==========================================

    notes = models.TextField(
        blank=True,
        verbose_name='Internal Notes',
        help_text='Staff notes (not visible to customer)'
    )

    assigned_to = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Assigned To',
        help_text='Staff member or technician assigned to this booking'
    )

    # ==========================================
    # Scheduling & Completion
    # ==========================================

    scheduled_datetime = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Scheduled Date/Time',
        help_text='Confirmed appointment date and time'
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Completed At',
        help_text='When the service was completed'
    )

    # ==========================================
    # Timestamps
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
        help_text='When this booking was submitted'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
        help_text='Last modification timestamp'
    )

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

        # Database indexes for common queries
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['priority', 'status']),
            models.Index(fields=['phone']),
            models.Index(fields=['scheduled_datetime']),
        ]

        # Permissions for staff access control
        permissions = [
            ('can_assign_booking', 'Can assign bookings to technicians'),
            ('can_export_bookings', 'Can export booking data'),
        ]

    def __str__(self) -> str:
        """Return string representation of the booking."""
        return f"#{self.pk} - {self.name} ({self.get_status_display()})"

    def mark_contacted(self) -> None:
        """
        Mark booking as contacted.

        Updates status to 'contacted' when staff reaches out to customer.
        """
        self.status = 'contacted'
        self.save(update_fields=['status', 'updated_at'])

    def mark_scheduled(self, scheduled_datetime) -> None:
        """
        Mark booking as scheduled with confirmed datetime.

        Args:
            scheduled_datetime: The confirmed appointment datetime
        """
        self.status = 'scheduled'
        self.scheduled_datetime = scheduled_datetime
        self.save(update_fields=['status', 'scheduled_datetime', 'updated_at'])

    def mark_completed(self) -> None:
        """
        Mark booking as completed.

        Updates status and records completion timestamp.
        """
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])

    def mark_cancelled(self, reason: str = '') -> None:
        """
        Mark booking as cancelled.

        Args:
            reason: Optional reason for cancellation (added to notes)
        """
        self.status = 'cancelled'
        if reason:
            self.notes = f"{self.notes}\n\nCancellation reason: {reason}".strip()
        self.save(update_fields=['status', 'notes', 'updated_at'])

    @property
    def is_actionable(self) -> bool:
        """
        Check if booking can still be acted upon.

        Returns:
            bool: True if booking is not completed or cancelled
        """
        return self.status not in ['completed', 'cancelled']

    @property
    def full_address(self) -> str:
        """
        Return formatted full address.

        Returns:
            str: Combined address, city, and ZIP code
        """
        parts = [self.address, self.city, self.zip_code]
        return ', '.join(part for part in parts if part)


class BookingNote(models.Model):
    """
    Model for tracking internal notes and updates on bookings.

    Allows staff to add timestamped notes to bookings for
    tracking communication and service history.

    Attributes:
        booking (FK): The booking this note belongs to
        author (str): Name of staff member who added the note
        content (str): The note content
        is_customer_visible (bool): Whether customer can see this note
        created_at (datetime): When note was added

    Example:
        >>> note = BookingNote.objects.create(
        ...     booking=booking,
        ...     author="John Doe",
        ...     content="Customer prefers morning appointments",
        ...     is_customer_visible=False
        ... )
    """

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booking_notes',
        verbose_name='Booking',
        help_text='The booking this note belongs to'
    )

    author = models.CharField(
        max_length=100,
        verbose_name='Author',
        help_text='Staff member who added this note'
    )

    content = models.TextField(
        verbose_name='Note Content',
        help_text='Content of the note'
    )

    is_customer_visible = models.BooleanField(
        default=False,
        verbose_name='Customer Visible',
        help_text='If true, customer can see this note in their booking history'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    class Meta:
        verbose_name = 'Booking Note'
        verbose_name_plural = 'Booking Notes'
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Return string representation of the note."""
        return f"Note on #{self.booking_id} by {self.author}"
