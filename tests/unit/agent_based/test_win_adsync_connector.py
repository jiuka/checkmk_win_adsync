#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# win_adsync_connector - Azure AD Connect Connector check
#
# Copyright (C) 2021  Marius Rieder <marius.rieder@scs.ch>
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
from cmk_addons.plugins.win_adsync.agent_based import win_adsync_connector


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        [
            ['cmk.com Delta Synchronization', 'success', '140', '05.12.2020 13:37:58', ''],
            ['cmk.com Export', 'completed-export-errors', '33', '05.12.2020 13:38:06', '']
        ],
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime(2020, 12, 5, 13, 37, 58, tzinfo=timezone.utc)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime(2020, 12, 5, 13, 38, 6, tzinfo=timezone.utc)
            ),
        }
    ),
])
def test_parse_win_adsync_connector(string_table, result):
    assert win_adsync_connector.parse_win_adsync_connector(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({}, []),
    (
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime(2020, 12, 5, 13, 37, 58, tzinfo=timezone.utc)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime(2020, 12, 5, 13, 38, 6, tzinfo=timezone.utc)
            ),
        },
        [
            Service(item='cmk.com Delta Synchronization'),
            Service(item='cmk.com Export')
        ]
    )
])
def test_discovery_win_adsync_connector(section, result):
    assert list(win_adsync_connector.discovery_win_adsync_connector(section)) == result


DEFAULT_PARAMS = {'duration': ('fixed', (300, 600))}


@pytest.mark.parametrize('timezone, section, result', [
    (
        'Europe/Zurich',
        {
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime(2020, 12, 5, 13, 38, 6, tzinfo=timezone.utc)
            ),
        },
        Result(state=State.OK, summary='Last sync: 2 hours 21 minutes'),
    ),
    (
        'Europe/London',
        {
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime(2020, 12, 5, 13, 38, 6, tzinfo=timezone.utc)
            ),
        },
        Result(state=State.OK, summary='Last sync: 2 hours 21 minutes'),
    ),
])
def test_check_win_adsync_connector_tz(freezer, timezone, section, result):
    freezer.move_to('2020-12-05 16:00')
    oldtimezone = os.environ.get('TZ', None)
    os.environ['TZ'] = timezone
    time.tzset()

    output = list(win_adsync_connector.check_win_adsync_connector('cmk.com Export', DEFAULT_PARAMS, section))

    if oldtimezone:
        os.environ['TZ'] = oldtimezone
    else:
        del os.environ['TZ']
    time.tzset()

    assert result in output
