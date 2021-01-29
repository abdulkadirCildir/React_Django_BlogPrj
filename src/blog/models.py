from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    # categories = (
    #     ("WORLD", 'World'),
    #     ('NEWS', 'News'),
    #     ('ART', 'Art'),
    #     ('CULTURE', 'Culture'),
    #     ('WRITING', 'Writing'),
    #     ('TECHNOLOGY', 'Technology'),
    #     ('MUSIC','Music'),
    #     ('FASHION', 'Fashion'),
    #     ('CAR', 'Car'),
    #     ('FOOD', 'Food'),
    #     ('BEAUTY', 'Beauty'),
    #     ('DESIGN', 'Design'),
    #     ('TRAVEL', 'Travel'),
    #     ('HEALTH', 'Health'),
    #     ('MOVIE', 'Movie'),
    #     ('HEALTH', 'Health'),
    #     ('HISTORY', 'History')
    # )

    name = models.CharField(max_length=100, verbose_name="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Post(models.Model):

    OPTIONS = (
        ('d', 'Draft'),
        ('p', 'Published')
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.URLField(default='django.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=OPTIONS, default='d')
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def comment_count(self):
        return self.comment_set.all().count()

    @property
    def like_count(self):
        return self.like_set.all().count()

    @property
    def postview_count(self):
        return self.postview_set.all().count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username