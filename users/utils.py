import json, jwt

from django.http import JsonResponse

from testgram.settings import SECRET_KEY, ALGORITHM
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs) :
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode (access_token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id = payload['user'])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'massage' : 'INVALID_TOKEN'} , status = 400 )
        
        except User.DoesNotExist:
            return JsonResponse({'massage' : 'INVALID_USER'} , status = 400 )
        
        return func(self, request, *args , **kwargs)
    
    return wrapper
