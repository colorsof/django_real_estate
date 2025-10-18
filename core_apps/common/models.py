import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError


# A timestamped Uuid model.This model is going to be an 
# abstract model that will hold model fields that will be 
# common to all the other applications in the project.

User = get_user_model()

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating 
    'created' and 'modified' fields, along with a UUID primary key.
    """
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
        #The -created_at and -updated_at will ensure the most recent objects are going to be returned first
        
class ContentView(TimeStampedModel):
        """
        A model to track content views by users.
        """
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"))
        object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
        content_object = GenericForeignKey('content_type', 'object_id')
        user = models.ForeignKey(
            User, 
            on_delete=models.SET_NULL, 
            null=True, 
            blank=True, 
            related_name='content_views',
            verbose_name=_("User")
            )
        
        viewer_ip = models.GenericIPAddressField(
            verbose_name=_("Viewer IP Address"),
            null=True,
            blank=True
        )
        
        last_viewed = models.DateTimeField()
        
        class Meta:
            unique_together = ('content_type', 'object_id', 'user', 'viewer_ip')
            verbose_name = _("Content View")
            verbose_name_plural = _("Content Views")

        def __str__(self) -> str:
            return f"{self.content_object} viewed by {self.user.get_full_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"
            
        @classmethod #this is a class method can be called on the class itself without instantiating an object of the class
        def record_view(cls, content_object, user:User, viewer_ip: str) -> None:
            from django.utils import timezone
            content_type = ContentType.objects.get_for_model(content_object)
            try:
                view, created = cls.objects.update_or_create(
                    content_type = content_type,
                    object_id=content_object.pkid,
                    user=user,
                    viewer_ip=viewer_ip,
                    defaults={'last_viewed': timezone.now()},
                )
            except IntegrityError:
                pass