# This lives in the PUBLIC schema
class Tenant(models.Model):
    """Each hotel is a tenant"""
    schema_name = models.CharField(max_length=63, unique=True)  # e.g., 'hotel_sarit'
    name = models.CharField(max_length=255)  # "Sarit Centre Hotel"
    domain = models.CharField(max_length=255, unique=True)  # 'sarit.yourdomain.com'
    
    # Business info
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField()
    owner_phone = models.CharField(max_length=20)
    
    # Subscription & status
    subscription_tier = models.CharField(choices=[
        ('trial', 'Trial'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ])
    subscription_status = models.CharField(choices=[
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ])
    subscription_start = models.DateField()
    subscription_end = models.DateField(null=True)
    
    # Commission structure
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)  # 15%
    
    # Settings
    timezone = models.CharField(max_length=50, default='Africa/Nairobi')
    currency = models.CharField(max_length=3, default='KES')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tenants'
        
        
# All models below exist in EACH tenant's schema

# ============ PROPERTY & LOCATION ============

class Property(models.Model):
    """
    Main property information. 
    Most hotels = 1 property, but allows for chains with multiple locations
    """
    name = models.CharField(max_length=255)  # "Sarit Centre Hotel - Westlands"
    slug = models.SlugField(unique=True)
    
    # Location
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)  # Kenyan counties
    country = models.CharField(max_length=100, default='Kenya')
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Coordinates (for maps)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    
    # Contact
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Descriptions
    short_description = models.TextField(max_length=500)  # For listings
    full_description = models.TextField()  # Full details
    
    # Amenities (property-wide)
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_bar = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_conference_room = models.BooleanField(default=False)
    has_generator = models.BooleanField(default=True)  # Important in Kenya!
    has_security = models.BooleanField(default=True)
    
    # Policies
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='10:00')
    cancellation_policy = models.TextField()
    
    # Payment options
    accepts_mpesa = models.BooleanField(default=True)
    accepts_cash = models.BooleanField(default=True)
    accepts_card = models.BooleanField(default=False)
    accepts_bank_transfer = models.BooleanField(default=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)  # Show on platform
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Properties'


class PropertyImage(models.Model):
    """Property photos"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/%Y/%m/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)  # Main photo
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# ============ ROOMS & INVENTORY ============

class RoomType(models.Model):
    """
    Template for room categories (not individual rooms)
    e.g., "Standard Single", "Deluxe Double", "Executive Suite"
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='room_types')
    
    name = models.CharField(max_length=100)  # "Standard Single Room"
    slug = models.SlugField()
    description = models.TextField()
    
    # Capacity
    max_adults = models.IntegerField(default=2)
    max_children = models.IntegerField(default=0)
    max_occupancy = models.IntegerField(default=2)  # Total people
    
    # Physical attributes
    size_sqm = models.IntegerField(null=True, blank=True)  # Square meters
    bed_type = models.CharField(max_length=50, choices=[
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed'),
        ('twin', 'Twin Beds'),
    ])
    number_of_beds = models.IntegerField(default=1)
    
    # Room amenities
    has_tv = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    has_fan = models.BooleanField(default=True)
    has_hot_water = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    has_bathtub = models.BooleanField(default=False)
    has_fridge = models.BooleanField(default=False)
    has_kettle = models.BooleanField(default=False)
    has_safe = models.BooleanField(default=False)
    
    # Pricing (base rates)
    base_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['property', 'slug']


class RoomTypeImage(models.Model):
    """Photos for each room type"""
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/%Y/%m/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)


class Room(models.Model):
    """
    Individual room units (actual physical rooms)
    e.g., Room 101, Room 102, Room 201
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    
    room_number = models.CharField(max_length=20)  # "101", "2A", etc.
    floor = models.IntegerField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service'),
    ], default='available')
    
    notes = models.TextField(blank=True)  # Internal notes
    
    class Meta:
        unique_together = ['property', 'room_number']
        ordering = ['floor', 'room_number']


# ============ PRICING RULES ============

class PricingRule(models.Model):
    """
    Dynamic pricing based on seasons, length of stay, etc.
    This is where you make money - allows flexible pricing
    """
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='pricing_rules')
    
    name = models.CharField(max_length=100)  # "High Season Pricing", "Weekend Rate"
    
    # Date range (optional - if not set, applies always)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    
    # Day of week filters (optional)
    apply_monday = models.BooleanField(default=True)
    apply_tuesday = models.BooleanField(default=True)
    apply_wednesday = models.BooleanField(default=True)
    apply_thursday = models.BooleanField(default=True)
    apply_friday = models.BooleanField(default=True)
    apply_saturday = models.BooleanField(default=True)
    apply_sunday = models.BooleanField(default=True)
    
    # Minimum stay requirement
    min_nights = models.IntegerField(default=1)
    
    # Pricing adjustments
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # OR
    percentage_adjustment = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # +20% or -10%
    
    # Priority (higher number = higher priority)
    priority = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-priority', 'valid_from']


# ============ AVAILABILITY ============

class Availability(models.Model):
    """
    Tracks which rooms are available on which dates
    Critical for preventing double bookings
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    
    is_available = models.BooleanField(default=True)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Reasons for unavailability
    blocked_reason = models.CharField(max_length=255, blank=True)  # "Maintenance", "Reserved", etc.
    
    class Meta:
        unique_together = ['room', 'date']
        indexes = [
            models.Index(fields=['date', 'is_available']),
        ]


# ============ GUESTS ============

class Guest(models.Model):
    """Guest profiles - reusable across bookings"""
    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    
    # ID/Passport (required in Kenya)
    id_type = models.CharField(max_length=20, choices=[
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('other', 'Other'),
    ])
    id_number = models.CharField(max_length=50)
    
    # Address (optional)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Preferences
    special_requests = models.TextField(blank=True)
    
    # Marketing
    accepts_marketing = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    total_bookings = models.IntegerField(default=0)
    last_stay = models.DateField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]


# ============ BOOKINGS ============

class Booking(models.Model):
    """The core booking model - this is where money happens"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='bookings')
    
    # Booking reference
    booking_number = models.CharField(max_length=20, unique=True)  # Auto-generated: BK-20250101-001
    
    # Dates
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    nights = models.IntegerField()  # Calculated
    
    # Guest counts
    number_of_adults = models.IntegerField(default=1)
    number_of_children = models.IntegerField(default=0)
    
    # Status workflow
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], default='pending')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Before taxes
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Commission (your platform fee)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)  # 15%
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_payout = models.DecimalField(max_digits=10, decimal_places=2)  # What hotel receives
    
    # Special requests
    special_requests = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)  # Hotel staff notes
    
    # Source tracking
    booking_source = models.CharField(max_length=50, choices=[
        ('direct', 'Direct Booking'),
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Phone Call'),
        ('referral', 'Referral'),
        ('google', 'Google Search'),
        ('social', 'Social Media'),
    ], default='direct')
    referrer_code = models.CharField(max_length=50, blank=True)  # Track who referred
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_out_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Cancellation
    cancellation_reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking_number']),
            models.Index(fields=['check_in_date', 'check_out_date']),
            models.Index(fields=['status']),
        ]


class BookingRoom(models.Model):
    """
    Many-to-many through table
    Links bookings to specific rooms (handles multiple rooms per booking)
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_rooms')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)  # Snapshot at booking time
    
    # Pricing for THIS room (in case of multiple rooms with different prices)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    nights = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['booking', 'room']


# ============ PAYMENTS ============

class Payment(models.Model):
    """Track all payment transactions"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('mpesa', 'M-Pesa'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
    ])
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    # External references
    transaction_id = models.CharField(max_length=100, blank=True)  # M-Pesa code, etc.
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    mpesa_phone = models.CharField(max_length=20, blank=True)
    
    # Metadata
    payment_date = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-payment_date']


# ============ REVIEWS ============

class Review(models.Model):
    """Guest reviews after checkout"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reviews')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    
    # Ratings (1-5 scale)
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    cleanliness_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    staff_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    location_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    value_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Review content
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    
    # Response from hotel
    hotel_response = models.TextField(blank=True)
    hotel_response_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


# ============ USERS & PERMISSIONS ============

class HotelStaff(models.Model):
    """Staff members who can access the system"""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='staff')
    
    role = models.CharField(max_length=50, choices=[
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('staff', 'Staff'),
    ])
    
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ============ ANALYTICS & TRACKING ============

class SearchQuery(models.Model):
    """Track what people are searching for - gold for marketing"""
    city = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    
    # Results
    results_found = models.IntegerField()
    property_clicked = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    booking_made = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Tracking
    session_id = models.CharField(max_length=100)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['city', 'created_at']),
        ]
        
        
        















# Critical indexes to add:
- Availability: (date, is_available) - for search queries
- Booking: (check_in_date, check_out_date, status) - for calendars
- Guest: (email, phone) - for lookups
- SearchQuery: (city, created_at) - for analytics

















# Find available rooms in Nairobi from Jan 1-3, 2025
available_rooms = Room.objects.filter(
    property__city='Nairobi',
    availability__date__range=['2025-01-01', '2025-01-03'],
    availability__is_available=True
).distinct()













# 1. Check availability
# 2. Calculate price (base + pricing rules)
# 3. Create Booking
# 4. Create BookingRoom entries
# 5. Mark Availability as unavailable
# 6. Create Payment record
# 7. Send confirmation












# Your platform commission
total_commission = Booking.objects.filter(
    status='confirmed',
    check_in_date__month=9
).aggregate(Sum('commission_amount'))
