#!/usr/bin/python3.7
import yaml
import json
import sys
import os
import PyInquirer
import random
from sty import fg, rs

class ui:
	@staticmethod
	def colored_cube(l, h, color):
		""" `color` is a rgb 3-tuple
		"""
		for _ in range(h):
			print(fg(*color) + '#' * l + rs.fg)

class ask:
	@staticmethod
	def _ask(**kwargs):
		return PyInquirer.prompt([{**kwargs, 'name': '_ans'}])['_ans']

	@classmethod
	def confirm(cls, message, default=False):
		return cls._ask(message=message, default=default, type='confirm')

	@classmethod
	def choose(cls, message, choices, type='list', default=None):
		return cls._ask(message=message, choices=choices, type=type, default=default)

	@classmethod
	def choose_several(cls, message, choices, type='expand', default=None):
		return cls._ask(message=message, choices=choices, type=type, default=default)

	@classmethod
	def input(cls, message, default=""):
		return cls._ask(message=message, type='input', default=default)

	@classmethod
	def input_several(cls, message, default=[]):
		answers = []
		ans = None
		while ans != "":
			ans = cls.input(message + " (Hit enter to finish)")
			answers.append(ans)
		return answers

class Database:
	def __init__(self, in_file, out_file):
		self.in_file = in_file
		self.out_file = out_file

	def __enter__(self):
		self._nested_content = self.read_file(self.in_file)
		self._flat_content = self._flat(self._nested_content)
		self.content = self._append_collections_to_products(self._flat_content)
		self.content = self._add_full_id_to_products(self.content)
		return self

	def __exit__(self, *args, **kwargs):
		self.write_file(self.out_file, self.content)

	def read_file(self, filepath):
		with open(filepath, "r") as file:
			raw = file.read()
			parsed = yaml.load(raw)
		return parsed

	def write_file(self, filepath, contents, format="json"):
		with open(filepath, "w") as file:
			if format == "json":
				raw = json.dumps(contents)
			elif format == "yaml":
				raw = yaml.dump(contents, Dumper=yaml.CDumper)
			else:
				raise ValueError("format must be either 'json' or 'yaml'")
			file.write(raw)

	@classmethod
	def _flatten_obj(cls, obj):
		flat = []
		for (key, value) in obj.items():
			flat.append({**value, **{"id": key}})
		return flat

	@classmethod
	def _flat(cls, content):
		flat_collections = cls._flatten_obj(content)
		flat_products_collections = []
		for collection in flat_collections:
			flat_products = cls._flatten_obj(collection["products"])
			collection["products"] = flat_products
			flat_products_collections.append(collection)
		return flat_products_collections

	@staticmethod
	def _append_collections_to_products(content):
		for collection in content:
			collection_no_products = {**collection}
			del collection_no_products["products"]
			for product in collection["products"]:
				product["collection"] = collection_no_products
		return content

	@staticmethod
	def _add_full_id_to_products(content, sep="--"):
		with_full_ids = []
		for collection in content:
			products = []
			for product in collection["products"]:
				with_full_ids.append(
					{'uid': f'{collection["id"]}{sep}{product["id"]}', **product}
				)
			with_full_ids.append(
				{**collection, 'products': products}
			)
		return with_full_ids

	def get_collection(self, collection_id):
		for collection in self.content:
			if collection["id"] == collection_id:
				return collection
		raise KeyError(f"Collection with id '{collection_id}' not found")

	def get_product(self, collection_id, product_id):
		collection = self.get_collection(collection_id)
		for product in collection["products"]:
			if product["id"] == product_id:
				return product
		raise KeyError(f"Product with id '{product_id}' not found")

	def add_product(self, **properties):
		name = properties.get('name', ask.input("Product name"))
		categories = properties.get('categories', ask.choose_several("Categories", [
			{
				'name': v.title(),
				'value': v,
				'key': v[0]
			} for v in ['graphism', 'software', 'motion', 'music']
			]))
		tags = properties.get('tags', ask.input_several("Tags"))
		if 'color' in properties.keys():
			color = properties['color']
		else:
			def random_color():
				return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
			color = None
			if ask.confirm("Extract color from the image?"):
				#FIXME:IS PLACEHOLDER
				confirmed = None
				extracted_color = random_color()
				ui.colored_cube(4, 4, extracted_color)
				if ask.confirm("Is that color right?"):
					color = extracted_color
			if color is None:
				color = ask.input("Enter an hexadecimal color (#RRGGBB)", default='#FFFFFF')
			






if __name__ == "__main__":
	with Database(sys.argv[1], sys.argv[1].replace(".yaml", ".json")) as db:
		db.add_product(name="Test", categories=["music"], tags=[])
