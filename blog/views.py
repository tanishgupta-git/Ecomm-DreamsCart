from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
# Create your views here.



def index(request):
	blogpost = Blogpost.objects.all()
	params = {'blogs':blogpost}
	return render(request,'blog/index.html',params)

def blogpost(request,id):
	post = Blogpost.objects.filter(post_id = id)[0]
	if id <= 1:
		params = {'post':post,'next':id+1}
	elif id == len(Blogpost.objects.all()):
		params = {'post':post,'prev':id-1}
	else:
		params = {'post':post,'prev':id-1,'next':id+1}
	return render(request, 'blog/blogpost.html',params)