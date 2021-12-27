from django.http import HttpResponse
import random
from articles.models import Article
from django.template.loader import render_to_string

def home(request):


    random_id = random.randint(1,3)
    article_obj = Article.objects.get(id=random_id)
    article_queryset = Article.objects.all()

    context = {
        "object_list": article_queryset,
        "name": "Abhishek Anand",
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content
    }


    HTML_STRING = render_to_string("home.html",context=context)

    return HttpResponse(HTML_STRING)