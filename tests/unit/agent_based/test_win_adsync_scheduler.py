#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# win_adsync_scheduler - Azure AD Connecht Scheduler check
#
# Copyright (C) 2021 Marius Rieder <marius.rieder@scs.ch>
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

import pytest  # type: ignore[import]
import os
import time
from datetime import datetime, timezone
from cmk.agent_based.v2 import (
    Result,
    Service,
    State,
)
from cmk_addons.plugins.win_adsync.agent_based import win_adsync_scheduler


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        [
            ['SyncCycleEnabled', 'True'],
            ['MaintenanceEnabled', 'True'],
            ['StagingModeEnabled', 'False'],
            ['SchedulerSuspended', 'False'],
            ['SyncCycleInProgress', 'False'],
            ['NextSyncCycleStartTimeInUTC', '05.06.2020 05:11:51'],
        ],
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': False,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        }
    ),
])
def test_parse_win_adsync_scheduler(string_table, result):
    assert win_adsync_scheduler.parse_win_adsync_scheduler(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({}, []),
    (
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': False,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        [Service()]
    )
])
def test_discovery_win_adsync_scheduler(section, result):
    assert list(win_adsync_scheduler.discovery_win_adsync_scheduler(section)) == result


DEFAULT_PARAMS = {
    'SyncCycleEnabled': (True, 2),
    'MaintenanceEnabled': (True, 2),
}


@pytest.mark.parametrize('params, section, result', [
    (
        {},
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': False,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        [
            Result(state=State.OK, summary='SyncCycleEnabled is True'),
            Result(state=State.OK, summary='MaintenanceEnabled is True'),
            Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020')
        ]
    ),
    (
        {},
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': False,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': False,
            'SyncCycleInProgress': False,
        },
        [
            Result(state=State.CRIT, summary='SyncCycleEnabled is False'),
            Result(state=State.OK, summary='MaintenanceEnabled is True'),
            Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020')
        ]
    ),
    (
        {},
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': False,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': False,
            'SyncCycleInProgress': False,
        },
        [
            Result(state=State.CRIT, summary='SyncCycleEnabled is False'),
            Result(state=State.OK, summary='MaintenanceEnabled is True'),
            Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020')
        ]
    ),
    (
        {'SchedulerSuspended': (False, 1)},
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': False,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        [
            Result(state=State.OK, summary='SyncCycleEnabled is True'),
            Result(state=State.OK, summary='MaintenanceEnabled is True'),
            Result(state=State.OK, summary='SchedulerSuspended is False'),
            Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020')
        ]
    ),
    (
        {'SchedulerSuspended': (False, 1)},
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': True,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        [
            Result(state=State.OK, summary='SyncCycleEnabled is True'),
            Result(state=State.OK, summary='MaintenanceEnabled is True'),
            Result(state=State.WARN, summary='SchedulerSuspended is True'),
            Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020')
        ]
    ),
    (
        {'SchedulerSuspended': (False, -1), 'SyncCycleEnabled': (False, -1)},
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': True,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        [
            Result(state=State.OK, summary='MaintenanceEnabled is True'),
            Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020')
        ]
    ),
])
def test_check_win_adsync_scheduler(params, section, result):
    merged_params = DEFAULT_PARAMS
    merged_params.update(params)
    assert list(win_adsync_scheduler.check_win_adsync_scheduler(merged_params, section)) == result


@pytest.mark.parametrize('timezone, section, result', [
    (
        'Europe/Zurich',
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': True,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        Result(state=State.OK, summary='Next sync: Fri Jun  5 07:11:51 2020'),
    ),
    (
        'Europe/London',
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': True,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        Result(state=State.OK, summary='Next sync: Fri Jun  5 06:11:51 2020'),
    ),
    (
        'UTC',
        {
            'MaintenanceEnabled': True,
            'NextSyncCycleStartTimeInUTC': datetime(2020, 6, 5, 5, 11, 51, tzinfo=timezone.utc),
            'SchedulerSuspended': True,
            'StagingModeEnabled': False,
            'SyncCycleEnabled': True,
            'SyncCycleInProgress': False,
        },
        Result(state=State.OK, summary='Next sync: Fri Jun  5 05:11:51 2020'),
    ),
])
def test_check_win_adsync_scheduler_tz(timezone, section, result):
    oldtimezone = os.environ.get('TZ', None)
    os.environ['TZ'] = timezone
    time.tzset()

    output = list(win_adsync_scheduler.check_win_adsync_scheduler({}, section))

    if oldtimezone:
        os.environ['TZ'] = oldtimezone
    else:
        del os.environ['TZ']
    time.tzset()

    assert result in output
