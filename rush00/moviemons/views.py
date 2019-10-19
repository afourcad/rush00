from django.shortcuts import render, HttpResponse, redirect
from moviemons.gestion import db

# Create your views here.
def new(request):
	print (request)
	if request.GET.get('a') == 'a':
		db.load_default_settings()
		db.save()
		return redirect('/worldmap')
	if request.GET.get('a') == 'b':
		# return redirect('/options/load_game')
		return render(request,  "moviemons/title_screen.html", {});
	return render(request,  "moviemons/title_screen.html", {});

def Worldmap(request):
	db.load()
	choix = ['left', 'right','up', 'down']

	# if request.GET.get('a') == "select":
	# 	return redirect('/moviedex')
	# if request.GET.get('a') == "start":
	# 	return redirect('/options')

	miv = 0
	rand = 0
	stat = "idle"
	if len(db.MoviemonBattle) == 0:
		if request.GET.get('a') in choix:
			if request.GET.get('a') == 'left' and db.mapx > MAPMIN:
				db.mapx-=1
				miv = 1
			if request.GET.get('a') == 'right' and db.mapx < MAPMAX:
				db.mapx+=1
				miv = 1
			if request.GET.get('a') == 'up' and db.mapy > MAPMIN:
				db.mapy-=1
				miv = 1
			if request.GET.get('a') == 'down' and db.mapy < MAPMAX:
				db.mapy+=1
				miv = 1

			if (miv):
				rand = random.randint(1,100)
				if rand > 60 and len(db.get_random_movie()) > 0: #A VERIF
					print("Moviemon trouve", random.choice(db.get_random_movie()))
					stat = "attack"
					db.MoviemonBattle = random.choice(db.get_random_movie())
				elif rand > 40:
					db.modif_movieballs(db.movieballs+1)
					print("Movieball trouve")
					stat = "ball"


	if len(db.MoviemonBattle) > 0:
		stat = "attack"
		print(db.MoviemonBattle)
		if request.GET.get('a') == 'a':
			return redirect('/battle/'+db.MoviemonBattle)
		elif request.GET.get('a') == 'b':
			db.MoviemonBattle = ""
			stat = "balade"
	db.save()

	return render(request, "moviemons/game.html", {
													"movieball": db.movieballs,
													"movietitle":db.MoviemonBattle,
													"stat":stat,
													"mapx":db.mapx,
													"mapy":db.mapy
	})
