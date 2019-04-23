# pygtk-jsonview
A module for python used in conjunction with GTK that provides a treeview, liststore, and filter list for a set of JSON data.  

The view is created with the data attached, like so:

```python
JSONView([{"name": "Eric", "class": "Wizard"}, {"name": "Winry", "class": "Dog"}])
```

Field types may be specified using the `headers` property:

```python
headers= {"name": {"name": "Player Name", "type": str}, "class": {"name": "PC Class", "type": str}}
data = [{"name": "Eric", "class": "Wizard"}, {"name": "Winry", "class": "Dog"}]
jsonview = JSONView(data, headers = headers)
```

Header information **must** include:
* `name` the field title.
* `type` the field type in python primitive.  This is used to set the treeview column renderer.

Header information **may** include:
* `enum` a boolean value specifying whether the values should be treated as a finite set.
* `displayasstring` a boolean value specifying whether to render the data as a string.  This is useful for showing python datatypes.  A dictionary field will be represented as the string format of the dictionary, while a list field will be represented as comma-separated values.  

If header information is not supplied when the view is initialized, it assumes a "best guess" approach that is probably sufficient for many programs.  It assumes that the datatype in each column will be the same for each row, and then reads the JSON data to create the header dictionary.  This is also a useful way to get a header dictionary that is mostly what you want when you are creating a program.  

Filter generation is not ready yet.  
