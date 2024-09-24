# -*- coding: utf-8 -*-

import os
import re

from common.external_services.igdb.core.tags import (
    crew_patterns,
    suffixes,
    platform_patterns,
)
from common.trackers.trackers import ITTData
from dataclasses import dataclass, field
from common.mediainfo import MediaFile
from common.utility import title

# Get the name of the crew only if it's the last substring in the title by \b$
crew_pattern = r"\b(" + "|".join(pattern.replace(" ", "_") for pattern in crew_patterns) + r")\b$"

# Get the platform substr
tag_pattern = r"\b(" + "|".join(platform_patterns) + r")\b"


@dataclass
class Contents:
    """Create a new object with the attributes of Contents"""

    file_name: str
    folder: str
    name: str
    size: int
    metainfo: str
    category: int
    tracker_name: str
    torrent_pack: bool
    torrent_path: str
    display_name: str
    doc_description: str
    audio_languages: list[str]
    episode_title: str = field(init=False)
    resolution: int = field(init=False)
    game_title: str
    game_crew: list
    game_tags: list

    def __post_init__(self):
        # Search for the episode title
        guess_filename = title.Guessit(self.file_name)
        self.episode_title = guess_filename.guessit_episode_title
        if self.episode_title:
            self.display_name = " ".join(
                self.display_name.replace(self.episode_title, "").split()
            )

        # Search for resolution based on mediainfo string
        tracker_data = ITTData.load_from_module()
        file_path = os.path.join(self.folder, self.file_name)
        media_file = MediaFile(file_path)
        video_height = f"{media_file.video_height}p"
        if video_height not in tracker_data.resolution:
            self.resolution = tracker_data.resolution["altro"]
        else:
            self.resolution = tracker_data.resolution[video_height]


@dataclass
class Media:
    """
    For each Folder, create an object with attributes:
    folder, subfolder, media_type, other, audio_codec, subtitle, resolution
    """

    folder: str
    subfolder: str

    @property
    def guess_filename(self):
        temp_name = os.path.basename(self.subfolder)

        temp_name = temp_name.replace(".", " ")
        # temp_name = temp_name.replace("_", " ")
        temp_name = temp_name.replace("-", " ")

        for crew_name in self.crew:
            temp_name = temp_name.replace(crew_name, "")

        for tag_name in self.game_tags:
            temp_name = temp_name.replace(tag_name, "")

        for suffix in suffixes:
            temp_name = temp_name.lower().replace(suffix.lower(), "")
        return title.Guessit(temp_name.strip())

    @property
    def source(self):
        return self.guess_filename.source

    @property
    def other(self):
        return self.guess_filename.other

    @property
    def audio_codec(self):
        return self.guess_filename.audio_codec

    @property
    def subtitle(self):
        return self.guess_filename.subtitle

    @property
    def resolution(self):
        return self.guess_filename.screen_size

    @property
    def torrent_path(self) -> str:
        return os.path.join(self.folder, self.subfolder)

    @property
    def crew(self) -> list:
        temp_name = self.subfolder.replace(".", " ").strip()
        matches = re.findall(crew_pattern, temp_name, re.IGNORECASE)
        return matches

    @property
    def game_tags(self) -> list:
        matches = re.findall(tag_pattern, self.subfolder, re.IGNORECASE)
        return matches

    @property
    def media_type(self):

        tracker_data = ITTData.load_from_module()
        movie_category = tracker_data.category.get("movie")
        serie_category = tracker_data.category.get("tvshow")
        game_category = tracker_data.category.get("game")

        if self.guess_filename.guessit_season:
            media_type = serie_category
        else:
            media_type = movie_category
        if self.crew:
            media_type = game_category
        return media_type

    @property
    def game_title(self):
        return self.guess_filename.guessit_title
