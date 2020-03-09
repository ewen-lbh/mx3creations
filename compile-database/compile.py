#!/usr/bin/env python3
"""A compiler for works.yaml file for my portfolio

Usage:
  swdbc [--renders ASSETS-DIR] [--works WORKS-FILE] [--collections COLLECTIONS-FILE] [--thumbs RESOLUTIONS]
  swdbc (-h|--help)
	
Options:
  -w --works WORKS-FILE              The YAML file where all the works are stored [default: works.yaml]
  -d --renders ASSETS-DIR            The directory where all of the work's renders are. [default: ./works]
	-c --collections COLLECTIONS-FILE  The YAML file where all the collections are stored [default: collections.yaml]
	-s --sites SITES-FILE              The YAML file where all the links to external sites are stored. [default: sites.yaml]
	-t --thumbs RESOLUTIONS            A comma-separated list of resolution for thumbnails [default: 20,250,500]
  -h --help                          Show this help
"""
import os, shutil
from typing import List, Dict, Optional, Union
from docopt import docopt
from PIL import Image
import pastel
from ruamel.yaml import YAML
yaml = YAML()
import json
from slugify import slugify

class Link:
	def __init__(self, name: str, url: str, id: str):
	 self.name = name
	 self.id = id
	 self.url = url
	
	@classmethod
	def create(cls, link: Union[str, dict, tuple]):
		if type(link) is tuple:
			return cls(name=link[0], url=link[1], id=slugify(link[0]))
		if tuple(link) is dict:
			return cls(**link)
		if tuple(link) is str:
			name = cls.compute_name(link)
			return cls(name=name, url=link, id=slugify(name))
	
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
		
		

class Collection:
	def __init__(self, id: str, name: str, learn_more: List[Link]):
	 self.name = name
	 self.id = id
	 

class WorkSize:
	def __init__(self, height: int, width: int):
	 self.height = height
	 self.width = width
	 
	def aspect_ratio(self) -> float:
		if self.height == 0:
			return None
		return self.width / self.height

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
		collection: Optional[str] = None,
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
		self.description = description
		self.front = front or self.id
		self.front += '.png'
		self.size = size
		self.wip = wip or False
		for attrname, value in other_attributes.items():
			setattr(self, attrname, value)
			
	def compute_directory(self) -> str:
		if self.collection is None:
			return self.id
		else:
			return os.path.join(self.collection, self.id)
	
	def as_dict(self) -> dict:
		return {
			'id': self.id,
			'name': self.name,
			'collection': self.collection,
			'best': self.best,
			'directory': self.directory,
			'using': self.using,
			'tags': self.tags,
			'year': self.year,
			'description': self.description,
			'front': self.front,
			'front': self.front,
			'size': {
				'height': self.size.height,
				'width': self.size.width,
				'aspect_ratio': self.size.aspect_ratio(),
			},
			'wip': self.wip,
		}

class WorkNotFound(Exception):
	pass
class MultipleWorksFound(Exception):
	pass

class Database:
	def __init__(self, path: str):
		self.path = path
		self.works = list(self)

	def __iter__(self):
		with open(self.path, 'r') as file:
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
			work = Work(**work)
			yield work
	
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
	args = docopt(__doc__)
	fullpath = lambda *paths: os.path.join(os.path.abspath(args['--renders']), *paths)
	folders = os.listdir(args['--renders'])
	database = Database(args['--works'])
	print(pastel.colorize(f'\n<info>    Compiling at {datetime.datetime.now().isoformat(sep=" ")}</info>\n'))
	#
	# Iterate
	#
	for work in database:
		# Get infos
		path = fullpath(work.directory, work.front)
		# Check if work.front file exists
		if not os.path.isfile(path):
			print(pastel.colorize(f"<fg=red>File <fg=white>{work.collection or ''}/{work.front}</fg=white> not found</fg=red>"))
			continue
		# Compute the work's size
		image = Image.open(path)
		width, height = image.size
		database.edit(work.id, size=WorkSize(height, width))
		# Make thumbnails
		thumbs_dir = os.path.join(args['--renders'], work.directory, 'thumbs')
		shutil.rmtree(thumbs_dir)
		os.makedirs(thumbs_dir, exist_ok=True)
		for width in [500, 150, 20]:
			thumb_path = os.path.join(thumbs_dir, str(width) + '.png')
			thumb = Image.open(path)
			thumb.resize((width, width))
			thumb.save(thumb_path)
		print(pastel.colorize(f'<info>Made thumbnails for {work.collection or ""}/{work.id}</info>'))
		
		
	#
	# Show infos
	#
	# Show number of untreated files
	#
	# I/O
	#
	# Write to .json
	database.save(to=args['--works'].replace('.yaml', '.json'))

if __name__ == "__main__":
	run()
