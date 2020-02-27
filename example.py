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
		self.set_default_size(1200,600)
		self.resizable = True
		self.connect("destroy", Gtk.main_quit)
		self.pane = Gtk.HPaned()
		self.jsonview = JSONView(data, headers = headers)
		self.inner_pane = Gtk.HPaned()
		self.inner_pane.add(self.jsonview.View)
		self.details_scroll = Gtk.ScrolledWindow()
		self.details_scroll.add_with_viewport(self.jsonview.Details)
		self.inner_pane.add(self.details_scroll)
		self.pane.add(self.inner_pane)
		self.pane.add(self.jsonview.FilterView)
		self.inner_pane.set_position(400)
		self.pane.set_position(800)
		self.add(self.pane)

#data = loadJSONData(jsonfile)
# headers= {"name": {"name": "Player Name", "type": str}, "class": {"name": "PC Class", "type": str}}
headers = None
data = [{"name": "Eric", "class": ["Wizard"], "eatspoop": False}, {"name": "Winry", "class": ["Dog", "Seal"], "eatspoop": True}]

window = MainWindow()
window.show_all()
Gtk.main()

# {'name': {'name': 'name', 'enum': False, 'type': <class 'str'>, 'displayasstring': False, 'islist': False, 'viewdisplay': True, 'filterdisplay': True, 'filtertype': 'regexpattern', 'detailstype': 'text'}, 'class': {'name': 'class', 'enum': True, 'type': <class 'str'>, 'displayasstring': True, 'islist': True, 'viewdisplay': True, 'filterdisplay': True, 'filtertype': 'checklist', 'detailstype': 'text', 'set': {'Seal', 'Dog', 'Wizard'}}, 'eatspoop': {'name': 'eatspoop', 'enum': False, 'type': <class 'bool'>, 'displayasstring': False, 'islist': False, 'viewdisplay': True, 'filterdisplay': True, 'filtertype': 'booleanchecklist', 'detailstype': 'text'}}
