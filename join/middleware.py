from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

class IgnoreInvalidTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Checks if the token is invalid and sets the user to None.

        This allows views with `AllowAny` permission to work even if the token is
        wrong or expired. By setting the user to None, the view can check its permissions
        without causing a `401 Unauthorized` error.
        """
        auth = TokenAuthentication()
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            try:
                # Try to authenticate the user with the token
                auth.authenticate(request)
            except AuthenticationFailed as e:
                # If the token is invalid, set user to None
                print(f"Invalid token detected, setting user to None: {e}")  # Debug message
                request.user = None  # Set user to None if token is invalid
            except Exception as e:
                print(f"Unexpected error during authentication: {e}")  # Debug message for other errors
        else:
            print("No token provided")  # Debug message if no token is found