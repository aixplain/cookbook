from aixplain.enums import Function, Supplier
from aixplain.modules.agent.tool.model_tool import ModelTool

# Default LLM model for the agent
DEFAULT_LLM_ID = "6646261c6eb563165658bbb1"  # GPT-4

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Tool configurations
TOOL_CONFIGS = {
    "speech_synthesis": {
        "function": Function.SPEECH_SYNTHESIS,
        "supplier": Supplier.GOOGLE
    },
    "translation": {
        "function": Function.TRANSLATION,
        "supplier": Supplier.MICROSOFT
    },
    "speech_recognition": {
        "function": Function.SPEECH_RECOGNITION
    }
}

def create_tool(tool_name: str, **kwargs) -> ModelTool:
    """Create a ModelTool with the specified configuration."""
    config = TOOL_CONFIGS.get(tool_name, {})
    config.update(kwargs)
    return ModelTool(**config) 