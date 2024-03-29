from django.shortcuts import render, HttpResponse, redirect
from moviemons.gestion import session, Gestion
from django.conf import settings
import random
from datetime import datetime

random.seed(datetime.now())

# Create your views here.
def new(request):
	print (request)
	if request.GET.get('a') == 'a':
		session.load_default_settings()
		session.save()
		return redirect('/worldmap')
	if request.GET.get('a') == 'b':
		return redirect('/options/load_game')
	return render(request,  "moviemons/title_screen.html", {});

def Worldmap(request):
	MAPMIN = 0
	MAPMAX = 9
	params = getattr(settings, "MOVIEMON", None)
	if (params):
		pos = params['GRID_SIZE']
		MAPMIN = pos[0]
		MAPMAX = pos[1]
	session.load()
	choix = ['left', 'right','up', 'down']

	if request.GET.get('a') == "select":
		return redirect('/moviedex')
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
				if rand > 60 and len(session.get_random_movie()) > 0:
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

def Battle(request, moviemon_id):
	remarque = ""
	print (request, moviemon_id)
	session.load()

	if moviemon_id not in session.My_Moviemons:
		if len(session.MoviemonBattle) > 0:
			print(session.MoviemonBattle)
			moviemon_id = session.MoviemonBattle
		elif moviemon_id in session.Moviemons:
			session.MoviemonBattle = moviemon_id
		else:
			return redirect('/')
		if request.GET.get('a') == 'a':
			if session.movieballs > 0:
				session.movieballs -= 1
				if (capture(calcul(session.Moviemons[moviemon_id]['imdbRating'], session.Strenght))):
					session.My_Moviemons.append(moviemon_id)
					remarque = moviemon_id +  " Captured ! B to exit the Battle"
					session.MoviemonBattle = ""
					session.Strenght += 1
				else:
					remarque = "Missed this time, press A to try again!"
			else:
				print("Moquerie")
				remarque = "Dame no more balls!, try to collect more first. B to exit"

	if request.GET.get('a') == 'b':
		session.MoviemonBattle = []
		session.save()
		return redirect('/worldmap')

	print("Print db.moviemon: ",moviemon_id , " : \n",session.Moviemons[moviemon_id])
	print("NB balls:",session.movieballs)

	session.save()
	return render(request, "moviemons/battle.html", {
		"DicoMovie":session.Moviemons[moviemon_id],
		"movieballs":session.movieballs,
		"remarque": remarque,
		"Strenght": session.Strenght,
		"Luck" : calcul(session.Moviemons[moviemon_id]['imdbRating'], session.Strenght)
	})

def load_slots():
	dirtybase = Gestion()
	slotsMy = []
	slotsmon = []
	slots = ["slotA.pickle", "slotB.pickle", "slotC.pickle"]
	slotscut = ["slotA", "slotB", "slotC"]
	for slot in slots:
		if (dirtybase.load(slot) != 'Free'):
			slotsMy.append([slot[0:5], len(dirtybase.My_Moviemons)])
			slotsmon.append([slot[0:5], len(dirtybase.Moviemons)])
		else:
			slotsMy.append([slot[0:5], 0])
			slotsmon.append([slot[0:5], 0])
	return slotsMy, slotsmon


def OptionsSave(request):
	slotsMy, slotsmon = load_slots();
	slots = ["slotA.pickle", "slotB.pickle", "slotC.pickle"]
	slotscut = ["slotA", "slotB", "slotC"]
	
	session.load()
	if request.GET.get('a') == 'up':
		session.index = (session.index - 1) % 3
	if request.GET.get('a') == 'down':
		session.index = (session.index +1) % 3

	if request.GET.get('process') == '1':
		if (len(session.My_Moviemons) > 0 and len(session.Moviemons) > 0):
			name = 'saved_game/' + slotscut[session.index] + "_" + str(len(session.My_Moviemons)) + "_" + str(len(session.Moviemons)) + ".mmg"
			session.save(name)
			session.save(slots[session.index])
		return redirect('/options/save_game')

	print("index", session.index);

	session.save()
	print("smy",slotsMy);
	print("smon",slotsmon);
	if request.GET.get('a') == 'start':
		return redirect('/options/save_game')
	if request.GET.get('a') == 'a':
		return redirect('/options/save_game?process=1')
	if request.GET.get('a') == 'b':
		return redirect('/options')
	return render(request, "moviemons/optionsSave.html", {"slots":slots, "slotsmon":slotsmon,"slotsMy":slotsMy, "name":slotscut[session.index]})


def OptionsLoad(request):
	slotsMy, slotsmon = load_slots();
	slots = ["slotA.pickle", "slotB.pickle", "slotC.pickle"]
	slotscut = ["slotA", "slotB", "slotC"]

	session.load()
	if request.GET.get('a') == 'up':
		session.index = (session.index - 1) % 3
	if request.GET.get('a') == 'down':
		session.index = (session.index +1) % 3

	if request.GET.get('process') == '1':
		if (slotsmon[session.index][1] != 0):
			session.load(slots[session.index])
			session.save()
			return redirect('/worldmap')

	session.save()
	print("smy",slotsMy);
	print("smon",slotsmon);
	if request.GET.get('a') == 'start':
		return redirect('/options/load_game')
	if request.GET.get('a') == 'a':
		return redirect('/options/load_game?process=1')
	if request.GET.get('a') == 'b':
		return redirect('/options')
	return render(request, "moviemons/optionsLoad.html", {"slots":slots, "slotsmon":slotsmon,"slotsMy":slotsMy, "name":slotscut[session.index]})

def Moviedex(request):
	session.load()
	newdico = {}
	session.My_Moviemons.sort()

	if request.GET.get('a') == 'select':
		session.index = 0;
		session.save();
		return redirect('/worldmap')

	if (len(session.My_Moviemons)):
		for elem in session.My_Moviemons:
			newdico[elem] = session.Moviemons[elem]

		print(session.index)
		if (len(session.My_Moviemons)):
			if request.GET.get('a') == 'down':
				session.index = (session.index  + 1) %len(session.My_Moviemons)
			if request.GET.get('a') == 'up':
				session.index = (session.index  + -1) %len(session.My_Moviemons)
			session.save()

		if request.GET.get('a') == 'a':
			return redirect('/moviedex/'+session.My_Moviemons[session.index])
		
		return render(request, "moviemons/moviedex.html", {"dico": newdico, "cursor": session.My_Moviemons[session.index]})
	else:
		return render(request, "moviemons/moviedex.html")

def MoviedexDetail(request, moviemon_id):
	session.load()
	if request.GET.get('a') == 'b':
		return redirect('/moviedex')
	return render(request, "moviemons/moviedexdetail.html", {"detail": session.Moviemons[moviemon_id]})

def Options(request):
	if request.GET.get('a') == 'start':
		return redirect('/worldmap')
	if request.GET.get('a') == 'a':
		return redirect('/options/save_game')
	if request.GET.get('a') == 'b':
		return redirect('/')
	return render(request, "moviemons/options.html")

def calcul(StrenghtMovie, StrenghtPlayer):
	C = 50 - (float(StrenghtMovie) * 10) + (StrenghtPlayer * 5)
	if C < 1:
		C = 1
	if C > 90:
		C = 90
	return C

def capture(C):
	if random.randint(0,100) < C:
		return (True)
	return (False)
