#!/usr/bin/env python3
"""Compiles a DaD (Database as Directory) to a single file for use with generated static websites

Usage:
	swdbc DIRECTORY [-o OUTPUT_FILE] [options]

Options:
	-o, --ouput FILE		Compiles to the given output. [default: database.toml]
											Defaults to "FILE" with the extension replaced with .json
	--as FORMAT					Output file format. Supported formats: json, yaml, toml. [default: toml]
	-v, --videos				Process videos
	-p, --pdfs					Process PDFs
	-t, --thumbnails		Generate thumbnails
	-d, --database			Compile the database file
	--all								Shortcut for -vptd
"""
from urllib.parse import urlparse
from datetime import date
import os
from docopt import docopt
import toml
import yaml
from typing import List, Union
import pastel

def run():
	args = docopt(__doc__)
	print(args)
	if not os.path.exists(args['DIRECTORY']):
		print(pastel.colorize(f'<red>Fatal error:</red> Directory <cyan>{args["DIRECTORY"]!r}</cyan> does not exist.'))
	if args['--database']:
		print('compiling database')


class Common:
	def __init__(self, id: str, name: str, description: str, categories: List[str], tags: List[str], created: date):
		self.id = id
		self.name = name
		self.description = description
		self.categories = categories
		self.tags = tags
		self.created = created

class Collection(Common):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class Link:
	def __init__(self, url, name=None):
	 self.url = url
	 self.name = name or self.compute_name()
	
	def compute_name(self):
		url = urlparse(self.url)
		domain = url.netloc.replace(url.scheme + '://', '')
		return domain


class Product(Common):
	def __init__(
		self,
		links: Union[dict, List[str], List[dict]],
		**kwargs
	):
		super().__init__(**kwargs)
		self.links = self._compute_links()
	
	def _compute_links(self, links):
		computed_links = []
		if type(links) is dict:
			for name, url in links.items():
				computed_links.append(Link(url=url, name=name))
		elif type(links) is list:
			for link in links:
				if type(link) is str:
					computed_links.append(Link(url=link))
				else:
					computed_links.append(Link(**link))
		return computed_links

class Variant(Common):
	def __init__(self, filename: str, **kwargs):
		super().__init__(**kwargs)
		self.filename = filename

if __name__ == "__main__":
		run()
