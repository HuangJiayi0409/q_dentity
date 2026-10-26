"""Versioned, lossless JSON DAG. References are storage sharing, not equalities."""
import json

MAX_NODES = 1000000


def pack(value):
    nodes, index, memo = [], {}, {}

    def visit(item):
        if not isinstance(item, (dict, list)):
            return item
        if id(item) in memo:
            return {'$ref': memo[id(item)]}
        node = ({k: visit(v) for k, v in item.items()} if isinstance(item, dict)
                else [visit(v) for v in item])
        key = json.dumps(node, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        if key not in index:
            if len(nodes) >= MAX_NODES:
                raise ValueError('wire_node_budget')
            index[key] = len(nodes)
            nodes.append(node)
        memo[id(item)] = index[key]
        return {'$ref': index[key]}

    root = visit(value)
    return {'packet_version': 2, 'nodes': nodes, 'root': root}


def unpack(packet):
    if not isinstance(packet, dict) or 'packet_version' not in packet:
        return packet  # Read historical v1 evidence as well.
    if packet['packet_version'] != 2 or set(packet) != {'packet_version', 'nodes', 'root'}:
        raise ValueError('unsupported_wire_packet')
    nodes = packet['nodes']
    if not isinstance(nodes, list) or len(nodes) > MAX_NODES:
        raise ValueError('wire_node_budget')
    values = []

    def decode(item):
        if isinstance(item, dict):
            if set(item) != {'$ref'}:
                raise ValueError('wire_expected_reference')
            n = item['$ref']
            if type(n) is not int or not 0 <= n < len(values):
                raise ValueError('wire_forward_or_invalid_reference')
            return values[n]
        if isinstance(item, list):
            raise ValueError('wire_uninterned_array')
        return item

    for node in nodes:
        if isinstance(node, dict):
            values.append({k: decode(v) for k, v in node.items()})
        elif isinstance(node, list):
            values.append([decode(v) for v in node])
        else:
            raise ValueError('wire_expected_container')
    return decode(packet['root'])
