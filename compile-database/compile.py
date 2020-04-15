#!/usr/bin/env python3
"""A compiler for works.yaml file for my portfolio

Usage:
  swdbc [options]
  swdbc (-h|--help|--version)

Files & directories options
--works=<file>         The works YAML file [default: ../static/works.yaml]
--renders=<directory>  The directory where renders are stored [default: ../static/works]
--collections=<file>   The collections YAML file [default: ../static/collections.yaml]
--watch                Auto-recompile when one of the YAML files or contents of the renders directory changes.
--rate=<ms>            Sets the refresh rate for the watch option. [default: 1000]
--regen-thumbs         Regenerate thumbnails even if they already exist.
--regen-colors         Recalculate colors even if they already exist.
-o, --output=<file>    The output file. Defaults to --works with the extension changed to .json

Miscellaneous options
--verbose=<level>      The verbosity level, 0 to quiet [default: 2]
"""
import os, shutil
from os.path import splitext
from typing import List, Dict, Optional, Union
from docopt import docopt
from PIL import Image
import pastel
import yaml
import subprocess

import json
from logger import Logger
from slugify import slugify
from time import time, sleep
from markdown2 import Markdown
import pdf2image

markdown = Markdown()
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorthief import ColorThief


def convert_markdown(text: str) -> Optional[str]:
    if not text:
        return None
    text = text.replace("\n", "\n\n")
    text = markdown.convert(text)
    text = text.replace("\n\n", "")
    return text


def get_dominant_color(filepath: str) -> str:
    thief = ColorThief(filepath)
    return thief.get_color(quality=1)


class WorkImage:
    def __init__(self, file: str, label: Optional[str] = None) -> None:
        self.file = file
        self.label = label
    
    def as_dict(self) -> dict:
        return {
            'label': self.label,
            'file': self.file
        }
    
    @staticmethod
    def compute_label(filename: str) -> str:
        return splitext(filename)[0].replace('-', ' ').title()
    
    @classmethod
    def get_from_parsed_yaml(cls, images: Union[List[str], List[dict], dict]) -> 'List[WorkImage]':
        typ = type(images)
        parsed = []
        if typ is list:
            for image in images:
                if type(image) is str:
                    file = image
                    label = cls.compute_label(image)
                elif type(image) is dict:
                    file = image['file']
                    label = image.get('label', cls.compute_label(file))
                else:
                    raise TypeError("Images must be one of List[str], List[dict], dict")
                parsed.append(cls(file, label))
                    
        elif typ is dict:
            for file, label in images.items():
                parsed.append(cls(file, label))
        return parsed
        

class Link:
    def __init__(self, name: str, url: str, id: str):
        self.name = name
        self.id = id
        self.url = url

    @classmethod
    def compute_name(cls, url: str):
        # TODO: use a library
        # find & remove protocol (http, ftp, etc.) and get hostname
        if "//" in url:
            hostname = url.split("/")[2]
        else:
            hostname = url.split("/")[0]

        # find & remove port number
        hostname = hostname.split(":")[0]
        # find & remove "#"
        hostname = hostname.split("#")[0]
        # find & remove "?"
        hostname = hostname.split("?")[0]
        # find & remove "www."
        hostname = hostname.replace("www.", "")

        return hostname

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "url": self.url,
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
                    name = link["name"]
                    url = link["url"]
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
        links: Union[List[str], List[dict], dict] = [],
    ):
        self.name = str(name)
        self.id = str(id)
        self.links = Link.get_from_parsed_yaml(links)
        self.description = convert_markdown(description)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "links": [link.as_dict() for link in self.links],
            "description": self.description,
        }


class WorkSize:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def aspect_ratio(self) -> Optional[float]:
        if self.height == 0:
            return None
        return self.height / self.width
        
class YoutubeProperties:
    """IDs for YouTube playlist and/or video"""
    def __init__(self, playlist: Optional[str] = None, video: Optional[str] = None) -> None:
        self.playlist = playlist
        self.video = video
    
    def as_dict(self):
        return {
            'playlist': self.playlist,
            'video': self.video
        }


class Work:
    def __init__(
        self,
        id: str,
        name: str,
        directory: str = None,
        year: int = None,
        description: str = "",
        front: str = None,
        color: str = None,
        size: WorkSize = WorkSize(0, 0),
        collection: Optional[Collection] = None,
        links: Union[List[str], List[dict], dict] = [],
        best: Optional[bool] = None,
        using: List[str] = [],
        wip: Optional[bool] = None,
        tags: List[str] = [],
        images: Union[List[str], List[dict], dict] = [],
        youtube: YoutubeProperties = YoutubeProperties(),
        **other_attributes: dict,
    ):
        self.id = str(id)
        self.collection = collection
        self.full_id = (self.collection.id + "/" if self.collection else "") + self.id
        self.name = str(name)
        self.best = best
        self.directory = directory or self.compute_directory()
        self.using = using
        self.tags = tags
        self.year = year
        self.description = convert_markdown(description)
        self.front = front or self.id
        self.front = str(self.front)
        self.front += ".png"
        self.size = size
        self.wip = wip or False
        self.links = Link.get_from_parsed_yaml(links)
        self.images = WorkImage.get_from_parsed_yaml(images)
        self.color = color
        self.youtube = youtube
        for attrname, value in other_attributes.items():
            setattr(self, attrname, value)

    def compute_directory(self) -> str:
        if self.collection is None:
            return self.id
        else:
            return os.path.join(self.collection.id, self.id)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "full_id": self.full_id,
            "name": self.name,
            "collection": None
            if self.collection is None
            else self.collection.as_dict(),
            "best": self.best,
            "directory": self.directory,
            "using": self.using,
            "tags": self.tags,
            "year": self.year,
            "description": self.description,
            "front": self.front,
            "links": [ln.as_dict() for ln in self.links],
            "size": {
                "height": self.size.height,
                "width": self.size.width,
                "aspect_ratio": self.size.aspect_ratio(),
            },
            "wip": self.wip,
            "color": self.color,
            "youtube": self.youtube.as_dict(),
            "images": [im.as_dict() for im in self.images]
        }


class WorkNotFound(Exception):
    pass


class CollectionNotFound(Exception):
    pass


class MultipleCollectionsFound(Exception):
    pass


class MultipleWorksFound(Exception):
    pass


class ValidationError(Exception):
    pass


class Database:
    def __init__(self, worksfile: str, collectionsfile: str, logger: Logger):
        self.logger = logger
        self.worksfile = worksfile
        self.collectionsfile = collectionsfile
        self.collections = list(self.get_collections())
        self.works = list(self)
        self.validate()

    def __iter__(self):
        with open(self.worksfile, "r") as file:
            works: List[dict] = yaml.load(file.read(), Loader=yaml.SafeLoader)
        for work in works:
            # Determine work.id or work.name
            if "id" not in work.keys() and "name" not in work.keys():
                raise KeyError(f"A work must have either a name or an id.")
            if "id" not in work.keys():
                work["id"] = slugify(str(work["name"]))
            elif "name" not in work.keys():
                work["name"] = work["id"]
            # Instanciate
            # bool_keys = ["best", "wip"]
            # for key in bool_keys:
            #     if key in work.keys():
            #         work[key] = self._parse_yes_no(work[key])
            if "collection" in work.keys() and work["collection"] is not None:
                work["collection"] = self.find_collection(id=work["collection"])
            else:
                work["collection"] = None
            if "youtube" in work.keys():
                work["youtube"] = YoutubeProperties(**work["youtube"])
            work = Work(**work)
            yield work

    def get_collections(self):
        with open(self.collectionsfile, "r") as file:
            collections: List[dict] = yaml.load(file.read(), Loader=yaml.SafeLoader)
        if collections is None:
            return []
        for collection in collections:
            # Instanciate
            yield Collection(**collection)

    def validate_works(self):
        """
		Checks to see if there are no duplicate IDs
		"""
        # We'll build up a ID list and check every time if the ID is not already in it.
        ids = []
        for work in self:
            if work.full_id in ids:
                self.logger.debug(
                    "Checking for {0!r}", json.dumps(work, indent=2, ensure_ascii=False)
                )
                raise ValidationError(
                    f"At least 2 works have the same id {work.full_id!r}"
                )
            else:
                ids.append(work.full_id)

    def validate_collections(self):
        """
		Checks to see if there are no duplicate IDs
		"""
        # We'll build up a ID list and check every time if the ID is not already in it.
        ids = []
        for collection in self.collections:
            if collection.id in ids:
                raise ValidationError(
                    f"At least 2 collections have the same id {collection.id!r}"
                )
            else:
                ids.append(collection.id)

    def validate(self):
        """
		Checks to see if there are no duplicate IDs, in both works and collections
		"""
        self.validate_works()
        self.validate_collections()

    def find_collection(self, **pred: dict) -> Collection:
        key, value = list(pred.items())[0]
        matching = [w for w in self.collections if getattr(w, key) == value]
        #TODO #33(@ewen-lbh): list all missing collections @ the end
        if not len(matching):
            raise CollectionNotFound(
                f"No collection with {key}={value!r} in the database"
            )
        elif len(matching) > 1:
            raise MultipleCollectionsFound(
                f"Found {len(matching)} collections with {key}={value!r} in the database, expecting one."
            )
        else:
            return matching[0]

    def edit(self, full_id: str, **modifications) -> Work:
        modified = self._modify(full_id, modifications)
        for idx, id in enumerate([w.full_id for w in self.works]):
            if modified.full_id == id:
                self.works[idx] = modified
        return modified

    def save(self, to: str):
        jsond = json.dumps(self._to_dicts_list(), ensure_ascii=False, indent=2)
        self.write(jsond, to)

    def write(self, content: str, to: str):
        with open(to, "w") as file:
            file.write(content)

    def get_ids(self) -> List[str]:
        return [w.id for w in self.works]

    def find(self, **pred) -> Work:
        key, value = list(pred.items())[0]
        matching = [w for w in self.works if getattr(w, key) == value]
        if not len(matching):
            raise WorkNotFound(f"No work with {key}={value!r} in the database")
        elif len(matching) > 1:
            raise MultipleWorksFound(
                f"Found {len(matching)} works with {key}={value!r} in the database, expecting one."
            )
        else:
            return matching[0]

    def _modify(self, full_id: str, modifications: dict) -> Work:
        work = self.find(full_id=full_id)
        for attrname, value in modifications.items():
            setattr(work, attrname, value)
        return work

    def _to_dicts_list(self) -> List[dict]:
        listd = []
        for w in self.works:
            listd.append(w.as_dict())
        return listd


def doit(args, log):
    import datetime

    #
    # Get infos
    #
    time_start = time()
    fullpath = lambda *paths: os.path.join(os.path.abspath(args["--renders"]), *paths)
    database = Database(args["--works"], args["--collections"], logger=log)
    log.info(
        "\n    Compiling {0} at {1}\n",
        args["--works"],
        datetime.datetime.now().strftime("%H:%M:%S"),
    )
    #
    # Iterate
    #
    for work in database:
        log.debug(
            "Working on work {0}:\n {1}",
            work.name,
            json.dumps(
                {k: v for k, v in work.as_dict().items() if k != "description"},
                ensure_ascii=False,
            ),
        )
        # Get infos
        path = fullpath(work.directory, work.front)
        path_disp = f'{work.collection.id if work.collection else ""}/{work.front}'
        # Check if work.front file exists
        if not os.path.isfile(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            video_path = path.replace(".png", ".mp4")
            pdf_path = path.replace(".png", ".pdf")
            if os.path.isfile(pdf_path):
                log.warn(
                    "File {0} not found, but {1} was found: converting the PDF to a PNG...",
                    path_disp,
                    path_disp.replace(".png", ".pdf"),
                )
                try:
                    pages = pdf2image.convert_from_path(pdf_path)
                    pages[0].save(
                        path
                    )  # TODO: choose the front page num. from works.yaml, instead of always #1
                    if len(pages) > 1:
                        for i, page in enumerate(pages):
                            log.success("  Converted page {0} successfully", f"#{i+1}")
                            page.save(path.replace(".png", f"--page-{i}.png"))
                except Exception:
                    log.error(
                        "An error occured during the conversion of {0} to a PNG",
                        path_disp.replace(".png", ".pdf"),
                    )
                    database.edit(work.full_id, front=None)
            elif os.path.isfile(video_path):
                log.warn(
                    "File {0} not found, but {1} was found: making a 5-second GIF...",
                    path_disp,
                    path_disp.replace(".png", ".mp4"),
                )
                try:
                    gif_path = path.replace(".png", ".gif")
                    subprocess.run(['./gifcurry-linux-6.0.0.0/bin/gifcurry_cli', f'-i={video_path}', f'-o={gif_path}', '-s 0','-e 5'], capture_output=True)
                    database.edit(
                        work.full_id, front=work.front.replace(".png", ".gif")
                    )
                except Exception as error:
                    from pprint import pformat
                    log.error(
                        "An error occured during the conversion of {0} to a GIF: {1}",
                        path_disp.replace(".png", ".mp4"), pformat(error)
                    )
                    database.edit(work.full_id, front=None)
            else:
                log.error("File {0} not found.", path_disp)
                database.edit(work.full_id, front=None)
            continue
        # Compute the work's size
        image = Image.open(path)
        width, height = image.size
        database.edit(work.full_id, size=WorkSize(height, width))
        # Make thumbnails
        thumbs_dir = os.path.join(args["--renders"], work.directory, "thumbs")
        os.makedirs(thumbs_dir, exist_ok=True)
        thumbnail_created_count = 0
        for width in [500, 150, 20]:
            if work.size.aspect_ratio() is not None:
                continue
            thumb_path = os.path.join(thumbs_dir, str(width) + ".png")
            if args['--regen-thumbs'] or not os.path.isfile(thumb_path):
                image.thumbnail((width, width))
                image.save(thumb_path)
                thumbnail_created_count += 1
        if thumbnail_created_count:
            log.info("Made {1} thumbnail(s) for {0}", work.full_id, thumbnail_created_count)
        # Compute the dominant color if not set explicitly
        # We use the thumbnail so it's less intensive.
        if not work.color:
            # Try to get the color from the last compiled works.json
            color_of_last_compiled = None
            last_compiled_filepath = os.path.join(os.path.dirname(args['--works']), 'works.json')
            if os.path.isfile(last_compiled_filepath):
                with open(last_compiled_filepath, 'r') as file:
                    last_compiled = json.loads(file.read())
                for last_compiled_work in last_compiled:
                    if 'color' in last_compiled_work.keys() and last_compiled_work['full_id'] == work.full_id:
                        color_of_last_compiled = last_compiled_work['color']
            
            if color_of_last_compiled is None or args['--regen-colors']:
                r, g, b = get_dominant_color(os.path.join(thumbs_dir, "500.png"))
                work_color = f"rgb({r},{g},{b})"
                from colr import Colr
                log.info(
                    f"Got the dominant color for {{0}}: {Colr().rgb(r, g, b, '█' * 10)}",
                    work.full_id,
                )
            
            else:
                work_color = color_of_last_compiled
            
            database.edit(work.full_id, color=work_color)

    #
    # Show infos
    #
    # Show number of untreated files
    #
    # I/O
    #
    # Write to .json
    works_output_path = args['--output'] or args["--works"].replace(".yaml", ".json")
    database.save(to=works_output_path)
    log.info(
        "\n    Saved works file to {0} in {1}\n",
        works_output_path,
        f"{time()-time_start:.3f}s",
    )


def run():
    args = docopt(__doc__, version="0.1.0")
    log = Logger(int(args["--verbose"]))
    doit(args, log)
    if args["--watch"]:
        watched_dir = os.path.dirname(args["--works"])
        log.info(
            "Watching for changes in {0}... (Press {1} to stop)", watched_dir, "Ctrl-C"
        )

        class WatchEventHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                super(WatchEventHandler, self).on_any_event(event)
                if event.src_path.endswith(".yaml") or event.src_path.endswith('.png'):
                    log.info("Detected changes in {0}", event.src_path)
                    doit(args, log)
                    log.info(
                        "Watching for changes in {0}... (Press {1} to stop)",
                        watched_dir,
                        "Ctrl-C",
                    )

        observer = Observer()
        observer.schedule(WatchEventHandler(), watched_dir)
        observer.start()
        try:
            while True:
                sleep(int(args["--rate"]))
        except KeyboardInterrupt:
            observer.stop()


if __name__ == "__main__":
    run()

