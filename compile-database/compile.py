#!/usr/bin/env python3
"""A compiler for works.yaml file for my portfolio

Usage:
  swdbc [options]
  swdbc (-h|--help|--version)

Files & directories options
--works=<file>         The works YAML file [default: ../static/works.yaml]
--renders=<directory>  The directory where renders are stored [default: ../static/works]
--collections=<file>   The collections YAML file [default: ../static/collections.yaml]
--sites=<file>         The sites YAML file [default: ../static/sites.yaml]

Miscellaneous options
--verbose=<level>      The verbosity level, 0 to quiet [default: 2]
"""
import os, shutil
from typing import List, Dict, Optional, Union
from docopt import docopt
from PIL import Image
import pastel
from ruamel.yaml import YAML
yaml = YAML()
import json
from logger import Logger
from slugify import slugify
from time import time
from markdown2 import Markdown
markdown = Markdown()

def convert_markdown(text: str) -> str:
	text = text.replace('\n', '\n\n')
	text = markdown.convert(text)
	text = text.replace('\n\n', '')
	return text

class Link:
	def __init__(self, name: str, url: str, id: str):
	 self.name = name
	 self.id = id
	 self.url = url
	
	@classmethod
	def compute_name(cls, url: str):
		# TODO: use a library
		# find & remove protocol (http, ftp, etc.) and get hostname
		if '//' in url:
			hostname = url.split('/')[2]
		else:
			hostname = url.split('/')[0]

		# find & remove port number
		hostname = hostname.split(':')[0]
		# find & remove "#"
		hostname = hostname.split('#')[0]
		# find & remove "?"
		hostname = hostname.split('?')[0]
		# find & remove "www."
		hostname = hostname.replace('www.', '')

		return hostname
	
	def as_dict(self) -> dict:
		return {
			'name': self.name,
			'id': self.id,
			'url': self.url,
		}
	
	@staticmethod
	def get_from_parsed_yaml(links) -> list:
		parsed_links = []
		if type(links) is list:
			for link in parsed_links:
				if type(link) is str:
					name = Link.compute_name(link)
					url = link
				else:
					name = link['name']
					url = link['url']
				parsed_links.append(Link(name=name, url=url, id=slugify(name)))
		else:
			for name, url in links.items():
				parsed_links.append(Link(name=name, url=url, id=slugify(name)))
		return parsed_links

class Collection:
	def __init__(
		self,
		id: str,
		name: str,
		description: str = "",
		links: Union[List[str], List[dict], dict] = []
	):
		self.name = name
		self.id = id
		self.links = Link.get_from_parsed_yaml(links)
		self.description = convert_markdown(description)
	def as_dict(self) -> dict:
		return {
			'name': self.name,
			'id': self.id,
			'links': [ link.as_dict() for link in self.links ],
			'description': self.description
		}
	 

class WorkSize:
	def __init__(self, height: int, width: int):
	 self.height = height
	 self.width = width
	 
	def aspect_ratio(self) -> Optional[float]:
		if self.height == 0:
			return None
		return self.height / self.width

class Work:
	def __init__(
		self,
		id: str,
		name: str,
		directory: str = None,
		year: int = None,
		description: str = "",
		front: str = None,
		size: WorkSize = WorkSize(0, 0),
		collection: Optional[Collection] = None,
		links: Union[List[str], List[dict], dict] = [],
		best: Optional[bool] = None,
		using: List[str] = [],
		wip: Optional[bool] = None,
		tags: List[str] = [],
		**other_attributes: dict
	):
		self.id = id
		self.name = name
		self.collection = collection
		self.best = best
		self.directory = directory or self.compute_directory()
		self.using = using
		self.tags = tags
		self.year = year
		self.description = convert_markdown(description)
		self.front = front or self.id
		self.front += '.png'
		self.size = size
		self.wip = wip or False
		self.links = Link.get_from_parsed_yaml(links)
		for attrname, value in other_attributes.items():
			setattr(self, attrname, value)
	
	def compute_directory(self) -> str:
		if self.collection is None:
			return self.id
		else:
			return os.path.join(self.collection.id, self.id)
	
	def as_dict(self) -> dict:
		return {
			'id': self.id,
			'name': self.name,
			'collection': None if self.collection is None else self.collection.as_dict(),
			'best': self.best,
			'directory': self.directory,
			'using': self.using,
			'tags': self.tags,
			'year': self.year,
			'description': self.description,
			'front': self.front,
			'links': [ ln.as_dict() for ln in self.links ],
			'size': {
				'height': self.size.height,
				'width': self.size.width,
				'aspect_ratio': self.size.aspect_ratio(),
			},
			'wip': self.wip,
		}

class WorkNotFound(Exception):
	pass
class CollectionNotFound(Exception):
	pass
class MultipleCollectionsFound(Exception):
	pass
class MultipleWorksFound(Exception):
	pass

class Database:
	def __init__(self, worksfile: str, collectionsfile: str):
		self.worksfile = worksfile
		self.collectionsfile = collectionsfile
		self.collections = list(self.get_collections())
		self.works = list(self)

	def __iter__(self):
		with open(self.worksfile, 'r') as file:
			works: List[dict] = yaml.load(file.read())
		for work in works:
			# Determine work.id or work.name
			if 'id' not in work.keys() and 'name' not in work.keys():
				raise KeyError(f'A work has neither a name nor an id.')
			if 'id' not in work.keys():
				work['id'] = slugify(work['name'])
			elif 'name' not in work.keys():
				work['name'] = work['id']
			# Instanciate
			bool_keys = ['best', 'wip']
			for key in bool_keys:
				if key in work.keys():
					work[key] = self._parse_yes_no(work[key])
			if 'collection' in work.keys() and work['collection'] is not None:
				work['collection'] = self.find_collection(id=work['collection'])
			else:
				work['collection'] = None
			work = Work(**work)
			yield work
		
	def get_collections(self):
		with open(self.collectionsfile, 'r') as file:
			collections: List[dict] = yaml.load(file.read())
		for collection in collections:
			# Instanciate the fuck
			yield Collection(**collection)
	
	def find_collection(self, **pred: dict) -> Collection:
		key, value = list(pred.items())[0]
		matching = [ w for w in self.collections if getattr(w, key) == value ]
		if not len(matching):
			raise CollectionNotFound(f'No collection with {key}={value!r} in the database')
		elif len(matching) > 1:
			raise MultipleCollectionsFound(f'Found {len(matching)} collections with {key}={value!r} in the database, expecting one.')
		else:
			return matching[0]
		
	@classmethod
	def _parse_yes_no(cls, value):
		truthy = ['yes', 'on', 'true']
		falsey = ['no', 'off', 'false']
		if value in truthy:
			return True
		if value in falsey:
			return False
		return None
	
	def edit(self, id: str, **modifications: dict) -> Work:
		modified = self._modify(id, modifications)
		for idx, id in enumerate(self.get_ids()):
			if modified.id == id:
				self.works[idx] = modified
		return modified
	
	def save(self, to: str):
		jsond = json.dumps(self._to_dicts_list(), ensure_ascii=False, indent=2)
		self.write(jsond, to)
	
	def write(self, content: str, to: str):
		with open(to, 'w') as file:
			file.write(content)
		
	def get_ids(self) -> List[str]:
		return [ w.id for w in self.works ]
	
	def find(self, **pred: dict) -> Work:
		key, value = list(pred.items())[0]
		matching = [ w for w in self.works if getattr(w, key) == value ]
		if not len(matching):
			raise WorkNotFound(f'No work with {key}={value!r} in the database')
		elif len(matching) > 1:
			raise MultipleWorksFound(f'Found {len(matching)} works with {key}={value!r} in the database, expecting one.')
		else:
			return matching[0]
	
	def _modify(self, id: str, modifications: dict) -> Work:
		work = self.find(id=id)
		for attrname, value in modifications.items():
			setattr(work, attrname, value)
		return work
	
	def _to_dicts_list(self) -> List[dict]:
		listd = []
		for w in self.works:
			listd.append(w.as_dict())
		return listd


def run():
	import datetime
	# 
	# Get infos
	#
	time_start = time()
	args = docopt(__doc__, version='0.1.0')
	fullpath = lambda *paths: os.path.join(os.path.abspath(args['--renders']), *paths)
	folders = os.listdir(args['--renders'])
	database = Database(args['--works'], args['--collections'])
	log = Logger(int(args['--verbose']))
	log.info('\n    Compiling {0} at {1}\n', args['--works'], datetime.datetime.now().strftime('%H:%M:%S'))
	#
	# Iterate
	#
	for work in database:
		# Get infos
		path = fullpath(work.directory, work.front)
		# Check if work.front file exists
		if not os.path.isfile(path):
			log.error('File {0} not found.', f'{work.collection.id if work.collection else ""}/{work.front}')
			database.edit(work.id, front=None)
			continue
		# Compute the work's size
		image = Image.open(path)
		width, height = image.size
		database.edit(work.id, size=WorkSize(height, width))
		# Make thumbnails
		thumbs_dir = os.path.join(args['--renders'], work.directory, 'thumbs')
		os.makedirs(thumbs_dir, exist_ok=True)
		for width in [500, 150, 20]:
			if work.size.aspect_ratio() is not None: continue
			thumb_path = os.path.join(thumbs_dir, str(width) + '.png')
			image.thumbnail((width, width))
			image.save(thumb_path)
		log.info('Made thumbnails for {0}', f'{work.collection.id if work.collection else ""}/{work.id}')
		
	#
	# Show infos
	#
	# Show number of untreated files
	#
	# I/O
	#
	# Write to .json
	works_output_path = args['--works'].replace('.yaml', '.json')
	database.save(to=works_output_path)
	log.info('\n    Saved works file to {0} in {1}\n', works_output_path, f'{time()-time_start:.3f}s')

if __name__ == "__main__":
	run()