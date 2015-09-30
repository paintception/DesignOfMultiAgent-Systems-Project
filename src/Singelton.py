def Singelton(cls):
	instances = {}
	def getInstance():
		if cls not in instances:
			instances[cls] = cls()
			return instances[cls]
	return getInstance
