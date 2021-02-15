#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# win_adsync_scheduler - Azure AD Connecht Scheduler check
#
# Copyright (C) 2020  Marius Rieder <marius.rieder@scs.ch>
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

# <<<win_adsync_schedule>>>
# SyncCycleEnabled:True
# MaintenanceEnabled:True
# StagingModeEnabled:False
# SchedulerSuspended:False
# SyncCycleInProgress:False
# NextSyncCycleStartTimeInUTC:05.06.2020 05:11:51

from datetime import datetime, timezone
from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    State,
)


def parse_win_adsync_scheduler(string_table):
    parsed = {}
    for line in string_table:
        key, value = line
        if value == 'True':
            parsed[key] = True
        elif value == 'False':
            parsed[key] = False
        elif key in ['NextSyncCycleStartTimeInUTC']:
            try:
                parsed[key] = datetime.strptime(value, "%d.%m.%Y %H:%M:%S").replace(tzinfo=timezone.utc)
            except Exception:
                pass
        else:
            parsed[key] = value
    return parsed


register.agent_section(
    name='win_adsync_scheduler',
    parse_function=parse_win_adsync_scheduler,
)


def discovery_win_adsync_scheduler(section):
    if len(section) > 0:
        yield Service()


def check_win_adsync_scheduler(params, section):
    for state in ['SyncCycleEnabled', 'MaintenanceEnabled', 'StagingModeEnabled', 'SchedulerSuspended']:
        if state not in params:
            continue

        if state not in section:
            yield Result(state=State.UNKNOWN, summary='Unknown state for %s' % state)
            continue

        if params[state][1] == -1:
            continue

        if section[state] == params[state][0]:
            yield Result(state=State.OK, summary='%s is %s' % (state, section[state]))
        else:
            yield Result(state=State(params[state][1]), summary='%s is %s' % (state, section[state]))

    if 'NextSyncCycleStartTimeInUTC' in section:
        yield Result(state=State.OK, summary='Next sync: %s' % section['NextSyncCycleStartTimeInUTC'].astimezone().strftime('%c'))


register.check_plugin(
    name='win_adsync_scheduler',
    service_name='ADSync Scheduler',
    discovery_function=discovery_win_adsync_scheduler,
    check_function=check_win_adsync_scheduler,
    check_ruleset_name='win_adsync_scheduler',
    check_default_parameters={
        'SyncCycleEnabled': (True, 2),
        'MaintenanceEnabled': (True, 2),
    },
)
