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

    results = ctx.deps.spotify.search(q=query, type="track", limit=limit)

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


@agent.tool
def play_track(ctx: RunContext[Deps], track_uri: str) -> str:
    """Play a specific track on Spotify.
    Use this tool when you want to play a specific track by its URI.
    Usually, you would first search for the track using the `search_tracks` tool and then use this tool to play it.

    Args:
        track_uri: The Spotify URI of the track to play, e.g. spotify:track:6nmDEbjMZru5j55HIkX2yZ
    """

    sp = ctx.deps.spotify
    device_id = _get_playback_device_id(sp)

    if not device_id:
        return "No active playback device found. Please ensure you have a Spotify client open and logged in."

    try:
        sp.start_playback(device_id=device_id, uris=[track_uri])
    except spotipy.SpotifyException as e:
        return f"Failed to start playback: {e}"

    return f"Playback started for track URI: {track_uri}"


@agent.tool
def play_song_by_name(ctx: RunContext[Deps], song_name: str):
    """Search for a song by name and play best match right away.
    This tool combines searching and playing a song in one step.
    Use this tool when user asks to play a song by name, e.g., "Play 'Diamond Eyes' by Deftones" and you don't need to choose from multiple search results.

    Args:
        song_name: The name of the song to search and play, e.g., "Diamond Eyes by Deftones"
    """

    sp = ctx.deps.spotify
    results = sp.search(q=song_name, type="track", limit=1)
    track = results.get("tracks", {}).get("items", [None])[0]

    if not track:
        return f"No tracks found for the query: {song_name!r}"

    device_id = _get_playback_device_id(sp)
    if not device_id:
        return "No active playback device found. Please ensure you have a Spotify client open and logged in."

    try:
        sp.start_playback(device_id=device_id, uris=[track["uri"]])
    except spotipy.SpotifyException as e:
        return f"Failed to start playback: {e}"

    artists = ", ".join(artist.get("name") for artist in track.get("artists", []))
    answer = f"Playback started for '{track.get('name')}' by {artists})"

    return answer


@agent.tool
def pause_playback(ctx: RunContext[Deps]) -> str:
    """Pause the current playback on Spotify.
    Use this tool when you want to pause the currently playing track.

    Returns:
        A message indicating whether the playback was successfully paused or if there was an error.
    """

    sp = ctx.deps.spotify
    device_id = _get_playback_device_id(sp)

    if not device_id:
        return "No active playback device found. Please ensure you have a Spotify client open and logged in."

    try:
        sp.pause_playback(device_id=device_id)
    except spotipy.SpotifyException as e:
        return f"Failed to pause playback: {e}"

    return "Playback paused successfully."


@agent.tool
def resume_playback(ctx: RunContext[Deps]) -> str:
    """Resume the current playback on Spotify.
    Use this tool when you want to resume the currently paused track.

    Returns:
        A message indicating whether the playback was successfully resumed or if there was an error.
    """

    sp = ctx.deps.spotify
    device_id = _get_playback_device_id(sp)

    if not device_id:
        return "No active playback device found. Please ensure you have a Spotify client open and logged in."

    try:
        sp.start_playback(device_id=device_id)
    except spotipy.SpotifyException as e:
        return f"Failed to resume playback: {e}"

    return "Playback resumed successfully."


@agent.tool
def get_current_playback(ctx: RunContext[Deps]) -> str:
    """Get information about the current playback on Spotify.
    Use this tool when you want to know what track is currently playing, along with its details.

    Returns:
        A message containing information about the currently playing track or indicating that nothing is playing.
    """

    sp = ctx.deps.spotify
    playback_info = sp.current_playback()

    if (
        not playback_info
        or not playback_info.get("is_playing")
        or not playback_info.get("item")
    ):
        return "No track is currently playing."

    track = playback_info.get("item")
    track_name = track.get("name")
    artists = ", ".join(artist.get("name") for artist in track.get("artists", []))
    album = track.get("album", {}).get("name")

    answer = f"Currently playing: '{track_name}' by {artists} from the album '{album}'."

    return answer


@agent.tool
def add_current_track_to_favurites(ctx: RunContext[Deps]):
    """Add the currently playing track to the user's Spotify favorites (liked songs).
    Use this tool when you want to like the currently playing track.

    Returns:
        A message indicating whether the track was successfully added to favorites or if there was an error.
    """

    sp = ctx.deps.spotify
    playback_info = sp.current_playback()

    if not playback_info or not playback_info.get("item"):
        return "No track is currently playing."

    track = playback_info.get("item")
    track_id = track.get("id")

    if not track_id:
        return "Failed to retrieve the current track's ID."

    try:
        sp.current_user_saved_tracks_add([track_id])
    except spotipy.SpotifyException as e:
        return f"Failed to add the current track to favorites: {e}"

    return f"'{track.get('name')}' by {', '.join(artist.get('name') for artist in track.get('artists', []))} has been added to your favorites."
