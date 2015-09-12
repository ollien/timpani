import json
import os
import os.path

class ConfigManager():
	_caches = {}
	def __init__(self, configPath = "configs/", overrideCache = False):
		if os.path.isdir(configPath):
			self.configPath = configPath
		elif os.path.isfile(configPath):
			raise ValueError("configPath is a file, expected directory.")
		else:
			raise ValueError("configPath does not eixst.")

		if not overrideCache and configPath in ConfigManager._caches:
			self._cache = ConfigManager._caches['path']
		else:
			self._cache = {}

		self._configs = {}
		self._syncCache()
		self.getConfigs()

	def __getitem__(self, key):
		try:
			return self._configs[key]
		except KeyError:
			self._syncCache()
			return self._configs[key]

	#Recursive function to get all files. Sub is the relative path from the root config dir.	
	def getConfigs(self, path = None, sub = "", overrideCache = False):
		if path == None:
			path = self.configPath
		files = os.listdir(path)	
		for item in files:
			#Ignore hidden files.
			if item[0] == ".":
				continue

			#Remove the .json handle from the name
			name = item.replace(".json", "")
			finalName = os.path.join(sub, name)

			#If it's a directory, run this function again within that directory
			if os.path.isdir(os.path.join(path, item)):
				self.getConfigs(path = os.path.join(path, item), sub = os.path.join(sub, item))
			#If we already have something from the cache, or added in previously, skip it.
			elif overrideCache or finalName not in self._configs:
				#Read in the file
				f = open(os.path.join(path, item), "r")
				#Check if it's JSON. If it is, it will be parsed.
				parsed = self.parseConfig(f.read())
				f.close()
				if parsed != None:
					self.addConfig(finalName, parsed)
	#Returns parsed JSON if config is valid JSON, otherwise, return Noen	
	def parseConfig(self, config):
		try:
			return json.loads(config)
		except ValueError:
			return None
	
	def addConfig(self, name, contents):
		self._configs[name] = contents
		self._cache[name] = contents
	
	def _syncCache(self):
		unmatchedKeys = [key for key in self._cache.keys() if key not in self._configs]
		for key in unmatchedKeys:
			self._configs[key] = self._cache[key]
