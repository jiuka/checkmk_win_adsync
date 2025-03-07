#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# win_adsync_connector - Azure AD Connect Connector check
#
# Copyright (C) 2020-2025  Marius Rieder <marius.rieder@scs.ch>
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

# <<<win_adsync_connector>>>
# cmk.onmicrosoft.com - AAD Delta Import;success;903;05.13.2020 13:37:57;
# cmk.onmicrosoft.com - AAD Delta Synchronization;success;124;05.13.2020 13:37:58;
# cmk.onmicrosoft.com - AAD Export;success;890;05.13.2020 13:38:05;
# cmk.com Full Import;success;523;05.12.2020 17:51:04;
# cmk.com Delta Import;success;34;05.13.2020 13:37:53;
# cmk.com Delta Synchronization;success;140;05.13.2020 13:37:58;
# cmk.com Export;completed-export-errors;33;05.13.2020 13:38:06;

from typing import NamedTuple
from datetime import datetime, timezone
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    check_levels,
    DiscoveryResult,
    Service,
    State,
    StringTable,
    render,
    Result,
)


class AdsyncConnector(NamedTuple):
    state: str
    duration: int
    lastrun: datetime


def parse_win_adsync_connector(string_table: StringTable) -> dict[AdsyncConnector]:
    parsed = {}
    for line in string_table:
        parsed[line[0]] = AdsyncConnector(
            state=line[1],
            duration=float(line[2]),
            lastrun=datetime.strptime(line[3], '%d.%m.%Y %H:%M:%S').replace(tzinfo=timezone.utc),
        )
    return parsed


agent_section_win_adsync_connector = AgentSection(
    name='win_adsync_connector',
    parse_function=parse_win_adsync_connector,
)


def discovery_win_adsync_connector(section: dict[AdsyncConnector]) -> DiscoveryResult:
    for name in section.keys():
        yield Service(item=name)


def check_win_adsync_connector(item: str, params: dict, section: dict[AdsyncConnector]) -> CheckResult:
    if item not in section:
        return

    conn = section[item]

    if conn.state == 'success':
        yield Result(state=State.OK, summary='State: Success')
    else:
        yield Result(state=State.WARN, summary=f'State: {conn.state}')

    yield Result(state=State.OK, summary='Last sync: %s' % conn.lastrun.astimezone().strftime('%c'))

    yield from check_levels(
        value=conn.duration,
        metric_name='duration',
        levels_upper=params.get('duration', None),
        render_func=render.timespan,
        label='Sync duration'
    )


check_plugin_win_adsync_connector = CheckPlugin(
    name='win_adsync_connector',
    service_name='ADSync %s',
    discovery_function=discovery_win_adsync_connector,
    check_function=check_win_adsync_connector,
    check_ruleset_name='win_adsync_connector',
    check_default_parameters={'duration': ('fixed', (300, 600))},
 )
