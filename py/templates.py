import os.path
import jinja2
import configmanager

configs = configmanager.ConfigManager(os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs")))
templateConfig = configs["templates"]
templatePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", templateConfig["template_directory"]))

class TemplateManager():
	def __init__(self, path = templatePath):
		self.environment = jinja2.Environment(loader = jinja2.FileSystemLoader(path))

	def __getitem__(self, attr):
		try:
			return self.environment.get_template(attr)
		except jinja2.TemplateNotFound:
			try:
				return self.environment.get_template(attr+".html")	
			except jinja2.TemplateNotFound:
				return None
