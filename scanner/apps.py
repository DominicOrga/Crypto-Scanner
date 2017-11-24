from django.apps import AppConfig
from .services import TestServiceSingleton

class ScannerConfig(AppConfig):
    name = 'scanner'

    def ready(self):
    	TestServiceSingleton().run()
    	TestServiceSingleton().run()
    	TestServiceSingleton().run()
    	

