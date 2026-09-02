from __future__ import annotations

import spotipy
from pydantic_ai import RunContext

from ..agent import agent
from ..deps import Deps


def _get_playback_device_id(sp: spotipy.Spotify) -> str | None:
    devices = sp.devices().get("devices", [])

    if not devices:
        return None

    for d in devices:
        if d.get("is_active"):
            return d.get("id")

    return devices[0].get("id")


@agent.tool
def search_tracks(ctx: RunContext[Deps], query: str, limit: int = 5) -> str:
    """Search for tracks on Spotify.
    Use this tool when you need to find specific tracks to play or provide information about.

    Args:
        query: The user's search query, e.g., "Diamond Eyes by Deftones"
        limit: The maximum number of tracks to return (default is 5)
    """

    results = ctx.deps.spotify.search(
        q=query, type="track", limit=limit
    )

    found_tracks = results.get("tracks", {}).get("items", [])

    if not found_tracks:
        return f"No tracks found for the query: {query!r}"

    track_info_list: list[str] = []
    for track in found_tracks:
        track_name = track.get("name")
        artists = ", ".join(artist.get("name") for artist in track.get("artists", []))
        uri = track.get("uri")

        track_info_list.append(f"- {track_name} by {artists} (URI: {uri})")

    answer = f"Found {len(found_tracks)} track(s) for the query: {query!r}\n\n"
    answer += "\n".join(track_info_list)

    return answer