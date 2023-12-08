from graphene import Enum
from graphene_django.converter import (
    convert_django_field,
    get_django_field_description,
    generate_enum_name,
)

from konst.models.fields import ConstantChoiceField, ConstantChoiceCharField


@convert_django_field.register(ConstantChoiceField)
@convert_django_field.register(ConstantChoiceCharField)
def convert_field_to_enum(field, registry=None):
    """Convert a ConstantChoiceField to a Graphene Enum."""
    class EnumWithDescriptionsType:
        @property
        def description(self):
            constant = field.constants.by_value[self.value]
            return constant.label if constant else None

    return Enum(
        generate_enum_name(field.model._meta, field),
        [(constant.id.upper(), constant.v) for constant in field.constants.constants],
        type=EnumWithDescriptionsType,
        description=get_django_field_description(field),
    )
