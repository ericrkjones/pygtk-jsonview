#!/usr/bin/python3
import json
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from GtkCustomWidgets import *

class JSONView():
	"""Loads a JSON database as a tree view with a liststore and an accompanying filter menu.  Headers and filters can either be set manually with a header dictionary or, if not specified, loaded from data type assumptions.
	
	Format:
		headers:
		{
			'id': {
				'name': 'Identification Number',
				'type': int,
				'enum': False,
				'filterdisplay': False,
				'viewdisplay': True,
				'detailstype': 'text'
			},
			'name': {
				'name': 'Name',
				'type': str,
				'enum': True,
				'filterdisplay': True,
				'viewdisplay': True,
				'filter': 'checklist',
				'detailstype': 'text'
			},
			'job': {
				'name': 'Job',
				'type': str,
				'enum': True,
				'filterdisplay': True,
				'viewdisplay': True
				'filter': 'checklist',
				'detailstype': 'text'
			}
		},
		filter_order: ['name', 'job'],
		details_order: ['id', 'name', 'job']
	The 'enum' field is true for fields 'name' and 'job', indicating that, when the database is imported, sets of distinct elements will be stored in the 'set' key.  
	"""

	def __init__(self, data,
				 headers = None,
				 filter_order = None,
				 details_order = None,
				 enable_view = True,
				 view_require_filter = False,
				 enable_filter = True,
				 filter_apply_on_change = True,
				 enable_details = True):
		"""Initialize the views.

		allownofilter: shows the entire dataset on load if true, otherwise needs at least 1 filter
		"""
		# Set data property
		self.data = data

		# Auto-create headers from best guess if necessary
		if headers is None:
			headers = self.createJSONHeaders()
		self.headers = headers

		# print(self.headers) # Debugging

		# Populate the 'set' key for each header element.
		# If a header dictionary already has a 'set' key, they will not be updated
		self.populateEnums()
		print(self.headers)
		
		# Create the liststore from the data and then the view from the liststore
		if enable_view:
			self.ListStore = self.buildListStore()
			self.View = self.buildTreeView(self.ListStore)
			self.ListStoreFilter = self.ListStore.filter_new()

		if enable_filter:
			self.FilterView = self.buildFilterView()
			self.FilterView.show_all()

		if enable_details:
			self.Details = self.buildDetailsView()
			self.Details.show_all()
		
	def buildTreeView(self, store):	
		"""Create the tree view according to the header data and fill it with a list store."""
		recordview = Gtk.TreeView(store)
		recordview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		for index, key in enumerate(self.headers):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(self.headers[key]['name'], renderer, text = index)
			column.set_sort_column_id(index)
			recordview.append_column(column)
		scroll = Gtk.ScrolledWindow()
		scroll.add(recordview)
		return scroll

	def buildListStore(self):
		"""Build the ListStore that contains all the visible data for the item selected in the TreeView."""
		columns = []
		for key in self.headers:
			if 'displayasstring' in self.headers[key] and self.headers[key]['displayasstring']:
				columntype = str
			else:
				columntype = self.headers[key]['type']
			columns.append(columntype)
		liststore = Gtk.ListStore(*columns)
		for record in self.data:
			thisrow = []
			for key in self.headers:
				if key in record:
					if 'displayasstring' in self.headers[key] and self.headers[key]['displayasstring']:
						if type(record[key]) is list:
							item = ", ".join([str(x) for x in record[key]])
						elif type(record[key]) is dict:
							item = ", ".join([str(x) + ": " + str(record[key][x]) for x in record[key]])
						else:
							item = str(record[key])
					else:
						item = record[key]
				else:
					item = None
				thisrow.append(item)
			liststore.append(thisrow)
		return liststore

	def populateEnums(self):
		"""Populate a set of distinct values for each field in JSON.  
		Steps through each of the "rows" of the JSON list and, for each non-null value where the header 'enum' value is true, merges the value of the element with the set of known values in the header set.  """
		enumsets = {}
		for record in self.data:
			for key in self.headers:
				# If the data in the record is a list or set, treat it as though it is a list of unique values
				if 'enum' in self.headers[key]:
					if self.headers[key]['enum']:
						if key not in enumsets:
							enumsets[key] = set()
						try:
							enumsets[key].update(record[key])
						except TypeError:
							sprint("Could not add elements of " + str(record[key]) + " to set of distinct values for " + key)
		for key in enumsets:
			if 'enumchoices' not in self.headers[key]:
				enumlist=list(enumsets[key])
				enumlist.sort()
				choices = {}
				for item in enumlist:
					choices[item] = item
				self.headers[key]['enumchoices'] = choices

	def packageFilterRow(self, key, widget):
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		box.add(Gtk.Label(self.headers[key]['name']))
		box.add(widget)
		row = Gtk.ListBoxRow()
		row.set_activatable(False)
		row.add(box)
		return row

	def packageDetailsRow(self, key):
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		box.add(Gtk.Label(self.headers[key]['name']))
		box.add(self.details_widgets[key])
		row = Gtk.ListBoxRow()
		row.set_activatable(False)
		row.add(box)
		return row
		
	def buildRegexPatternFilter(self, key):
		pass

	def buildMinMaxEntryFilter(self, key):
		pass

	def buildFilterView(self):
		self.filter_widgets = {}
		filterlist = Gtk.ListBox()
		filterlist.set_selection_mode(Gtk.SelectionMode.NONE)
		for key in self.headers:
			filtertype = self.headers[key].get('filtertype')
			if filtertype == 'booleanchecklist':
				# self.filter_widgets[key] = BooleanChecklist()
				widget = BooleanChecklist()
				widget.set_all(True)
				filterlist.add(self.packageFilterRow(key, widget))
			if filtertype == 'checklist':
				# self.filter_widgets[key] = Checklist(choices = self.headers[key]['enumchoices'])
				widget = Checklist(choices = self.headers[key]['enumchoices'])
				widget.set_all(True)
				filterlist.add(self.packageFilterRow(key, widget))
		# for key in self.filter_widgets:
		# 	filterlist.add(self.packageFilterRow(key))
		return filterlist

	def changeFilter(self, field, key):
		print("Filter values changed for " + key)
		# for key in self.Filter

	def buildDetailsTextElement(self, key):
		widget = Gtk.Label()
		return widget
		
	def buildDetailsView(self):
		# This function needs to create a dictionary self.details_items for which each key is a widget.
		self.details_widgets = {}
		detailslist = Gtk.ListBox()
		detailslist.set_selection_mode(Gtk.SelectionMode.SINGLE)
		for key in self.headers:
			detailstype = self.headers[key].get('detailstype')
			if detailstype == 'text':
				self.details_widgets[key] = self.buildDetailsTextElement(key)
		for key in self.details_widgets:
			detailslist.add(self.packageDetailsRow(key))
		return detailslist

	def createJSONHeaders(self):
		autodatatypes = [str, int, float, bool, dict]
		stringreformattypes = [dict]
		enumerabletypes = [str, int]
		listtypes = [list, set, tuple]
		"""Read the JSON data and output a dictionary with all field keys, datatypes, and, if the field type is list or tuple, a set of all unique elements."""
		headers = {}
		for record in self.data:
			for key in record:
				# If the key is not in headers, create a new dictionary variable assigned to the key
				if key not in headers:
					# Determine the record type and whether to treat as enumerated
					islist = type(record[key]) in listtypes
					if islist:
						if len(record[key]) > 0:
							recordtype = type(record[key][0])
							displayasstring = True
							enumerated = recordtype in enumerabletypes
					else:
						enumerated = False
						recordtype = type(record[key])

					# Try to set a filter type for the filter widget
					try:
						if recordtype is str:
							if enumerated:
								filtertype = 'checklist'
							else:
								filtertype = 'regexpattern'
						elif recordtype is int:
							if enumerated:
								filtertype = 'checklist'
							else:
								filtertype = 'minmaxentry'
						elif recordtype is float:
							if enumerated:
								filtertype = 'checklist'
							else:
								filtertype = 'minmaxentry'
						elif recordtype is bool:
							filtertype = 'booleanchecklist'
						else:
							raise(TypeError)
						filterdisplay = True
					except TypeError:
						print("" + key + " type " + str(recordtype) + " (enumerated: " + str(enumerated) + ") is not supported for automatic filter assignment.")
						filterdisplay = False
					
					if recordtype is not None and enumerated is not None:
						displayasstring = islist or recordtype in stringreformattypes
						if recordtype in autodatatypes:
							headers[key] = {'name': key, 'enum': enumerated, 'type': recordtype, 'displayasstring': displayasstring, \
											'islist': islist, 'viewdisplay': True, 'filterdisplay': filterdisplay, 'filtertype': filtertype, 'detailstype': 'text'}
		return headers
