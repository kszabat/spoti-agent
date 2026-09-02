import spotipy
from dataclasses import dataclass


@dataclass
class Deps:
    spotify: spotipy.Spotify


d = Deps()