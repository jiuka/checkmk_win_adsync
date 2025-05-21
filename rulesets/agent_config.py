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


from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    DefaultValue,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _parameter_form_win_adsync_bakery():
    return Dictionary(
        elements={
            'agent': DictElement(
                parameter_form=SingleChoice(
                    title=Title('Azure AD Connect Sync'),
                    help_text=Help('This will deploy the agent plugin <tt>win_adsync</tt> '
                                   'for checking Azure AD COnnect Sync.'),
                    elements=[
                        SingleChoiceElement(name='deploy', title=Title('Deploy Azure AD Connect Sync plugin')),
                        SingleChoiceElement(name='do_not_deploy', title=Title('Do not deploy Azure AD Connect Sync plugin')),
                    ],
                    prefill=DefaultValue('deploy'),
                ),
                required=True,
            )
        },
    )


rule_spec_win_adsync_bakery = AgentConfig(
    title=Title('Azure AD Connect Sync'),
    name='win_adsync',
    parameter_form=_parameter_form_win_adsync_bakery,
    topic=Topic.APPLICATIONS,
    help_text=Help('This will deploy the agent plugin <tt>win_adsync</tt> '
                   'for checking Azure AD COnnect Sync.'),
)
