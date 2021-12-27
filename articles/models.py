import random
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from .utils import sulgify_instance_title

User = settings.AUTH_USER_MODEL
# Create your models here.
class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups) 

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class  Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False,auto_now=False,null=True,blank=True)

    objects=ArticleManager()
	
    def get_absolute_url(self):
        #return f'/articles/{self.slug}/'
        return reverse("article_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        
        #if self.slug is None:
        #    self.slug = slugify(self.title)
        super().save(*args,**kwargs)

# THIS IS NOW IMPORTED FROM utils.py
#def sulgify_instance_title(instance, save=False, new_slug=None):
#   if new_slug is not None:
#        slug = new_slug
#    else:
#        slug = slugify(instance.title)
#    qs = Article.objects.filter(slug=slug).exclude(id=instance.id)
#    if qs.exists():
#        rand_int = random.randint(300_000, 500_000)
#       slug = f"{slug}-{rand_int}"
#       return sulgify_instance_title(instance, save=save, new_slug=slug )
#    instance.slug = slug
#
#    if save:
#       instance.save()
#    return instance

def article_pre_save(sender, instance, *args, **kwargs):
    #print('Pre_Save')
    if instance.slug is None:
        sulgify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    #print('post_save')
    if created:
        sulgify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)