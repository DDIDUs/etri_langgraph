import re
from typing import Any, List, Optional, Dict

from etri_langgraph.utils.registry import node_registry, BaseNode


@node_registry(name="parser")
class JsonParser(BaseNode):
    def __init__(
        self,
        key: str,
        examples: Optional[dict] = None,
        **kwargs,
    ):
        self.key = key
        self.examples = examples
        self.kwargs = kwargs

    def preprocess(self, text: str) -> str:
        code_block_pattern = r"```[a-z]*\n(.*?)```"
        matches = re.findall(code_block_pattern, text, re.DOTALL)

        if matches:
            return matches[-1]
        
        incomplete_pattern = r"```[a-z]*\n(.*?)$"
        fallback_matches = re.findall(incomplete_pattern, text, re.DOTALL)

        if fallback_matches:
            return fallback_matches[-1]

        return text  

    async def run(self, data: Dict[str, Any], config: Optional[dict] = None) -> Dict[str, Any]:
        config = config or {}
        input_key = self.kwargs.get("input_keys", [])[-1]
        output_key = self.kwargs.get("output_key", "parsed_output")

        raw_input = data.get(input_key, "")
        parsed_result = self.preprocess(raw_input)

        data[output_key] = parsed_result
        return data
