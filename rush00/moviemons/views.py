from django.shortcuts import render, HttpResponse, redirect
from moviemons.gestion import session

# Create your views here.
def new(request):
	print (request)
	if request.GET.get('a') == 'a':
		session.load_default_settings()
		session.save()
		return redirect('/worldmap')
	if request.GET.get('a') == 'b':
		# return redirect('/options/load_game')
		return render(request,  "moviemons/title_screen.html", {});
	return render(request,  "moviemons/title_screen.html", {});

def Worldmap(request):
	session.load()
	choix = ['left', 'right','up', 'down']

	# if request.GET.get('a') == "select":
	# 	return redirect('/moviedex')
	if request.GET.get('a') == "start":
		return redirect('/options')

	miv = 0
	rand = 0
	stat = "idle"
	if len(session.MoviemonBattle) == 0:
		if request.GET.get('a') in choix:
			if request.GET.get('a') == 'left' and session.mapx > MAPMIN:
				session.mapx-=1
				miv = 1
			if request.GET.get('a') == 'right' and session.mapx < MAPMAX:
				session.mapx+=1
				miv = 1
			if request.GET.get('a') == 'up' and session.mapy > MAPMIN:
				session.mapy-=1
				miv = 1
			if request.GET.get('a') == 'down' and session.mapy < MAPMAX:
				session.mapy+=1
				miv = 1

			if (miv):
				rand = random.randint(1,100)
				if rand > 60 and len(session.get_random_movie()) > 0: #A VERIF
					print("Moviemon trouve", random.choice(session.get_random_movie()))
					stat = "attack"
					session.MoviemonBattle = random.choice(session.get_random_movie())
				elif rand > 40:
					session.modif_movieballs(session.movieballs+1)
					print("Movieball trouve")
					stat = "ball"


	if len(session.MoviemonBattle) > 0:
		stat = "attack"
		print(session.MoviemonBattle)
		if request.GET.get('a') == 'a':
			return redirect('/battle/'+session.MoviemonBattle)
		elif request.GET.get('a') == 'b':
			session.MoviemonBattle = ""
			stat = "balade"
	session.save()

	return render(request, "moviemons/game.html", {
													"movieball": session.movieballs,
													"movietitle":session.MoviemonBattle,
													"stat":stat,
													"mapx":session.mapx,
													"mapy":session.mapy
	})

def Options(request):
	if request.GET.get('a') == 'start':
		return redirect('/worldmap')
	if request.GET.get('a') == 'a':
		return redirect('/options/save_game')
	if request.GET.get('a') == 'b':
		return redirect('/')
	return render(request, "moviemons/options.html")
