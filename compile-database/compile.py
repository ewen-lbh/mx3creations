"""A compiler for works.yaml file for my portfolio

Usage:
  swdbc [--renders ASSETS-DIR] [--works WORKS-FILE]
  swdbc (-h|--help)
	
Options:
  -w --works WORKS-FILE    The YAML file where all the works are stored [default: works.yaml]
  -d --renders ASSETS-DIR  The directory where all of the work's renders are. [default: ./works]
  -h --help                Show this help
"""
import os
from typing import List, Dict, Optional, Union
from docopt import docopt
from PIL import Image
import pastel
from ruamel.yaml import YAML
yaml = YAML()
from slugify import slugify

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
		collection: Optional[str] = [],
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
		self.directory = directory or self.id
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

class WorkNotFound(Exception):
	pass
class MultipleWorksFound(Exception):
	pass

class Database:
	def __init__(self, path: str):
		self.path = path
		self.works = list(self.iterate())

	def iterate(self):
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


def run():
	args = docopt(__doc__)
	fullpath = lambda *paths: os.path.join(os.path.abspath(args['--renders']), *paths)
	folders = os.listdir(args['--renders'])
	database = Database(args['--works'])
	for folder in folders:
		if folder not in database.get_ids():
			print(pastel.colorize(f"<comment>Skipping directory <options=bold;fg=red>{folder}</options=bold;fg=red></comment>"))
			continue
		work = database.find(id=folder)
		path = fullpath(work.directory, work.front)
		if not os.path.isfile(path):
			print(pastel.colorize(f"<fg=red>File <options=bold;fg=red>{work.front}</options=bold;fg=red> not found</fg=red>"))
			continue
		image = Image.open(path)
		width, height = image.size
		database.edit(work.id, size=WorkSize(height, width))
		print(work.size.aspect_ratio())
if __name__ == "__main__":
	run()
