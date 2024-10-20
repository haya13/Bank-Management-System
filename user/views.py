
"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer, AuthTokenSerializer
import logging

logger = logging.getLogger(__name__)



class CreateUserView(generics.CreateAPIView):
    """ Endpoint for creating a new user in our system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user


class DeleteUserView(generics.DestroyAPIView):
    """Allow users to delete their own account"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Override the delete method to handle user deletion"""
        user = self.get_object()

        try:
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return Response({"error": f"An error occurred while trying to delete the user: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
