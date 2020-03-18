definition = dict(
    port={
        'xpath': '.',
        'children': dict(
            number={
                'attribute': 'portid'
            },
            protocol={
                'attribute': 'protocol'
            }
        ),
    },
    state={
        'attribute': 'state',
        'xpath': 'state'
    },
    service={
        'xpath': 'service',
        'children': dict(
            name={
                'attribute': 'name'
            },
            product={
                'attribute': 'product'
            },
            version={
                'attribute': 'version'
            }
        )
    }
)


class Element:
    name = None
    xpath = ""
    parent = None
    children = []
    attribute = None
    text = False
    level = 0

    def __init__(self, key):
        self.name = key

    def xpathfull(self, xpath=None):
        """Return a full xPath for the element"""

        if xpath is None:
            xpath = []

        xpath.append(self.xpath)

        if self.parent:
            return self.parent.xpathfull(xpath)

        return "".join(reversed(xpath))

    def data(self, xml_element, default=""):
        """Get data from the element depending on the "type" of element,
        either it's attribute data or the text value from the XML element
        """

        if self.text:
            if xml_element.text:
                return xml_element.text
            else:
                return default

        if self.attribute:
            return xml_element.get(self.attribute, default)

        return default

    def find(self, key):
        if key == self.name:
            return self

        splitted_names = key.split(".")

        for k in splitted_names:
            if self.name == k:
                if self.children:
                    for child in self.children:
                        elem = child.find(".".join(splitted_names[1:]))

                        if elem:
                            return elem

        return None

    @staticmethod
    def build(definition_object, parent=None):
        elements = []

        for _, key in enumerate(definition_object):
            elem = Element(key)

            if 'xpath' in definition_object[key]:
                elem.xpath = definition_object[key]['xpath']

            if 'text' in definition_object[key]:
                elem.text = definition_object[key]['text']

            if parent:
                elem.level = parent.level + 1
                elem.parent = parent

            if 'attribute' in definition_object[key]:
                elem.attribute = definition_object[key]['attribute']

            # Recursively build children elements
            if 'children' in definition_object[key]:
                elem.children = Element.build(definition_object[key]['children'], elem)

            elements.append(elem)

        return elements
