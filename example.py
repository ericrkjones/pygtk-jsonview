#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from JSONView import *

def loadJSONData(file):
	with open(file, 'r') as jsondata:
		d = json.load(jsondata)
	return d

class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="JSONView Demo")
		self.set_default_size(800,600)
		self.resizable = True
		self.connect("destroy", Gtk.main_quit)
		self.pane = Gtk.HPaned()
		self.jsonview = JSONView(data, headers = headers)
		self.pane.add(self.jsonview.View)
		self.pane.add(self.jsonview.Filter)
		self.add(self.pane)

#data = loadJSONData(jsonfile)
headers= {"name": {"name": "Player Name", "type": str}, "class": {"name": "PC Class", "type": str}}
data = [{"name": "Eric", "class": "Wizard"}, {"name": "Winry", "class": "Dog"}]
window = MainWindow()
window.show_all()
Gtk.main()
