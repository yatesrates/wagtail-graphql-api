from django.core import checks

from wagtail_graphql import settings


def check_settings(app_configs, **kwargs):
    errors = []
    default_filter = settings.WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER
    allowed_filters = settings.WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS

    from wagtail.images.models import Filter
    from wagtail.images.exceptions import InvalidFilterSpecError

    try:
        Filter(spec=default_filter).operations
    except InvalidFilterSpecError:
        errors.append(
            checks.Error(
                'WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER setting must be a '
                'valid Wagtail image filter.',
                hint='http://docs.wagtail.io/en/stable/topics/images.html',
                id='wagtail_graphql.E001',
            )
        )

    try:
        for rendition_filter in allowed_filters:
            Filter(spec=rendition_filter).operations
    except InvalidFilterSpecError:
        errors.append(
            checks.Error(
                'WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS setting must '
                'be a collection of valid Wagtail image filters.',
                hint='http://docs.wagtail.io/en/stable/topics/images.html',
                id='wagtail_graphql.E002',
            )
        )

    return errors


def register_checks():
    checks.register(check_settings)