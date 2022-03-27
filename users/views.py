from email import message
import json , re , bcrypt , jwt

from django.http import JsonResponse
from django.views import View

from django.conf import settings

from users.utils import login_decorator

from .models import Follow, User

class SignUpView(View):
    def post(self, request):
        try: 
            data = json.loads(request.body)
            name            = data['name']
            email           = data['email']
            password        = data['password']
            phone           = data['phone']
            date_of_birth   = data['date_of_birth']
            
            PASSWORD_CHECK  = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            EMAIL_CHECK     = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
            if User.objects.filter(email = email).exists():
                return JsonResponse({"massage":"REGISTERED."}, status=401)
            
            if not re.match(EMAIL_CHECK, email): 
                return JsonResponse({"massage":"INVALID_EMAIL."}, status=401)
            
            if not re.match(PASSWORD_CHECK, password):
                return JsonResponse({"massage":"INVALID_PASSWORD."}, status=401) 
            
            hashed_password      = bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                        name            =  name,
                        email           =  email,
                        password        =  hashed_password,
                        phone           =  phone,
                        date_of_birth   =  date_of_birth
                    )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR123123'}, status=401)


class SignInView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            email          = data["email"]
            input_password = data["password"]
            user           = User.objects.get(email= email)
            
            checkpw_input_db = bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8') )

            if not user:
                return JsonResponse( {'meassage' : 'INVALID EMAIL.'}, status = 401)        
            if not checkpw_input_db:
                return JsonResponse( {'message' : 'INVALID PASSWORD.' } , status = 401)
            new_token        = jwt.encode( {"user": user.id } , settings.SECRET_KEY , algorithm= settings.ALGORITHM)
            return JsonResponse({"token": new_token }, status = 200)
 
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)
        
        
class FollowView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user_id = request.user
        following_id = data['following']
        try:
            if not Follow.objects.filter(follow = user_id , following = following_id).exists():
                if user_id != following_id:
                    return JsonResponse({'message' : 'self nono!'} , status = 400)
                Follow.objects.create(
                follow      = user_id,
                following   = User.objects.get(id = following_id))
                
                return JsonResponse({'message' : 'create!'} , status = 200)

            follow_off = Follow.objects.get(follow = user_id , following = following_id)
            follow_off.delete()     
            return JsonResponse({'message' : 'delete!'} , status = 200)
        except KeyError:
            return JsonResponse({'message' : 'key error'} , status = 400)
    
    @login_decorator    
    def get(self, requset):
        user = requset.user
        following_list = [{
            'name' : follower.following.name
        }for follower in Follow.objects.filter(follow = user )]
        
        return JsonResponse({'follower_list': following_list} , status =200)
        
