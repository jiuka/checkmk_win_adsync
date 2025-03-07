#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2025  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cmk.graphing.v1 import graphs, metrics, perfometers, translations, Title

translation_win_adsync_connector = translations.Translation(
    name='win_adsync_connector',
    check_commands=[translations.PassiveCheck('win_adsync_connector')],
    translations={
        'last_sync': translations.RenameTo('win_adsync_connector_last_sync'),
        'duration': translations.RenameTo('win_adsync_connector_duration'),
    },
)

metric_win_adsync_connector_last_sync = metrics.Metric(
    name='win_adsync_connector_last_sync',
    title=Title('Last Sync'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.BLUE,
)

metric_win_adsync_connector_duration = metrics.Metric(
    name='win_adsync_connector_duration',
    title=Title('Sync Curation'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.GREEN,
)

perfometer_dell_storage_center = perfometers.Stacked(
    name='win_adsync_connector',
    upper=perfometers.Perfometer(
        name='win_adsync_connector_duration',
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(300)),
        segments=['win_adsync_connector_duration'],
    ),
    lower=perfometers.Perfometer(
        name='win_adsync_connector_last_sync',
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(3600)),
        segments=['win_adsync_connector_last_sync'],
    ),
)
