from django.db import models


class Post(models.Model):
    user        = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name='posts')    
    contents    = models.CharField(max_length=2000, null= True)
    create_at   = models.DateTimeField(auto_now=True)
    update_at   = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "posts"
        
class Image(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='images')
    images = models.URLField(max_length=300)
    class Meta:
        db_table = "images"
    
class Comment(models.Model):
    user      = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='user')
    post      = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='post')
    contents  = models.CharField(max_length=300, null=True)
    create_at = models.DateField(auto_now=True)
    
    class Meta:
        db_table = "comments"
        

class Like(models.Model):
    user        = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post        = models.ForeignKey('Post', on_delete=models.CASCADE , related_name="posts")
    like_or_not = models.BooleanField(null=True)
    create_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "likes"

