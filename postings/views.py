import json
import re

from django.http import JsonResponse
from django.views import View

from postings.models import Post , Image
from users.utils import login_decorator
from users.views import User


class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            
            contents      = data['contents']
            img_list     = data['images'].split(',')
            
            post_content = Post.objects.create(contents = contents, user = user)
            
            for image in img_list:
                Image.objects.create(
                    img = image,
                    post = post_content,
                )
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