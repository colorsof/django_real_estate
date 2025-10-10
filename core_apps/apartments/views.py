from typing import Any

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from core_apps.common.renderers import GenericJSONRenderer
from core_apps.profiles.models import Profile
from .models import Apartment
from .serializers import ApartmentSerializer

#class ApartmentViewSet(viewsets.ModelViewSet): why apiview and not viewset
class ApartmentCreateAPIView(generics.CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = 'Apartment'
    
    def create(self, request:Request, *args, **kwargs:Any):
        user = request.user
        if user.is_superuser or (hasattr(user, "profile") and user.profile.occupation == Profile.Occupation.TENANT):
            return super().create(request, *args, **kwargs)
        else:
            return Response({
                "message": "Only superusers or tenants can create apartments."
            }, status=403)

class ApartmentDetailAPIView(generics.ListAPIView):
    serializer_class = ApartmentSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = 'Apartment'

    def get_queryset(self):
        return self.request.user.apartment.all()
        
        
        