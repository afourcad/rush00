import sys, json, requests, pickle, random, os
from django.conf import settings

class Gestion():

	def __init__(self):
		params = getattr(settings, "MOVIEMON", None)
		if not params:
			print('Missing setting MOVIEMON')
			movies = ['Manos: The Hands of Fate'] # par defaut
		else:
			movies = params['MOVIES']
		self.lst = movies
		print('Movie list : ',self.lst)

	
	def set_default(self):
		params = getattr(settings, "MOVIEMON", None)
		if not params:
			print('Missing setting MOVIEMON')
			self.mapx = 50
			self.mapy = 50
		else:
			pos = params['INITIAL_PLAYER_POS']
			self.mapx = pos[0]
			self.mapy = pos[1]
		print('Initial player position: ', self.mapx, ", ", self.mapy)

		self.coord           = [48.8584, 2.2945]
		self.movieballs      = 100
		self.Moviemons       = {}
		self.My_Moviemons    = []
		self.MoviemonBattle  = ''
		self.Strenght        = 0
		self.index 			 = 0

	def set_value(cls,
				new_corrd,
				new_movieballs,
				new_Moviemons,
				new_My_Moviemons,
				new_MoviemonBattle = [],
				new_Strenght = 0,
				new_mapx = 50,
				new_mapy = 50,
				new_index = 0):

		cls.coord           = new_corrd
		cls.movieballs      = new_movieballs
		cls.Moviemons       = new_Moviemons
		cls.My_Moviemons    = new_My_Moviemons
		cls.MoviemonBattle  = new_MoviemonBattle
		cls.Strenght        = new_Strenght
		cls.mapx			= new_mapx
		cls.mapy            = new_mapy
		cls.index			= new_index

	def move_coord(self, x, y):
		self.coord[0] = x
		self.coord[1] = y

	def modif_movieballs(self, nb):
		self.movieballs = nb

	def add_moviemons(self, name):
		self.My_Moviemons.append(name)

	def del_moviemons(self, name):
		del self.Moviemons[name]

	def del_battlemovie(self, moviemon_id):
		self.MoviemonBattle = ''

	def load(self, name):
		info = []
		print(name,os.path.isfile(name))
		if os.path.isfile(name):
			with (open(name, "rb")) as openfile:
				while True:
					try:
						print("Chargement fichier :", name);
						info.append(pickle.load(openfile))
					except EOFError:
						break
			self.set_value(info[0][0],
						   info[0][1],
						   info[0][3],
						   info[0][2],
						   info[0][4],
						   info[0][5],
						   info[0][6],
						   info[0][7],
						   info[0][8])
			self.save('info.pickle')
			openfile.close()
			return info[0]
		return ("Free")

	def dump(self):
		info = []
		with (open("info.pickle", "rb")) as openfile:
			while True:
				try:
					info.append(pickle.load(openfile))
				except EOFError:
					break
		openfile.close()
		return info[0]

	def get_random_movie(self):
		my_mon = self.My_Moviemons
		mon = list(self.Moviemons.keys())
		return [x for x in mon if x not in my_mon]

	def load_default_settings(self):
		self.set_default()
		F = open("info.pickle", "wb")
		for item in self.lst:
			r = requests.get("http://www.omdbapi.com/?t=" + item + "&apikey=xxxxxxxx")
			if r.status_code != 200:
				raise Exception ("Error: " + str(r.status_code))
			Moviemon = json.loads(r.text)
			self.Moviemons[Moviemon['Title'].replace(" ", "_").replace(":", "-")] = Moviemon
		info = [
				self.coord,
				self.movieballs,
				self.My_Moviemons,
				self.Moviemons,
				self.MoviemonBattle,
				self.Strenght,
				self.mapx,
				self.mapy,
				self.index
		]

		pickle.dump(info, F)
		F.close()
		return info

	def get_strength(self):
		return len(self.My_Moviemons)

	def get_movie(self):
		return self.Moviemons[name]

	def get_all_movies(self):
		info = self.dump()
		return list(info[3].keys())

	def save(self, name):
		F = open(name, "wb")
		info = [
				self.coord,
				self.movieballs,
				self.My_Moviemons,
				self.Moviemons,
				self.MoviemonBattle,
				self.Strenght,
				self.mapx,
				self.mapy,
				self.index
			]

		pickle.dump(info, F)
		F.close()


# singleton object
db = Gestion();


























