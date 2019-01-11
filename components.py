import json
import os
import logging
from common import Common

logging.getLogger().setLevel(Common.LOG_LEVEL)


class NodeEncoder(json.JSONEncoder):

    @staticmethod
    def encode_nrange(nr):
        return {
            'minv': nr.minv,
            'maxv': nr.maxv,
            'mode': nr.mode
        }

    def default(self, o):
        base = {
            'name': o.name,
            'weight': o.weight
        }
        if o.description:
            base['description'] = o.description
        if o.must:
            base['must'] = o.must
        if o.vrange:
            base['vrange'] = NodeEncoder.encode_nrange(o.vrange)
        if isinstance(o, ExternalNode):
            base['link'] = o.link
            return base
        elif isinstance(o, LinkNode):
            if o.project:
                base['project'] = o.project
            base['bound'] = o.bound
            base['qrange'] = NodeEncoder.encode_nrange(o.qrange)
            base['links'] = o.links
            return base
        elif isinstance(o, LeafNode):
            return base
        else:
            return json.JSONEncoder.default(self, o)


class OutputNodeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ExternalNode):
            raise Exception("output encoder received an uncompressed ExternalNode")
        elif isinstance(o, LinkNode):
            base = {
                'name': o.name
            }
            if o.description:
                base['description'] = o.description
            if o.project:
                base['project'] = o.project
            if isinstance(o.value, int):
                base['value'] = o.value
            base['links'] = o.links
            return base
        elif isinstance(o, LeafNode):
            base = {
                'name': o.name
            }
            if o.description:
                base['description'] = o.description
            if isinstance(o.value, int):
                base['value'] = o.value
            return base
        else:
            return json.JSONEncoder.default(self, o)


class NodeDecoder:

    @staticmethod
    def decode_qrange(content):
        return NRange(content['minv'], content['maxv'], content['mode'])

    @staticmethod
    def decode_listlinks(links, root):
        for link in links:
            if 'links' in link:
                node = LinkNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                if 'must' in link:
                    node.set_must(link['must'])
                if 'vrange' in link:
                    node.set_vrange(NodeDecoder.decode_qrange(link['vrange']))
                node.set_bound(link['bound'])
                node.set_weight(link['weight'])
                node.set_qrange(NodeDecoder.decode_qrange(link['qrange'])),
                sublinks = NodeDecoder.decode_links(link['links'], node)
                node.links = list(sublinks)
                yield node
            elif 'link' in link:
                node = ExternalNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None,
                    link['link']
                )
                node.set_weight(link['weight'])
                if 'qrange' in link:
                    node.set_qrange(NodeDecoder.decode_qrange(link['qrange']))
                if 'bound' in link:
                    node.set_bound(link['bound'])
                if 'must' in link:
                    node.set_must(link['must'])
                yield node
            else:
                node = LeafNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                if 'must' in link:
                    node.set_must(link['must'])
                if 'vrange' in link:
                    node.set_vrange(NodeDecoder.decode_qrange(link['vrange']))
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
                if 'value' in link:
                    node.set_value(link['value'])
                yield node
            elif 'link' in link:
                raise Exception('Decoder attempted to read output with a compressed ExternalNode. Bad Encoder?')
            else:
                node = LeafNode(
                    root,
                    link['name'],
                    link['description'] if 'description' in link else None
                )
                if 'value' in link:
                    node.set_value(link['value'])
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
        logging.debug("Decoding file %s" % file)
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


class NRange:
    def __init__(self, minv, maxv, mode):
        self.minv = minv
        self.maxv = maxv
        try:
            int_mode = int(mode)
        except ValueError:
            raise Exception('Created Node Range with invalid mode. Must be a number %s' % mode)
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
        self.must = None
        self.vrange = None
        self.value = None

    def __eq__(self, other):
        logging.debug("Comparing %s with %s and root name %s vs %s" % (self.name, other.name, self.root.name, other.root.name))
        return self.name == other.name and self.root.name == other.root.name

    def __repr__(self):
        sel_str = self.tostr(self, '')
        sel_str += '\n'
        return sel_str

    def tostr(self, node, sel_str, i=1):
        sel_str += node.name + ((': %i' % node.value) if isinstance(node.value, int) else '') + (' (( ' + node.description + ' )) ' if node.description else ' ')
        if isinstance(node, LinkNode):
            for subnode in node.links:
                sel_str = self.tostr(subnode, sel_str + '\n' + '\t'*i, i+1)
        return sel_str

    def set_weight(self, weight):
        try:
            self.weight = float(weight)
        except ValueError:
            raise Exception('Node weight must be float compatible value. Received %s' % str(weight))

    def set_must(self, must):
        if must:
            self.must = must

    def set_value(self, value):
        if isinstance(value, int):
            self.value = value
        else:
            raise Exception("Attempted to set non int value to node")

    def set_vrange(self, vrange):
        if isinstance(vrange, NRange):
            self.vrange = vrange
        else:
            raise Exception("Attempted to set non QRange object as vrange")

    def clear_vrange(self):
        self.vrange = None


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
        if not isinstance(qrange, NRange):
            raise Exception("received invalid qrange. not QRange object.")
        self.qrange = qrange

    def save(self):
        output_path = os.path.join(Common.OUTPUT_FOLDER, self.project)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        with open(os.path.join(output_path, self.name+'.txt'), 'w') as file:
            file.write(str(self))
        with open(os.path.join(output_path, self.name+'.json'), 'w') as file:
            json.dump(self, file, cls=OutputNodeEncoder, indent=2)


class ExternalNode(LinkNode):
    def __init__(self, root, name, description, link):
        super(ExternalNode, self).__init__(root, name, description)
        self.link = link

    def __eq__(self, other):
        logging.debug("Comparing %s with %s and root name %s vs %s" % (self.name, other.name, self.root.name, other.root.name))
        return self.name == other.name


class LeafNode(Node):
    def __init__(self, root, name, description):
        super(LeafNode, self).__init__(root, name, description)
