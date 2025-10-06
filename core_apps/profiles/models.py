from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedModel

User = get_user_model()

#what is a forward reference?
def get_user_username(instance: "Profile") -> str:
    return instance.user.username

class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")
        
    class Occupation(models.TextChoices):
        MASON = "mason", _("Mason")
        CARPENTER = "carpenter", _("Carpenter")
        PAINTER = "painter", _("Painter")
        PLUMBER = "plumber", _("Plumber")
        ROOFER = "roofer", _("Roofer")
        ELECRICIAN = "electrician", _("Electrician")
        TENANT = "tenant", _("Tenant")
        HVAC_TECHNICIAN = "hvac_technician", _("HVAC Technician")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = CloudinaryField("avatar", blank=True, null=True)
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    bio = models.TextField(verbose_name=_("Bio"),blank=True, null=True)
    occupation = models.CharField(
        verbose_name=_("Occupation"),
        max_length=20,
        choices=Occupation.choices,
        default=Occupation.TENANT
    )
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"),
                                    max_length=30, default="+254786346123")
    country_of_origin = CountryField(verbose_name=_("Country of Origin"),
                                     default="KE")
    city_of_origin = models.CharField(
        verbose_name=_("City"), max_length=180, default="Nairobi"
    )
    report_count = models.PositiveIntegerField(
        verbose_name=_("Report Count"), default=0
    )
    reputation = models.IntegerField(verbose_name=_("Reputation"), default=100)
    slug = AutoSlugField(
        populate_from=get_user_username, unique=True
    )
    
    @property
    def is_banned(self) -> bool:
        return self.report_count >= 5
    
    def update_reputation(self):
        self.reputation = max(0, 100 - self.report_count * 20)

    def save(self, *args, **kwargs):
        self.update_reputation()
        super().save(*args, **kwargs)