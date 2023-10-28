# Copyright © Zhandos Kadyrkulov 2023 | All Rights Reserved

from . import panels


def register_ui():
    panels.register_panels()


def unregister_ui():
    panels.unregister_panels()