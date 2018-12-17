import json


class NodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, LinkNode):
            return {'name': o.name, 'bound': o.bound, 'links': o.links}
        elif isinstance(o, LeafNode):
            return {'name': o.name, 'weight': o.weight}
        else:
            return json.JSONEncoder.default(self, o)


class NodeDecoder:

    @staticmethod
    def node_generator(links, root):
        for link in links:
            if 'bound' in link:
                node = LinkNode(root, link['name'], link['bound'])
                sublinks = NodeDecoder.node_generator(link['links'], node)
                node.links = list(sublinks)
                yield node
            else:
                node = LeafNode(root, link['name'], link['weight'])
                yield node
    @staticmethod
    def decode(file):
        root_node = json.load(file)
        name = root_node['name']
        bound = root_node['bound']
        root = LinkNode(None, name, bound)
        root.root = root
        root_links = list(NodeDecoder.node_generator(root_node['links'], root))
        root.links = root_links
        return root


class Node:
    def __init__(self, root, name):
        super(Node, self).__init__()
        self.root = root
        self.name = name


class LinkNode(Node):
    MAPPER = {
        's': 'single',
        'm': 'many',
        'a': 'all'
    }

    def __init__(self, root, name, bound):
        lb = bound.lower()
        if lb not in list(LinkNode.MAPPER.keys()) + list(LinkNode.MAPPER.values()):
            raise Exception('LinkNode bound must be either single(s), many(m) or all(a)')
        super(LinkNode, self).__init__(root, name)
        self.bound = LinkNode.MAPPER[lb] if lb in LinkNode.MAPPER.keys() else lb
        self.links = []


class LeafNode(Node):
    def __init__(self, root, name, weight):
        if type(weight) != float:
            raise Exception('LeafNode weight must be float')
        self.weight = weight
        super(LeafNode, self).__init__(root, name)
