import threading
import time

class TestServiceSingleton(object):
	__instance = None
	__is_running = False

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)

		return cls.__instance

	def run(self):
		if self.__is_running:
			return

		def daemon():
			while True:
				print("hello")
				time.sleep(3)

		th = threading.Thread(target=daemon)
		th.daemon = True
		th.start()

		self.__is_running = True