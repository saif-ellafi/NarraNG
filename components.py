import json
import os
from common import Common


class NodeEncoder(json.JSONEncoder):

    @staticmethod
    def encode_qrange(qr):
        return {
            'minv': qr.minv,
            'maxv': qr.maxv,
            'mode': qr.mode
        }

    def default(self, o):
        if isinstance(o, LinkNode):
            base = {}
            if o.project:
                base['project'] = o.project
            base['name'] = o.name
            base['bound'] = o.bound
            base['weight'] = o.weight
            if o.description:
                base['description'] = o.description
            base['qrange'] = NodeEncoder.encode_qrange(o.qrange)
            base['links'] = o.external if o.external else o.links
            return base
        elif isinstance(o, LeafNode):
            base = {
                'name': o.name,
                'weight': o.weight
            }
            if o.description:
                base['description'] = o.description
            return base
        else:
            return json.JSONEncoder.default(self, o)


class NodeDecoder:

    @staticmethod
    def decode_qrange(content):
        return QRange(content['minv'], content['maxv'], content['mode'])

    @staticmethod
    def decode_listlinks(links, root):
        for link in links:
            if 'bound' in link:
                node = LinkNode(
                    root,
                    link['name'],
                    link['bound'],
                    link['weight'],
                    NodeDecoder.decode_qrange(link['qrange']),
                    link['description'] if 'description' in link else None
                )
                sublinks = NodeDecoder.decode_links(link['links'], node)
                node.links = list(sublinks)
                yield node
            else:
                node = LeafNode(
                    root,
                    link['name'],
                    link['weight'],
                    link['description'] if 'description' in link else None
                )
                yield node

    @staticmethod
    def decode_links(links, root):
        if type(links) == list:
            return list(NodeDecoder.decode_listlinks(links, root))
        else:
            path = os.path.join(Common.PROJECTS_FOLDER, links+'.json')
            root.external = links
            with open(path) as sublinks_file:
                delegate_sublinks = NodeDecoder.decode(sublinks_file).links
            return delegate_sublinks

    @staticmethod
    def decode(file):
        root_node = json.load(file)
        name = root_node['name']
        bound = root_node['bound']
        weight = root_node['weight']
        qrange = NodeDecoder.decode_qrange(root_node['qrange'])
        description = root_node['description'] if 'description' in root_node else None
        root = LinkNode(None, name, bound, weight, qrange, description)
        root.root = root
        if 'project' in root_node:
            root.project = root_node['project']
        root_links = list(NodeDecoder.decode_links(root_node['links'], root))
        root.links = root_links
        return root


class QRange:
    def __init__(self, minv, maxv, mode):
        self.minv = minv
        self.maxv = maxv
        try:
            int_mode = int(mode)
        except ValueError:
            raise Exception('Created QRange with invalid mode. Must be a number %s' % mode)
        if minv <= int_mode <= maxv:
            self.mode = mode
        else:
            raise Exception("Mode must be within minv and maxv")


class Node:
    def __init__(self, root, name, weight, description):
        super(Node, self).__init__()
        self.root = root
        self.name = name
        self.description = description
        if type(weight) != float:
            raise Exception('Node weight must be float')
        self.weight = weight

    def __eq__(self, other):
        return self.name == other.name and self.root.name == other.root.name

    def __repr__(self):
        sel_str = self.tostr(self, '')
        sel_str += '\n'
        return sel_str

    def tostr(self, node, sel_str):
        if isinstance(node, LeafNode):
            sel_str += '\t'
        sel_str += node.name + (' (( ' + node.description + ' )) ' if node.description else ' ')
        if isinstance(node, LinkNode):
            for subnode in node.links:
                sel_str = self.tostr(subnode, sel_str + '\n\t')
        return sel_str


class LinkNode(Node):
    MAPPER = {
        's': 'single',
        'm': 'many',
        'a': 'all'
    }

    def __init__(self, root, name, bound, weight, qrange, description):
        lb = bound.lower()
        if lb not in list(LinkNode.MAPPER.keys()) + list(LinkNode.MAPPER.values()):
            raise Exception('LinkNode bound must be either single(s), many(m) or all(a)')
        super(LinkNode, self).__init__(root, name, weight, description)
        self.project = None
        self.bound = LinkNode.MAPPER[lb] if lb in LinkNode.MAPPER.keys() else lb
        self.links = []
        self.qrange = qrange
        self.locked = False
        self.external = None

    def save(self):
        with open(os.path.join(Common.OUTPUT_FOLDER, self.name+'.txt'), 'w') as file:
            file.write(str(self))
        with open(os.path.join(Common.OUTPUT_FOLDER, self.name+'.json'), 'w') as file:
            json.dump(self, file, cls=NodeEncoder, indent=2)


class LeafNode(Node):
    def __init__(self, root, name, weight, description):
        super(LeafNode, self).__init__(root, name, weight, description)
