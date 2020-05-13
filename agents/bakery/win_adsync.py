#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def bake_win_adsync(opsys, conf, conf_dir, plugins_dir):
    shutil.copy2(cmk.utils.paths.local_agents_dir + "/windows/plugins/win_adsync.ps1",
                 plugins_dir + "/win_adsync.ps1")

bakery_info["win_adsync"] = {
    "bake_function" : bake_win_adsync,
    "os"            : [ "windows" ],
}