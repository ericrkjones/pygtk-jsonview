import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Checklist(Gtk.ListBox):
	'''An extension of the concept of a CheckButton, this is a ListBox of CheckButtons.
	A dictionary of "{Label: [Value]}" is supplied. In many cases, Label==Value.
	The Checklist has a function that returns a dictionary of "{Value: Boolean}".
	Functionally, this allows the developer to re-name data. For example, if I had a boolean value, but I wanted to represent it as "Up" or "Down", I could make my choices = {"Up":True, "Down":False}.
	The Checklist also aggregates all of its children's triggered functions so that it can perform a triggered function.'''
	
	choices = {}

	def __init__(self, choices = None,  *args, **kwds):
		super().__init__(*args, **kwds)
		for key in choices:
			self.add(key, value = choices[key])
	def add(self, label, value = None):
		'''Adds labeling information to the choices property and a checkbox element to the Checklist.'''
		if value is None:
			value = label
		if label in self.choices:
			raise KeyError(label + " already in choices list, duplicates are not allowed.")
		self.choices[label] = value
		self.add_entry(label, value)

	def add_entry(self, label, value):
		row = Gtk.ListBoxRow()
		button = Gtk.CheckButton.new_with_label(label)
		row.add(button)
		super().add(row)
		
	def set_all(self, boolean):
		for row in self.get_children():
			checkbox = row.get_child()
			checkbox.set_active(boolean)
			
	def get_state(self):
		choices_state = {}
		for row in self.get_children():
			checkbox = row.get_child()
			label = checkbox.get_label()
			choices_state[self.choices[label]] = checkbox.get_active()
		return choices_state

	def get_state_unlabeled(self):
		state = [row.get_child().get_active() for row in self.get_children()]
		return state

	def get_all_active(self):
		return all(self.get_state_unlabeled())

	def get_all_inactive(self):
		return all(not(self.get_state_unlabeled()))

class BooleanChecklist(Checklist):
	'''A special time-saving class of CheckList that is very simply a boolean "True/False" with labels "True/False".'''
	__gtype_name__ = 'BooleanChecklist'

	def __init__(self, *args, **kwds):
		super().__init__(choices = {"True": True, "False": False}, *args, **kwds)
