from typing import Any, List, Optional, Dict
import copy

from etri_langgraph.utils.registry import (
    node_registry,
    prompt_registry,
    model_registry,
    BaseNode,
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

    def preprocess(self):
        prompt_conf = self.kwargs.get("prompt", {})
        prompt_type = prompt_conf.get("type")
        prompt_kwargs = prompt_conf.get("kwargs", {})

        prompt = prompt_registry[prompt_type](
            examples=self.examples,
            **prompt_kwargs,
        )
        model = model_registry[prompt_type](**self.llm)

        chain = prompt | model | StrOutputParser()
        chain.name = "llm_chain"

        return chain

    async def run(self, data: List[dict], config: Optional[dict] = None) -> dict:
        config = config or {}

        chain = self.preprocess()
        latest_data = data[-1]

        result = await chain.ainvoke(latest_data, config=config)
        output_key = self.kwargs.get("output_key", "output")

        latest_data.update({output_key: result})
        return latest_data
