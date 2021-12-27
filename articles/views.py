from django.shortcuts import render
from django.db.models import Q, lookups, query
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import ArticleForm
# Create your views here.
from .models import Article

#def article_search_view(request):
	#print(dir(request))
	#print(request.GET)
	#query = request.GET.get('q')#this is a dictionary
	#THIS IS ALSO A WAY WHEN query_dict = request.GET is used
	#query = query_dict.get("q")
	#try:
	#	query = query_dict.get("q")
	#except:
	#	query = None
    #qs = Article.objects.search(query=query)
    #context = {
     #   "object_list": qs
    #}
    #return render(request, "articles/search.html", context=context)	

def article_search_view(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query=query)
    context = {
        "object_list": qs
    }
    return render(request, "articles/search.html", context=context)    

@login_required
def article_create_view(request):
	#print(request.POST)
	form = ArticleForm(request.POST or None)
	context = {
		"form": form
	}
	if form.is_valid():
		#THIS PART IS FOR THE ArticleForm CLASS IN forms.py
		article_object = form.save() # THIS WORK ONLY ON ModelForm
		context['form'] = ArticleForm()
		# THIS PART IS FOR THE CLASS ArticleFormOld in forms.py
		#title = form.cleaned_data.get("title")
		#content = form.cleaned_data.get("title")
		#print(title, content)
		#article_object = Article.objects.create(title=title, content=content)
		#context['object'] = article_object
		#context['created'] = True
	return render(request,"articles/create.html", context=context)

#old method
#def article_create_view(request):
#	#print(request.POST)
#	form = ArticleForm()
#	context = {
#		"form": form
#	}
#	if request.method == "POST":
#		form = ArticleForm(request.POST)
#		context['form']=form
#		if form.is_valid():
#			title = form.cleaned_data.get("title")
#			content = form.cleaned_data.get("title")
#			#print(title, content)
#			article_object = Article.objects.create(title=title, content=content)
#			context['object'] = article_object
#			context['created'] = True
#	return render(request,"articles/create.html", context=context)
	    

def article_detail_view(request, slug=None):
	article_obj = None
	if slug is not None:
		try:
			article_obj = Article.objects.get(slug=slug)
		except:
			raise Http404
		
	context ={
		"object": article_obj,
	}
	return render(request,"articles/details.html",context=context)