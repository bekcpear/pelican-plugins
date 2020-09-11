from __future__ import unicode_literals
from pelican import signals
from pelican.generators import ArticlesGenerator, StaticGenerator, PagesGenerator
import re

def initialized(pelican):
    print('init')

def extract_summary(instance):
    print(instance._content)

def run_plugin(generators):
    print('run_plugin');


def register():
    signals.initialized.connect(initialized)
    signals.all_generators_finalized.connect(run_plugin)
    signals.content_object_init.connect(extract_summary)
