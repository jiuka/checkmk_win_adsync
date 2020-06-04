#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    TextAscii,
    Tuple,
)
from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersApplications,
    CheckParameterRulespecWithItem,
    rulespec_registry,
)

def _vs_win_adsync_scheduler_state(title, expected, error_state):
    return Tuple(
        title=title,
        elements=[
            DropdownChoice(
                title=_('Expected value'),
                choices=[
                    (True, _('True')),
                    (False, _('False')),
                ],
                default_value=expected,
            ),
            DropdownChoice(
                title=_('Error state'),
                choices=[
                    (2, _('CRITICAL')),
                    (1, _('WARNING')),
                    (0, _('OK')),
                    (-1, _('IGNORE')),
                ],
                default_value=error_state,
            ),
        ]
    )

def _vs_win_adsync_scheduler():
    return Dictionary(
        title=_('Azure Ad Connect Sync Scheduler'),
        elements=[
            ('SyncCycleEnabled',
             _vs_win_adsync_scheduler_state(
                 title=_("Sync Cycle state"),
                 expected=True,
                 error_state=2)
            ),
            ('MaintenanceEnabled',
             _vs_win_adsync_scheduler_state(
                 title=_("Maintenance state"),
                 expected=True,
                 error_state=2)
            ),
            ('StagingModeEnabled',
             _vs_win_adsync_scheduler_state(
                 title=_("Staging mode"),
                 expected=False,
                 error_state=1)
            ),
            ('SchedulerSuspended',
             _vs_win_adsync_scheduler_state(
                 title=_("Scheduler suspended"),
                 expected=False,
                 error_state=1)
            ),
        ]
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="win_adsync_scheduler",
        group=RulespecGroupCheckParametersApplications,
        parameter_valuespec=_vs_win_adsync_scheduler,
        title=lambda: _("Azure AD Connect Sync Scheduler"),
    ))

def _vs_win_adsync_connector():
    return Dictionary(
        title=_('Azure AD Connect Connector'),
        elements=[
            ('duration',
             Tuple(
                 title=_("Maximal time the last sync took"),
                 elements=[
                     Age(title=_("Warning if longer than")),
                     Age(title=_("Critical if longer than")),
                 ],
            )),
        ]
    )

def _item_spec_win_adsync_connector():
    return TextAscii(
        title=_("Name of the Connector and the sync profile"),
        allow_empty=False,
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="win_adsync_connector",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_win_adsync_connector,
        parameter_valuespec=_vs_win_adsync_connector,
        title=lambda: _("Azure AD Connect Connector"),
    ))
