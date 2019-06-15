from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='images_created',
                            on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    about = models.TextField(blank=True,
                             null=True,
                             max_length=500)
    slug = models.SlugField(max_length=200,
                            blank=True,
                            unique=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)

    def __str__(self):
        return self.about[:50] + "..."

    def save(self,*args,**kwargs):
        if not self.slug:
            try:
                self.slug = slugify(str(self.user)) +"-" + slugify(str(self.image))
                super(Image,self).save(*args,**kwargs)
            except:
                self.slug = slugify(str(self.user)) +"-" + slugify(str(self.image)) + slugify(str(self.created))
                super(Image,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('foods_detail',args=[self.id,self.slug])

    def get_edit_url(self):
        return reverse('edit_post',args=[self.id,self.slug])

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='comments_created',
                            on_delete=models.CASCADE)
    image = models.ForeignKey(Image,related_name='comments',
                             on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.comment[:50] + "...."
