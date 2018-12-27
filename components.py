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
            base['links'] = o.links
            return base
        elif isinstance(o, LeafNode):
            base = {
                'name': o.name,
                'weight': o.weight
            }
            if o.description:
                base['description'] = o.description
            return base
        elif isinstance(o, ValueNode):
            base = {}
            base['name'] = o.name
            base['weight'] = o.weight
            if o.description:
                base['description'] = o.description
            base['qrange'] = NodeEncoder.encode_qrange(o.qrange)
            return base
        elif isinstance(o, ExternalNode):
            base = {}
            base['name'] = o.name
            base['weight'] = o.weight
            if o.description:
                base['description'] = o.description
            base['link'] = o.link
            return base
        else:
            return json.JSONEncoder.default(self, o)


class OutputNodeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, LinkNode):
            base = {}
            if o.project:
                base['project'] = o.project
            base['name'] = o.name
            if o.description:
                base['description'] = o.description
            base['links'] = o.links
            return base
        elif isinstance(o, LeafNode):
            base = {
                'name': o.name
            }
            if o.description:
                base['description'] = o.description
            return base
        elif isinstance(o, ValueNode):
            if not o.value:
                raise Exception("Cannot encode an Output ValueNode without value")
            base = {
                'name': o.name,
                'value': o.value
            }
            if o.description:
                base['description'] = o.description
            return base
        elif isinstance(o, ExternalNode):
            raise Exception("output encoder received an uncompressed ExternalNode")
        else:
            return json.JSONEncoder.default(self, o)


class NodeDecoder:

    @staticmethod
    def decode_qrange(content):
        return QRange(content['minv'], content['maxv'], content['mode'])

    @staticmethod
    def decode_listlinks(links, root):
        for link in links:
            if 'links' in link:
                node = LinkNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                node.set_bound(link['bound'])
                node.set_weight(link['weight'])
                node.set_qrange(NodeDecoder.decode_qrange(link['qrange'])),
                sublinks = NodeDecoder.decode_links(link['links'], node)
                node.links = list(sublinks)
                yield node
            elif 'qrange' in link:
                node = ValueNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                node.set_weight(link['weight'])
                node.set_qrange(NodeDecoder.decode_qrange(link['qrange']))
                yield node
            elif 'link' in link:
                node = ExternalNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None,
                    link['link']
                )
                node.set_weight(link['weight'])
                yield node
            else:
                node = LeafNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                node.set_weight(link['weight'])
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
        root = LinkNode(None, name, description)
        root.set_bound(bound)
        root.set_weight(weight)
        root.set_qrange(qrange)
        root.root = root
        if 'project' in root_node:
            root.project = root_node['project']
        root_links = list(NodeDecoder.decode_links(root_node['links'], root))
        root.links = root_links
        return root


class OutputNodeDecoder:

    @staticmethod
    def decode_listlinks(links, root):
        for link in links:
            if 'links' in link:
                node = LinkNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                sublinks = OutputNodeDecoder.decode_links(link['links'], node)
                node.links = list(sublinks)
                yield node
            elif 'value' in link:
                node = ValueNode(
                    root,
                    link['name'],
                    description=link['description'] if 'description' in link else None
                )
                node.value = link['value']
                yield node
            elif 'link' in link:
                raise Exception('Decoder attempted to read output with a compressed ExternalNode. Bad Encoder?')
            else:
                node = LeafNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                yield node

    @staticmethod
    def decode_links(links, root):
        if type(links) == list:
            return list(OutputNodeDecoder.decode_listlinks(links, root))
        else:
            path = os.path.join(Common.PROJECTS_FOLDER, links+'.json')
            root.external = links
            with open(path) as sublinks_file:
                delegate_sublinks = OutputNodeDecoder.decode(sublinks_file).links
            return delegate_sublinks

    @staticmethod
    def decode(file):
        root_node = json.load(file)
        name = root_node['name']
        description = root_node['description'] if 'description' in root_node else None
        root = LinkNode(None, name, description)
        root.root = root
        if 'project' in root_node:
            root.project = root_node['project']
        root_links = list(OutputNodeDecoder.decode_links(root_node['links'], root))
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
    def __init__(self, root, name, description):
        super(Node, self).__init__()
        self.root = root
        self.name = name
        self.description = description
        self.weight = None

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
        elif isinstance(node, ValueNode):
            sel_str += ': %i' % node.value
        return sel_str

    def set_weight(self, weight):
        if type(weight) != float:
            raise Exception('Node weight must be float')
        self.weight = weight


class LinkNode(Node):
    MAPPER = {
        's': 'single',
        'm': 'many',
        'a': 'all'
    }

    def __init__(self, root, name, description):
        super(LinkNode, self).__init__(root, name, description)
        self.project = None
        self.links = []
        self.bound = None
        self.qrange = None
        self.locked = False

    def set_bound(self, bound):
        lb = bound.lower()
        if lb not in list(LinkNode.MAPPER.keys()) + list(LinkNode.MAPPER.values()):
            raise Exception('LinkNode bound must be either single(s), many(m) or all(a)')
        self.bound = LinkNode.MAPPER[lb] if lb in LinkNode.MAPPER.keys() else lb

    def set_qrange(self, qrange):
        if not isinstance(qrange, QRange):
            raise Exception("received invalid qrange. not QRange object.")
        self.qrange = qrange

    def save(self):
        with open(os.path.join(Common.OUTPUT_FOLDER, self.name+'.txt'), 'w') as file:
            file.write(str(self))
        with open(os.path.join(Common.OUTPUT_FOLDER, self.name+'.json'), 'w') as file:
            json.dump(self, file, cls=OutputNodeEncoder, indent=2)


class LeafNode(Node):
    def __init__(self, root, name, description):
        super(LeafNode, self).__init__(root, name, description)


class ValueNode(Node):
    def __init__(self, root, name, description):
        super(ValueNode, self).__init__(root, name, description)
        self.qrange = None
        self.value = None

    def set_qrange(self, qrange):
        if not isinstance(qrange, QRange):
            raise Exception("received invalid qrange. not QRange object.")
        self.qrange = qrange

    def set_value(self, value):
        if self.qrange.minv <= value <= self.qrange.maxv:
            self.value = value
        else:
            raise Exception("ValueNode value must be within qrange")


class ExternalNode(Node):
    def __init__(self, root, name, description, link):
        super(ExternalNode, self).__init__(root, name, description)
        self.link = link
