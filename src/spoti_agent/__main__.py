import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .agent import agent
from .config import get_settings
from .deps import Deps


def main() -> None:
    settings = get_settings()
    scope = "user-modify-playback-state user-read-playback-state user-library-modify user-library-read"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
            redirect_uri=settings.spotify_redirect_uri,
            scope=scope,
        )
    )
    deps = Deps(spotify=sp)

    print("Welcome to the Spotify Agent! Type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = agent.run_sync(user_prompt=user_input, deps=deps)
        print(f"Agent: {result.output}")


if __name__ == "__main__":
    main()
