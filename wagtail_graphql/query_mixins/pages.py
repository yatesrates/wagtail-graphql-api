from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql.inventory import inventory
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs
from wagtail_graphql.query_mixins.base import get_model_query_attributes_by_app, get_app_query_attributes


def get_page_attributes_by_app():
    def resolve_pages_create(model):
        """
        Create a function to resolve all pages for a certain page model.
        """

        def resolve_pages(self, info, **kwargs):
            return get_base_queryset_for_page_model_or_qs(
                model, info, **kwargs
            )

        return resolve_pages

    return get_model_query_attributes_by_app(
        inventory.pages.graphql_types,
        resolve_objects_func=resolve_pages_create
    )


def get_pages_type():
    attrs = dict(get_app_query_attributes(get_page_attributes_by_app()))

    class PagesByAppQueryMixin:
        description = _(
            'Contains Django apps used by the registered GraphQL models.'
        )

    attrs['Meta'] = PagesByAppQueryMixin
    return type('PagesByAppQueryMixin', (graphene.ObjectType, ), attrs)


class PageQueryMixinMeta:
    description = _('Object that contains all pages-related data.')


# Create the page query mixin dynamically.
PageQueryMixin = type(
    'PageQueryMixin', tuple(), {
        'pages': graphene.Field(get_pages_type()),
        'resolve_pages': lambda *args, **kwargs: True,
        'Meta': PageQueryMixinMeta
    }
)
