from typing import Annotated

import spotipy
import typer
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from spotipy.oauth2 import SpotifyOAuth

from .agent import agent
from .config import get_settings
from .deps import Deps

app = typer.Typer(add_completion=False)


@app.command()
def main(
    model: Annotated[
        str | None,
        typer.Option(
            "--model",
            "-m",
            help="Override the default Ollama model used for the agent. If not provided, the default model from the configuration (.env file) will be used.",
        ),
    ] = None,
) -> None:
    """Run the interactive chat with the spoti-agent."""

    settings = get_settings()

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
            redirect_uri=settings.spotify_redirect_uri,
            scope="user-modify-playback-state user-read-playback-state "
            "user-library-modify user-library-read",
        )
    )
    deps = Deps(spotify=sp)

    model_override = None
    if model is not None:
        model_override = OllamaModel(
            model, provider=OllamaProvider(base_url=settings.ollama_base_url)
        )

    agent.to_cli_sync(deps=deps, prog_name="spoti-agent", model=model_override)


if __name__ == "__main__":
    app()
