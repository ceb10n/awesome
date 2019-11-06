from .attribute_type import AttributeType
from .attribute import Attribute


class AttributeDefinitionFactory:

    def create(self, info):
        attrs = []

        if 'AttributeDefinitions' in info:
            table_attrs = info['AttributeDefinitions']
            for attr in table_attrs:
                attrs.append(
                    Attribute(
                        attr['AttributeName'],
                        AttributeType(attr['AttributeType']),
                        None))

        return attrs
