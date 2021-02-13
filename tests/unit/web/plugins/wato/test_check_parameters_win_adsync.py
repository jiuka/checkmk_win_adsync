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
import check_parameters_win_adsync
from cmk.gui.exceptions import MKUserError


@pytest.mark.parametrize('data', [
    ({'SyncCycleEnabled': (True, 1)}),
    ({'MaintenanceEnabled': (True, 1)}),
    ({'StagingModeEnabled': (True, 1)}),
    ({'SchedulerSuspended': (True, 1)}),
    ({'SyncCycleEnabled': (False, 1)}),
    ({'MaintenanceEnabled': (False, 2)}),
    ({'StagingModeEnabled': (False, 3)}),
    ({'SchedulerSuspended': (False, -1)}),
])
def test_vs_win_adsync_scheduler_accepts(data):
    vs = check_parameters_win_adsync._vs_win_adsync_scheduler()
    assert vs.validate_datatype(data, '') is None


@pytest.mark.parametrize('data', [
    ({'yolo': (True, 1)}),
    ({'MaintenanceEnabled': ('True', 1)}),
    ({'StagingModeEnabled': 1}),
])
def test_vs_win_adsync_scheduler_rejects(data):
    vs = check_parameters_win_adsync._vs_win_adsync_scheduler()
    with pytest.raises(MKUserError):
        vs.validate_datatype(data, '')


@pytest.mark.parametrize('data', [
    ({'duration': (1, 2)}),
])
def test_vs_win_adsync_connector(data):
    vs = check_parameters_win_adsync._vs_win_adsync_connector()
    assert vs.validate_datatype(data, '') is None


@pytest.mark.parametrize('data', [
    ({'duration': 1}),
    ({'foo': 1}),
])
def test_vs_win_adsync_connector_rejects(data):
    vs = check_parameters_win_adsync._vs_win_adsync_connector()
    with pytest.raises(MKUserError):
        vs.validate_datatype(data, '')
