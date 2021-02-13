#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice,
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)

try:
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import (
        RulespecGroupMonitoringAgentsAgentPlugins
    )
except Exception:
    RulespecGroupMonitoringAgentsAgentPlugins = None


def _valuespec_agent_config_win_adsync():
    return DropdownChoice(
        title=_('Azure AD Connect Sync'),
        help=_('This will deploy the agent plugin <tt>win_adsync</tt> '
               'for checking Azure AD COnnect Sync.'),
        choices=[
            (True, _('Deploy Azure AD Connect Sync plugin')),
            (None, _('Do not deploy Azure AD Connect Sync plugin')),
        ],
    )


if RulespecGroupMonitoringAgentsAgentPlugins is not None:
    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name='agent_config:win_adsync',
            valuespec=_valuespec_agent_config_win_adsync,
        ))
