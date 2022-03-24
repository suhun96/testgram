import json

from django.http import JsonResponse
from django.views import View

from postings.models import Post , Image
from users.utils import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            
            contents      = data['contents']
            img_list     = data['img'].split(',')
            
            post_content = Post.objects.create(contents = contents, user = user)
            
            for image in img_list:
                Image.objects.create(
                    img = image,
                    post = post_content,
                )
            return JsonResponse({'massage':'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'massage':'KEY_ERROR123'}, status =400)