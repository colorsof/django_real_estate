# Django Profile Model & Cloudinary Integration - Anki Cards

## Cloudinary Configuration Cards

**Card 1**
**Q:** What are the three essential environment variables needed to configure Cloudinary in Django?
**A:** 
- `CLOUDINARY_CLOUD_NAME` - Your Cloudinary account's cloud name
- `CLOUDINARY_API_KEY` - API key from Cloudinary dashboard  
- `CLOUDINARY_API_SECRET` - API secret from Cloudinary dashboard

**Card 2**
**Q:** Where should Cloudinary credentials be stored in local development vs production?
**A:** 
- **Local development**: Store in `.env.local` file
- **Documentation**: Add variable names (without values) to `.env.example` file
- **Production**: Set as environment variables on hosting platform

**Card 3**
**Q:** How do you configure Cloudinary in Django's `base.py` settings file?
**A:**
```python
import cloudinary
from os import getenv

# Get credentials from environment variables
CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY") 
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)
```

**Card 4**
**Q:** Why use Cloudinary instead of serving media files with nginx?
**A:** 
- **Managed service**: Handles media management automatically
- **Cloud-based**: No server storage concerns
- **Feature-rich**: Built-in image transformations, optimization
- **Free tier available**: Cost-effective for small projects
- **Scalable**: Handles traffic spikes without configuration

## Profile Model Design Cards

**Card 5**
**Q:** Why create a separate Profile model instead of adding fields directly to the User model?
**A:** 
**Separation of Concerns principle:**
- **User model**: Handles authentication-related fields only
- **Profile model**: Contains additional user information not directly related to authentication
- **Better organization**: Keeps code modular and maintainable
- **Flexibility**: Can extend profile without touching core authentication

**Card 6**
**Q:** What is a forward reference in Django models and when is it needed?
**A:** 
A forward reference uses quotes around a class name when referencing a class that hasn't been defined yet:
```python
def get_user_username(instance: "Profile") -> str:
    return instance.user.username
```
- Used when the `Profile` class is referenced before it's fully defined
- Python requirement for type hints with undefined classes
- Prevents NameError during import

**Card 7**
**Q:** What does `models.OneToOneField` create and what do its parameters mean?
**A:**
```python
user = models.OneToOneField(
    User, on_delete=models.CASCADE, related_name="profile"
)
```
- **Relationship**: Each Profile links to exactly one User (1:1)
- **on_delete=CASCADE**: Delete profile when user is deleted
- **related_name="profile"**: Access profile from user with `user.profile`

**Card 8**
**Q:** How do Django's `TextChoices` work and what are their advantages?
**A:**
```python
class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female") 
    OTHER = "other", _("Other")
```
- **First value**: Stored in database ("male")
- **Second value**: Human-readable label ("Male")
- **Advantages**: Type safety, IDE autocomplete, cleaner than tuple choices
- **Internationalization**: `_()` makes labels translatable

## Profile Model Fields Cards

**Card 9**
**Q:** What is the purpose and configuration of the `CloudinaryField` in the Profile model?
**A:**
```python
avatar = CloudinaryField("avatar", blank=True, null=True)
```
- **Purpose**: Stores user profile images in Cloudinary
- **blank=True**: Field optional in forms (Django admin)
- **null=True**: Database column can be NULL
- **Integration**: Automatically handles image upload to Cloudinary

**Card 10**
**Q:** What occupations are available in the Profile model's Occupation choices?
**A:**
- MASON, CARPENTER, PAINTER, PLUMBER, ROOFER
- ELECTRICIAN, TENANT, HVAC_TECHNICIAN
- **Default**: TENANT (most users are tenants in real estate app)
- **Storage**: Lowercase values in DB, capitalized labels for display

**Card 11**
**Q:** How does the user reporting and reputation system work in the Profile model?
**A:**
- **report_count**: Tracks how many times user was reported (default: 0)
- **reputation**: User's reputation score (default: 100)
- **is_banned**: Property returns True if report_count >= 5
- **update_reputation()**: reputation = max(0, 100 - report_count * 20)
- **Each report**: Deducts 20 reputation points

## Model Methods and Properties Cards

**Card 12**
**Q:** What does the `@property` decorator do in the `is_banned` method?
**A:**
```python
@property
def is_banned(self) -> bool:
    return self.report_count >= 5
```
- **Makes method accessible like an attribute**: `user.profile.is_banned`
- **No parentheses needed**: Called as property, not method
- **Business logic**: User banned after 5+ reports
- **Return type**: Boolean value

**Card 13**
**Q:** Why is the `save()` method overridden in the Profile model?
**A:**
```python
def save(self, *args, **kwargs):
    self.update_reputation()
    super().save(*args, **kwargs)
```
- **Automatic reputation updates**: Recalculates reputation on every save
- **Data consistency**: Ensures reputation always reflects current report count
- **Hook pattern**: Runs custom logic before standard save behavior
- **Calls parent**: `super().save()` performs actual database save

**Card 14**
**Q:** What is the purpose of the `AutoSlugField` in the Profile model?
**A:**
```python
slug = AutoSlugField(
    populate_from=get_user_username, unique=True
)
```
- **Auto-generation**: Creates URL-friendly slug from username
- **SEO-friendly**: Clean URLs like `/profile/john-doe/`
- **Unique constraint**: No duplicate slugs allowed
- **Function reference**: Uses `get_user_username()` for slug source

## Special Fields and Libraries Cards

**Card 15**
**Q:** What does `PhoneNumberField` provide and how is it configured?
**A:**
```python
phone_number = PhoneNumberField(
    verbose_name=_("Phone Number"),
    max_length=30, 
    default="+254786346123"
)
```
- **Validation**: Automatically validates phone number format
- **International format**: Supports country codes
- **Library**: From `phonenumber_field` package
- **Default**: Kenyan number format (+254)

**Card 16**
**Q:** How does `CountryField` work in the Profile model?
**A:**
```python
country_of_origin = CountryField(
    verbose_name=_("Country of Origin"),
    default="KE"
)
```
- **Library**: From `django_countries` package
- **ISO codes**: Stores 2-letter country codes (KE = Kenya)
- **Display**: Automatically shows full country name in forms
- **Validation**: Only accepts valid ISO country codes

**Card 17**
**Q:** What is `gettext_lazy` (imported as `_`) used for in Django models?
**A:**
- **Internationalization (i18n)**: Marks strings for translation
- **Lazy evaluation**: Translation happens when string is actually used
- **Usage**: `verbose_name=_("Gender")` marks "Gender" as translatable
- **Best practice**: Always use for user-facing strings in models

## Architecture and Best Practices Cards

**Card 18**
**Q:** What is the inheritance hierarchy of the Profile model?
**A:**
```python
class Profile(TimeStampedUUIDModel):
```
- **Inherits from**: `TimeStampedUUIDModel` (custom abstract model)
- **Provides**: UUID primary key, created_at, updated_at fields
- **Location**: `core_apps.common.models`
- **Pattern**: Abstract base model for consistent timestamps and UUIDs

**Card 19**
**Q:** Why use `get_user_model()` instead of importing User directly?
**A:**
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```
- **Flexibility**: Works with custom User models
- **Django best practice**: Recommended in official documentation
- **Configuration**: Respects `AUTH_USER_MODEL` setting
- **Reusability**: Makes app work with any User model implementation

**Card 20**
**Q:** What are the key principles demonstrated in the Profile model design?
**A:**
- **Separation of concerns**: Profile separate from authentication
- **Single responsibility**: Each field has clear purpose
- **Data integrity**: Validation, constraints, and business rules
- **User experience**: Sensible defaults and optional fields  
- **Internationalization**: Translatable strings throughout
- **Extensibility**: Easy to add new fields and methods
