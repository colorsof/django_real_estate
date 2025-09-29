# Django Common Models - Anki Cards

## Card 1: TimeStampedModel Purpose
**Front:** What is the purpose of creating a TimeStampedModel as an abstract base class?
**Back:** 
- Provides common fields that all other models in the project will inherit
- Contains `pkid`, `id` (UUID), `created_at`, and `updated_at` fields
- Abstract model (not created in database) - serves as base class only
- Ensures consistent timestamping and UUID identification across all models

## Card 2: Abstract Model Meta Option
**Front:** What does `abstract = True` in a model's Meta class do?
**Back:** 
- The model is NOT created as a table in the database
- It serves only as a base class for other models to inherit from
- Child models that inherit from it will have the abstract model's fields
- Used for sharing common functionality without creating unnecessary tables

## Card 3: TimeStampedModel Fields
**Front:** What are the four fields in TimeStampedModel and their purposes?
**Back:** 
- `pkid`: BigAutoField primary key (sequential integer)
- `id`: UUIDField for unique identification (editable=False, unique=True)
- `created_at`: DateTimeField with auto_now_add=True (set on creation)
- `updated_at`: DateTimeField with auto_now=True (updated on every save)

## Card 4: Model Ordering
**Front:** What does `ordering = ['-created_at', '-updated_at']` accomplish?
**Back:** 
- Orders query results in descending order by creation date first
- If creation dates are the same, uses update date as secondary sort
- The minus sign (-) indicates descending order (newest first)
- Most recent objects are returned first by default

## Card 5: Generic Foreign Key Components
**Front:** What are the three components needed for a Generic Foreign Key in Django?
**Back:** 
1. `content_type`: ForeignKey to ContentType (what model type)
2. `object_id`: PositiveIntegerField (which instance ID)  
3. `content_object`: GenericForeignKey('content_type', 'object_id') (the actual object)

## Card 6: ContentView Model Purpose
**Front:** What is the ContentView model designed to track?
**Back:** 
- Tracks views of ANY model instance in the application
- Records who viewed what content (user can be anonymous)
- Captures viewer's IP address for analytics
- Timestamps when the view occurred
- Uses generic foreign key to reference any model type

## Card 7: ContentView Unique Constraint
**Front:** What fields make up the unique_together constraint in ContentView?
**Back:** 
```python
unique_together = ('content_type', 'object_id', 'user', 'viewer_ip')
```
- Prevents duplicate view records for same user/IP viewing same object
- Ensures one view record per unique combination
- Allows tracking without creating spam records

## Card 8: Class Methods vs Instance Methods
**Front:** What is the difference between a class method (@classmethod) and instance method in Django models?
**Back:** 
- **Class method**: Called on the class itself (e.g., `ContentView.record_view()`)
- **Instance method**: Called on model instances (e.g., `view.save()`)
- Class methods receive `cls` as first parameter (the class)
- Instance methods receive `self` as first parameter (the instance)
- Class methods are for operations relevant to the class as a whole

## Card 9: ContentView.record_view() Method
**Front:** What does the `record_view()` class method do?
**Back:** 
```python
ContentView.record_view(content_object, user, viewer_ip)
```
- Gets ContentType for the object being viewed
- Uses get_or_create() to find existing view or create new one
- Handles IntegrityError if duplicate creation attempt occurs
- Returns None - used for side effects (recording the view)

## Card 10: GenericIPAddressField
**Front:** What does `models.GenericIPAddressField()` handle?
**Back:** 
- Stores both IPv4 and IPv6 addresses automatically
- Validates IP address format on save
- Useful for tracking user locations/analytics
- Can be null/blank for anonymous users
- Better than CharField for IP storage

## Card 11: Django Admin Registration
**Front:** How do you register a model with custom admin options in Django?
**Back:** 
```python
@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')
```
- Use `@admin.register(Model)` decorator
- Create admin class inheriting from `admin.ModelAdmin`
- Customize with `list_display`, `readonly_fields`, etc.

## Card 12: GenericTabularInline
**Front:** What is GenericTabularInline used for in Django admin?
**Back:** 
- Allows editing related objects that use Generic Foreign Keys
- Shows as inline forms in the admin interface
- `extra = 0` means no empty forms shown by default
- `readonly_fields` prevents editing of specified fields
- Useful for viewing ContentView records inline with other models

## Card 13: ContentType Framework
**Front:** What is Django's ContentType framework used for?
**Back:** 
- Keeps track of all models installed in your Django project
- Each model gets a ContentType instance automatically
- Used with Generic Foreign Keys to reference any model
- `ContentType.objects.get_for_model(obj)` gets ContentType for any object
- Enables building flexible, reusable apps

## Card 14: get_or_create() Method
**Front:** What does Django's `get_or_create()` method return?
**Back:** 
```python
view, created = Model.objects.get_or_create(
    field1=value1,
    defaults={'field2': value2}
)
```
- Returns a tuple: (object, created_boolean)
- `object`: The retrieved or created instance
- `created`: True if new object was created, False if existing found
- Uses `defaults` for fields only when creating new objects
- Prevents duplicate creation with race conditions
