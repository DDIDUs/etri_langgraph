def get_node_config_by_name(config: dict, node_name: str) -> dict:
    nodes = config.get("config", {}).get("graph", {}).get("nodes", [])
    for node in nodes:
        if node.get("name") == node_name:
            return node
    return {}

def extract_inputs_from_target(current_state: dict, input_keys: list) -> dict:
    target = current_state.get("target", {})
    
    missing_keys = [key for key in input_keys if key not in target]
    if missing_keys:
        raise KeyError(f"'target' 블록에 다음 키가 없습니다: {missing_keys}")

    return {key: target[key] for key in input_keys}