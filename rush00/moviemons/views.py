from django.shortcuts import render
from moviemons.gestion import db

# Create your views here.
def new(request):
	print (request)
	# if request.GET.get('a') == 'a':
	# 	db.load_default_settings()
	# 	db.save("save.pickle")
	# 	return redirect('/worldmap')
	# if request.GET.get('a') == 'b':
	# 	return redirect('/options/load_game')
	# return render(request,  "moviemons/base.html", {});
	return render(request,  "moviemons/title_screen.html")
