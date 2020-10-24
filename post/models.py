from django.db import models
from user.models import User

# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'post'
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    pubdate = models.DateTimeField(null=False)
    # author
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # content

    def __repr__(self):
        return "<Post {} {} {} {} [{}]>".format(self.id, self.title, self.author, self.content, self.author_id )

    __str__ = __repr__

class Content(models.Model):
    class Meta:
        db_table = 'content'
    # id 可以不写，主键django帮你创建一个 pk
    post = models.OneToOneField(Post, to_field='id',on_delete=models.CASCADE) # post_id
    content = models.TextField(null=False) # content

    def __repr__(self):
        return "<Content {} {}>".format(self.post.id, self.content[:20])

    __str__ = __repr__
