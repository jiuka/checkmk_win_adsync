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
import datetime
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import win_adsync_connector


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        [
            ['cmk.com Delta Synchronization', 'success', '140', '05.12.2020 13:37:58', ''],
            ['cmk.com Export', 'completed-export-errors', '33', '05.12.2020 13:38:06', '']
        ],
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
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
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
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


DEFAULT_PARAMS = {'duration': (300, 600)}


@pytest.mark.parametrize('item, params, section, result', [
    (
        '',
        {},
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
            ),
        },
        []
    ),
    (
        'cmk.com Delta Synchronization',
        {},
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
            ),
        },
        [
            Result(state=State.OK, summary='State: Success'),
            Result(state=State.OK, summary='Last sync: Sat Dec  5 13:37:58 2020'),
            Result(state=State.OK, summary='Sync duration: 2 minutes 20 seconds'),
            Metric('duration', 140.0, levels=(300.0, 600.0))
        ]
    ),
    (
        'cmk.com Delta Synchronization',
        {'duration': (100, 200)},
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
            ),
        },
        [
            Result(state=State.OK, summary='State: Success'),
            Result(state=State.OK, summary='Last sync: Sat Dec  5 13:37:58 2020'),
            Result(state=State.WARN, summary='Sync duration: 2 minutes 20 seconds (warn/crit at 1 minute 40 seconds/3 minutes 20 seconds)'),
            Metric('duration', 140.0, levels=(100.0, 200.0))
        ]
    ),
    (
        'cmk.com Delta Synchronization',
        {'duration': (100, 110)},
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
            ),
        },
        [
            Result(state=State.OK, summary='State: Success'),
            Result(state=State.OK, summary='Last sync: Sat Dec  5 13:37:58 2020'),
            Result(state=State.CRIT, summary='Sync duration: 2 minutes 20 seconds (warn/crit at 1 minute 40 seconds/1 minute 50 seconds)'),
            Metric('duration', 140.0, levels=(100.0, 110.0))
        ]
    ),
    (
        'cmk.com Export',
        {},
        {
            'cmk.com Delta Synchronization': win_adsync_connector.AdsyncConnector(
                'success', 140, datetime.datetime(2020, 12, 5, 13, 37, 58)
            ),
            'cmk.com Export': win_adsync_connector.AdsyncConnector(
                'completed-export-errors', 33, datetime.datetime(2020, 12, 5, 13, 38, 6)
            ),
        },
        [
            Result(state=State.WARN, summary='State: completed-export-errors'),
            Result(state=State.OK, summary='Last sync: Sat Dec  5 13:38:06 2020'),
            Result(state=State.OK, summary='Sync duration: 33 seconds'),
            Metric('duration', 33.0, levels=(300.0, 600.0))
        ]
    ),
])
def test_check_win_adsync_connector(item, params, section, result):
    merged_params = DEFAULT_PARAMS.copy()
    merged_params.update(params)
    assert list(win_adsync_connector.check_win_adsync_connector(item, merged_params, section)) == result
