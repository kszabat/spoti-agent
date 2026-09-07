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
        "check using the tools (e.g., search)"
    ),
)

# Register the Spotify tools with the agent
from .tools import spotify_tools  # noqa: F401
