from __future__ import print_function, unicode_literals

import re

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.settings.static_media import PIPELINE_CSS, PIPELINE_JS


ROOT = settings.ROOT_PATH
PIPELINE_RE = re.compile(r"\{\% (stylesheet|javascript) '([^']+)' \%\}")
SPACE_RE = re.compile(r'^\s+')
BUNDLES = {
    'javascript': PIPELINE_JS,
    'stylesheet': PIPELINE_CSS,
}
STYLE_TEMPLATE = '<link href="{{ static(\'%s\') }}" rel="stylesheet" type="text/css" />'
JS_TEMPLATE = '<script type="text/javascript" src="{{ static(\'%s\') }}" charset="utf-8"></script>'
BUNDLE_TEMPLATE = '{0}/BUNDLES/{1}.{0}'


def get_leading_space(line):
    match = SPACE_RE.match(line)
    if match:
        return match.group(0)

    return ''


class Command(BaseCommand):
    """Command to convert all templates from Pipeline bundles to individual assets.

    TODO: Delete me after pipeline removal.
    """
    def handle(self, *args, **options):
        for template in ROOT.glob('bedrock/*/templates/**/*.html'):
            print('===============')
            print(template)
            lines = []
            modified = False
            with template.open('r') as tf:
                for line in tf:
                    match = PIPELINE_RE.search(line)
                    if match:
                        print(line)
                        mtype, bundle = match.groups()
                        indent = get_leading_space(line)
                        if mtype == 'stylesheet':
                            lines.append(indent + STYLE_TEMPLATE % BUNDLE_TEMPLATE.format('css', bundle) + '\n')
                        else:
                            lines.append(indent + JS_TEMPLATE % BUNDLE_TEMPLATE.format('js', bundle) + '\n')

                        modified = True
                        print(lines[-1])
                    else:
                        lines.append(line)

            if modified:
                with template.open('w') as tf:
                    tf.writelines(lines)
