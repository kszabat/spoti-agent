## Setup

1. Copy `.env.example` to `.env`:

```bash
   cp .env.example .env
```
2. Create a Spotify application at [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) to get your **Client ID** and **Client Secret**.
3. Create a Gemini API key at [aistudio.google.com](https://aistudio.google.com/).
4. Fill in the values in `.env` file with the values ​​obtained in the previous two steps.

## Installation
1. Download and install `uv` [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/)
2. From the root of the repository, install the project as a global `uv` tool:

```bash
uv tool install --editable .
```

This makes the `spoti-agent` command available anywhere on your system.

3. Restart your terminal.
4. Run the app using the `spoti-agent` command.

## Features

- **Search for tracks** -- find tracks matching a query
- **Play a song by name** -- search and start playback in one step
- **Play a specific track** --  start playback for a track by its Spotify URI
- **Pause / resume playback** -- control the currently playing track
- **Check what's playing** -- get the name, artist, and album of the currently playing track
- **Like the current track** -- add the currently playing song to your Spotify favorites (Liked Songs)
