/** @odoo-module */

import { calendarView } from '@web/views/calendar/calendar_view';

import { SessionCalendarController } from './session_calendar_controller';

import { registry } from '@web/core/registry';

const SessionCalendarView = {
    ...calendarView,

    Controller: SessionCalendarController,
}

registry.category('views').add('session_calendar', SessionCalendarView);