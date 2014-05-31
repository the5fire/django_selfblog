#coding:utf-8
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import force_bytes, force_text


def restructuredtext(value):
    import warnings
    warnings.warn('The restructuredtext filter has been deprecated',
                  category=DeprecationWarning)
    try:
        from docutils.core import publish_parts
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'restructuredtext' filter: The Python docutils library isn't installed.")
        return force_text(value)
    else:
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(source=force_bytes(value), writer_name="html4css1", settings_overrides=docutils_settings)
        return mark_safe(force_text(parts["fragment"]))
