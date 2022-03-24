import json , re

from django.http import JsonResponse
from django.views import View

from postings.models import Post , Image , Comment
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
        
        