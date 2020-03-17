definition = {
    'port': {
        'xpath': './',
        'children': {
            'number': {
                'attribute': 'portid'
            },
            'protocol': {
                'attribute': 'protocol'
            }
        },
    },
    'state': {
        'attribute': 'state',
        'xpath': './state'
    },
    'service': {
        'xpath': './service',
        'children': {
            'name': {
                'attribute': 'name'
            },
            'product': {
                'attribute': 'product'
            },
            'version': {
                'attribute': 'version'
            }
        },
    }
}


class Element:
    name = None
    xpath = "./"
    parent = None
    children = []
    attribute = None
    level = 0

    def __init__(self, key):
        self.name = key

    @staticmethod
    def build(definition_object, parent=None):
        elements = []

        for _, key in enumerate(definition_object):
            elem = Element(key)

            if 'xpath' in definition_object:
                elem.xpath = definition_object[key]['xpath']

            if parent:
                elem.level = parent.level + 1

            if 'attribute' in definition_object[key]:
                elem.attribute = definition_object[key]['attribute']

            # Recursively build children
            if 'children' in definition_object[key]:
                elem.children.append(Element.build(definition_object[key]['children'], elem))

            elements.append(elem)

        return elements

    @staticmethod
    def supported_columns(elements, parent=None):
        columns = []

        for element in elements:
            elem = element.name

        return columns


print(Element.build(definition))
