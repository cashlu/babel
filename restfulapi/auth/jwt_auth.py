from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class TokenAuth:
    def authenticate(self, request):
        token = {"token": request.META.get("HTTP_AUTHORIZATION")}
        valid_data = VerifyJSONWebTokenSerializer().validate(token)
        # print(valid_data)
        user = valid_data['user']
        print(user.username)
        if user:
            return
        else:
            raise AuthenticationFailed
