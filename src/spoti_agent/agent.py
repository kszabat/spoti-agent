from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from .config import get_settings
from .deps import Deps

settings = get_settings()

model = OllamaModel(
    settings.ollama_model, provider=OllamaProvider(settings.ollama_base_url)
)

agent = Agent(
    model,
    deps_type=Deps,
    tools=[duckduckgo_search_tool()],
    instructions=(
        "You are a helpful assistant that can control Spotify playback and answer questions about tracks, albums, and artists; "
        "You can also provide information about the current playback state and the user's library;"
        "Fulfil the user's requests by using the provided tools and information - do not guess or make up information; "
        "check using the tools (e.g., search). Use web search (duckduckgo_search_tool) only when you need information from outside of Spotify or when the user asks for information that is not available in Spotify, for example, when user does not know the exact name of a track or artist and wants to find it or when the user remembers only a part of the lyrics and wants to find the track. If needed, you can use retrieved information to answer the user's question or provide it to other tools (for example: search_tracks or play_song_by_name)."
    ),
)

# Register the Spotify tools with the agent
from .tools import spotify_tools  # noqa: F401
