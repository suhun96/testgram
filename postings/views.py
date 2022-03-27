import json , re
from venv import create

from django.http import JsonResponse
from django.views import View

from postings.models import Post , Image , Comment , Like 
from users.utils import login_decorator
from users.views import User


class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            
            contents        = data['contents']
            image_list      = data['images'].split(',')
            url_check =  "^.*\.(jpg|jpeg|gif|png|bmp|tiff|tga|svg)$"
            
            for image in image_list:
                if not re.match(url_check, image):
                    return JsonResponse({'message' : 'INVALID_IMAGES!!'}, status = 401)
                
                
            post_content = Post.objects.create(contents = contents, user = user)
            for image in image_list:
                Image.objects.create(images = image, post = post_content)
            return JsonResponse({'massage':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'massage':'KEY_ERROR123'}, status =400)
    
    @login_decorator    
    def get(self, request):
        post_list = [{
            'name' : User.objects.get(id = post.user.id).name,
            'contents' : post.contents,
            'images' :[image.images for image in post.images.all()],
            'create_at' : post.create_at
        } for post in Post.objects.all()]
        
        return JsonResponse({'data':post_list} , status =200) 
    

class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            contents = data['contents']
            post = data['post']
            
            
            Comments = Comment.objects.create(
                user = user,
                contents = contents,
                post = Post.objects.get(id = post)
            )
            
            return JsonResponse({'massage' : Comments.id }, status=200)
        except KeyError:
            return JsonResponse({'massage' : 'you cant'} , status = 400)
    
    @login_decorator
    def get(self, request):
        try:
            comments_list = [{
                'name' : User.objects.get(id = comment.user.id).name,
                'post' : comment.post.id,
                'contents' : comment.contents,
                'create_at' : comment.create_at 
                } for comment in Comment.objects.all()]
            
            
            return JsonResponse({'list' :comments_list} , status =200)
        except KeyError:
            return JsonResponse({'massage' : 'cant'} , status = 400)
        


class LikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user_id = request.user
        post_id = data['post']
        try:
            if not Like.objects.filter(user = user_id ,post = post_id).exists():
                push_like = Like.objects.create(
                    user    = user_id,
                    post    = Post.objects.get(id = post_id),
                    like_or_not = "1"
                )
                
                push_like_list = {
                    "user" : push_like.user.name,
                    "post" : push_like.post.id,
                    "like_or_not" : push_like.like_or_not
                }
                return JsonResponse({'massage': push_like_list } , status = 200)

            pushed_like = Like.objects.get(user = user_id , post =post_id)
            pushed_like.delete()
            return JsonResponse({'message' : 'ok delete'} , status = 200)
    
        except KeyError:
            return JsonResponse({'massage' : 'unlike', 'message' : 'push_unlike'} , status = 400)
        
    def get(self, requset):
        data = json.loads(requset.body)
        post = data['post']
        post_like = [{
            'name'      : like.user.name,
            'create_at' : like.create_at
        }for like in Like.objects.filter(post = post)]
        return JsonResponse({'message' : post_like }, status =200)
    
    
                
                
                
