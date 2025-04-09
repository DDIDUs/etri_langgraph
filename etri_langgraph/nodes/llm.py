from typing import Any, List, Optional
import copy

from etri_langgraph.utils.sampling import get_node_config_by_name, extract_inputs_from_target
from etri_langgraph.utils.registry import register_module
from etri_langgraph.model.chat import GeneralChatModel

@register_module("llm", "llm_jun")
def node2(state: List[dict]):
    current_state = copy.deepcopy(state[-1]) if state else {}
    node_info = get_node_config_by_name(current_state, "llm_jun")
    input_keys = node_info["input_keys"]
    result = extract_inputs_from_target(current_state, input_keys)

    
    messages = result["prompt_jun_out"]


    chat_model = GeneralChatModel(
        model="meta-llama/Llama-3.1-8B-Instruct",               # 또는 meta-llama/Llama-3.1-8B-Instruct 등
        max_tokens=16384,
        temperature=0.7,
        top_p=1.0,
        platform="vllm",          # "azure", "vllm", "open_webui" 등도 가능
    )

    try:
        result = chat_model._generate(messages=messages)
        response_text = result.generations[0].message.content
    except Exception as e:
        response_text = f"[node2] LLM error: {str(e)}"

    if response_text:
        current_state.setdefault("target", {})
        current_state["target"]["llm_jun_out"] = response_text            

    state.append(current_state)
    return state
