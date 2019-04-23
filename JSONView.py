#!/usr/bin/python3
import json
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class JSONView():
	"""Loads a JSON database as a tree view with a liststore and an accompanying filter menu.  Headers and filters can either be set manually with a header dictionary or, if not specified, loaded from data type assumptions.
	
	Format:
		{
			'id': {
				'name': 'Identification Number',
				'type': int,
				'enum': False,
				'filterdisplay': False,
				'viewdisplay': True
			},
			'name': {
				'name': 'Name',
				'type': str,
				'enum': True,
				'filterdisplay': True,
				'viewdisplay': True,
				'filter': 'radio'
			},
			'job': {
				'name': 'Job',
				'type': str,
				'enum': True,
				'filterdisplay': True,
				'viewdisplay': True
				'filter': 'check'
			}
		}
	The 'enum' field is true for fields 'name' and 'job', indicating that, when the database is imported, sets of distinct elements will be stored in the 'set' key.  
	"""

	def __init__(self, data, headers = None, allownofilter = True):
		"""Initialize the views.

		allownofilter: shows the entire dataset on load if true, otherwise needs at least 1 filter
		"""
		self.data = data
		if headers is None:
			headers = self.createJSONHeaders()
		self.headers = headers
		self.populateEnums()
		self.ListStore = self.buildListStore()
		self.View = self.buildTreeView(self.ListStore)
		self.Filter = self.buildFilter()

	def buildTreeView(self, store):
		recordview = Gtk.TreeView(store)
		for index, key in enumerate(self.headers):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(self.headers[key]['name'], renderer, text = index)
			column.set_sort_column_id(index)
			recordview.append_column(column)
		scroll = Gtk.ScrolledWindow()
		scroll.add(recordview)
		return scroll

	def buildListStore(self):
		"""Build the ListStore that contains all the visible data"""
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
		for record in self.data:
			for key in self.headers:
				# If the data in the record is a list or set, treat it as though it is a list of unique values
				if 'enum' in self.headers[key]:
					if self.headers[key]['enum']:
						if 'set' not in self.headers[key]:
							self.headers[key]['set'] = set()
						try:
							self.headers[key]['set'].update(record[key])
						except TypeError:
							print("Could not add elements of " + str(record[key]) + " to set of distinct values for " + key)

	def buildFilter(self):
		self.filterlist = Gtk.ListBox()
		scroll = Gtk.ScrolledWindow()
		scroll.add(self.filterlist)
		return scroll

	def createJSONHeaders(self):
		autodatatypes = [str, int, float, bool, dict]
		stringreformattypes = [dict]
		enumerabletypes = [str, int]
		listtypes = [list, set]
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
					else:
						enumerated = False
						recordtype = type(record[key])

					if recordtype is not None and enumerated is not None:
						displayasstring = islist or recordtype in stringreformattypes
						if recordtype in autodatatypes:
							headers[key] = {'name': key, 'enum': enumerated, 'type': recordtype, 'displayasstring': displayasstring, 'islist': islist, 'viewdisplay': True, 'filterdisplay': True}
		return headers
