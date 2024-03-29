import sys, json, requests, pickle, random, os
from django.conf import settings

class Gestion():

	def __init__(self):
		self.sessionName = 'session.pickle'
		self.set_default()
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
			self.mapx = 5
			self.mapy = 5
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

	def set_value(self,
				new_corrd,
				new_movieballs,
				new_Moviemons,
				new_My_Moviemons,
				new_MoviemonBattle = [],
				new_Strenght = 0,
				new_mapx = 5,
				new_mapy = 5,
				new_index = 0):

		self.coord           = new_corrd
		self.movieballs      = new_movieballs
		self.Moviemons       = new_Moviemons
		self.My_Moviemons    = new_My_Moviemons
		self.MoviemonBattle  = new_MoviemonBattle
		self.Strenght        = new_Strenght
		self.mapx			= new_mapx
		self.mapy            = new_mapy
		self.index			= new_index

	def modif_movieballs(self, nb):
		self.movieballs = nb

	def add_moviemons(self, name):
		self.My_Moviemons.append(name)

	def del_moviemons(self, name):
		del self.Moviemons[name]

	def del_battlemovie(self, moviemon_id):
		self.MoviemonBattle = ''

	def prefix_load(self, name=None):
		if (not name):
			return None;
		info = []
		list_of_files = os.listdir('./saved_game')
		print(list_of_files);
		for each_file in list_of_files:
		    if each_file.startswith(name) and os.path.isfile('./saved_game' + name):
		    	name = './saved_game' + name;
		    	with (open(name, "rb")) as openfile:
		    		while True:
		    			try:
		    				print("Chargement fichier :", name);
		    				info.append(pickle.load(openfile))
		    				print("load index", info[0][8]);
		    			except EOFError:
		    				break
		    	self.set_value(info[0][0], info[0][1], info[0][3], info[0][2], info[0][4], info[0][5], info[0][6], info[0][7], info[0][8])
		    	openfile.close()
		    	return info[0]
		return ("Free")

	def load(self, name=None):
		if (not name):
			name = self.sessionName
		info = []
		print(name,os.path.isfile(name))
		if os.path.isfile(name):
			with (open(name, "rb")) as openfile:
				while True:
					try:
						print("Chargement fichier :", name);
						info.append(pickle.load(openfile))
						print("load index", info[0][8]);
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
			openfile.close()
			return info[0]
		return ("Free")

	def save(self, name=None):
		if (not name):
			name = self.sessionName
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
		print("saved index", self.index);	
		pickle.dump(info, F)
		F.close()

	def dump(self):
		info = []
		with (open(self.sessionName, "rb")) as openfile:
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
		omdb = getattr(settings, "OMDB", None)
		F = open(self.sessionName, "wb")
		for item in self.lst:
			url = omdb['url'] + item + "&apikey=" + omdb['key'];
			r = requests.get(url)
			if r.status_code != 200:
				raise Exception ("Error: " + str(r.status_code))
			Moviemon = json.loads(r.text)
			self.Moviemons[Moviemon['Title'].replace(" ", "_").replace(":", "-")] = Moviemon
		print("x, y", self.mapx, self.mapy);
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

# singleton object
session = Gestion()
