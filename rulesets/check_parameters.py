#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    LevelsType,
    migrate_to_integer_simple_levels,
    ServiceState,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition, HostCondition


def migrate_adsync_schedule_state(value: dict | tuple) -> dict:
    if isinstance(value, dict):
        return value

    return dict(
        expected=value[0],
        error_state=value[1],
    )


def ADSyncScheduleStateDictElement(title, expected, error_state):
    return DictElement(
        parameter_form=Dictionary(
            title=Title(title),
            elements={
                'expected': DictElement(
                    parameter_form=BooleanChoice(
                        title=Title('Expected value'),
                        prefill=DefaultValue(expected),
                    )
                ),
                'error_state': DictElement(
                    parameter_form=ServiceState(
                        title=Title('Error value'),
                        prefill=DefaultValue(error_state),
                    )
                ),
            },
            migrate=migrate_adsync_schedule_state,
        )
    )


def _parameter_win_adsync_scheduler():
    return Dictionary(
        elements={
            'SyncCycleEnabled': ADSyncScheduleStateDictElement(
                title='Sync Cycle state',
                expected=True,
                error_state=2
            ),
            'MaintenanceEnabled': ADSyncScheduleStateDictElement(
                title='Maintenance state',
                expected=True,
                error_state=2
            ),
            'StagingModeEnabled': ADSyncScheduleStateDictElement(
                title='Staging mode',
                expected=True,
                error_state=1
            ),
            'SchedulerSuspended': ADSyncScheduleStateDictElement(
                title='Scheduler suspended',
                expected=False,
                error_state=1
            ),
        },
    )


rule_specwin_adsync_scheduler = CheckParameters(
    name='win_adsync_scheduler',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_win_adsync_scheduler,
    title=Title('Azure Ad Connect Sync Scheduler'),
    condition=HostCondition(),
)


def _parameter_win_adsync_connector():
    return Dictionary(
        elements={
            'duration': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Maximal time the last sync took'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.HOUR, TimeMagnitude.MINUTE, TimeMagnitude.SECOND]
                    ),
                    prefill_fixed_levels=DefaultValue(LevelsType.FIXED),
                    migrate=migrate_to_integer_simple_levels,
                ),
                required=False,
            ),
        }
    )


rule_spec_win_adsync_connector = CheckParameters(
    name='win_adsync_connector',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_win_adsync_connector,
    title=Title('Azure AD Connect Connector'),
    condition=HostAndItemCondition(item_title=Title('Name of the Connector and the sync profile')),
)
