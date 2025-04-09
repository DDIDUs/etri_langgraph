import copy
from typing import List

from etri_langgraph.utils.sampling import get_node_config_by_name, extract_inputs_from_target
from etri_langgraph.utils.registry import register_module

@register_module("template", "template_jun")
def node3(state: List[dict]):
    current_state = copy.deepcopy(state[-1]) if state else {}
    node_info = get_node_config_by_name(current_state, "template_jun")
    input_keys = node_info["input_keys"]

    result = extract_inputs_from_target(current_state, input_keys)
    
    response_text = "template_jun completed"
    
    if response_text:
        current_state.setdefault("target", {})
        current_state["target"]["template_jun_out"] = response_text            #2

    state.append(current_state)
    return state