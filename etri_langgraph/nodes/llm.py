from typing import Any, List, Optional, Dict
from etri_langgraph.utils.registry import (
    node_registry, prompt_registry, model_registry, BaseNode,
)
from langchain_core.output_parsers import StrOutputParser

@node_registry(name="llm")
class LLMNode(BaseNode):
    def __init__(
        self,
        key: str,
        examples: Optional[dict] = None,
        llm: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.key = key
        self.examples = examples
        self.llm = llm or {}
        self.kwargs = kwargs
        self.prompt_conf = kwargs.get("prompt", {})

    async def run(self, data: List[dict]) -> dict:
        prompt_type = self.prompt_conf.get("type")
        prompt_kwargs = self.prompt_conf.get("kwargs", {})

        chain = (
            prompt_registry[prompt_type](examples=self.examples, **prompt_kwargs)
            | model_registry[prompt_type](**self.llm)
            | StrOutputParser()
        )

        result = await chain.ainvoke(data[-1])
        data.update({self.kwargs.get("output_key", "output"): result})
        return data
