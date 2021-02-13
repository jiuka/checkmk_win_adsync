#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from pathlib import Path
from typing import Any

from cmk.base.cee.plugins.bakery.bakery_api.v0 import FileGenerator, OS, Plugin, register


def get_win_adsync_files(conf: Any) -> FileGenerator:
    yield Plugin(base_os=OS.WINDOWS, source=Path('win_adsync.ps1'))


register.bakery_plugin(
    name='win_adsync',
    files_function=get_win_adsync_files,
)
