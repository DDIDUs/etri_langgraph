import copy
from typing import Dict, List, Optional

from etri_langgraph.utils.sampling import get_node_config_by_name, extract_inputs_from_target
from etri_langgraph.prompt.chat import chat_prompt
from etri_langgraph.utils.registry import register_module

@register_module("prompt", "prompt_jun")
def node1(state: List[dict]):
    current_state = copy.deepcopy(state[-1]) if state else {}
    node_info = get_node_config_by_name(current_state, "prompt_jun")
    input_keys = node_info["input_keys"]
    result = extract_inputs_from_target(current_state, input_keys)

    body_template_paths = node_info.get("kwargs", {}).get("body_template_paths", [])
        
    examples = []  # 필요하면 여기에 예제 목록 전달
    system_template_paths = []  # 필요하면 설정에서 가져와도 됨
    prompt_result = chat_prompt(
        examples=examples,
        body_template_paths=body_template_paths,
        system_template_paths=system_template_paths,
    )
    
    if prompt_result:
        final_messages = prompt_result.format_messages(
            prompt=result["prompt"],
        )

    if final_messages:
        current_state.setdefault("target", {})
        current_state["target"]["prompt_jun_out"] = final_messages            

    state.append(current_state)
    return state