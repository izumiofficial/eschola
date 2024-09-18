import logging
import math
from datetime import datetime, timedelta
from itertools import repeat
from werkzeug.urls import url_parse

import pytz
import uuid

from odoo import api, fields, models
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.calendar.models.calendar_recurrence import (
    weekday_to_field,
    RRULE_TYPE_SELECTION,
    END_TYPE_SELECTION,
    MONTH_BY_SELECTION,
    WEEKDAY_SELECTION,
    BYDAY_SELECTION
)

RRULE_TYPE_SELECTION_UI = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
    ('custom', 'Custom')
]

def get_weekday_occurence(date):
    """
    :returns: ocurrence

    >>> get_weekday_occurence(date(2019, 12, 17))
    3  # third Tuesday of the month

    >>> get_weekday_occurence(date(2019, 12, 25))
    -1  # last Friday of the month
    """
    occurence_in_month = math.ceil(date.day/7)
    if occurence_in_month in {4, 5}:  # fourth or fifth week on the month -> last
        return -1
    return occurence_in_month


class Session(models.Model):
    _name = "session"
    _description = "Session"

    @api.model
    def _default_start(self):
        now = fields.Datetime.now()
        return now + (datetime.min - now) % timedelta(minutes=30)

    @api.model
    def _default_stop(self):
        now = fields.Datetime.now()
        start = now + (datetime.min - now) % timedelta(minutes=30)
        return start + timedelta(hours=1)

    name = fields.Char(string='Name')
    start_datetime = fields.Datetime(string='Start Date')
    end_datetime = fields.Datetime(string='End Date')
    course_id = fields.Many2one('slide.channel', string='Course')
    recurrency = fields.Boolean('Recurrent')
    recurrence_id = fields.Many2one(
        'calendar.recurrence', string="Recurrence Rule")
    start = fields.Datetime(
        'Start', required=True, tracking=True, default=_default_start,
        help="Start date of an event, without time for full days events")
    stop = fields.Datetime(
        'Stop', required=True, tracking=True, default=_default_start,
        compute='_compute_stop', readonly=False, store=True,
        help="Stop date of an event, without time for full days events")
    display_time = fields.Char('Event Time', compute='_compute_display_time')
    allday = fields.Boolean('All Day', default=False)
    start_date = fields.Date(
        'Start Date', store=True, tracking=True,
        compute='_compute_dates', inverse='_inverse_dates')
    stop_date = fields.Date(
        'End Date', store=True, tracking=True,
        compute='_compute_dates', inverse='_inverse_dates')
    duration = fields.Float('Duration', compute='_compute_duration', store=True, readonly=False)
    rrule = fields.Char('Recurrent Rule', compute='_compute_recurrence', readonly=False)
    rrule_type_ui = fields.Selection(RRULE_TYPE_SELECTION_UI, string='Repeat',
                                     compute="_compute_rrule_type_ui",
                                     readonly=False,
                                     help="Let the event automatically repeat at that interval")
    rrule_type = fields.Selection(RRULE_TYPE_SELECTION, string='Recurrence',
                                  help="Let the event automatically repeat at that interval",
                                  compute='_compute_recurrence', readonly=False)
    event_tz = fields.Selection(
        _tz_get, string='Timezone', compute='_compute_recurrence', readonly=False)
    end_type = fields.Selection(
        END_TYPE_SELECTION, string='Recurrence Termination',
        compute='_compute_recurrence', readonly=False)
    interval = fields.Integer(
        string='Repeat On', compute='_compute_recurrence', readonly=False,
        help="Repeat every (Days/Week/Month/Year)")
    count = fields.Integer(
        string='Number of Repetitions', help="Repeat x times", compute='_compute_recurrence', readonly=False)
    mon = fields.Boolean(compute='_compute_recurrence', readonly=False)
    tue = fields.Boolean(compute='_compute_recurrence', readonly=False)
    wed = fields.Boolean(compute='_compute_recurrence', readonly=False)
    thu = fields.Boolean(compute='_compute_recurrence', readonly=False)
    fri = fields.Boolean(compute='_compute_recurrence', readonly=False)
    sat = fields.Boolean(compute='_compute_recurrence', readonly=False)
    sun = fields.Boolean(compute='_compute_recurrence', readonly=False)
    month_by = fields.Selection(
        MONTH_BY_SELECTION, string='Option', compute='_compute_recurrence', readonly=False)
    day = fields.Integer('Date of month', compute='_compute_recurrence', readonly=False)
    weekday = fields.Selection(WEEKDAY_SELECTION, compute='_compute_recurrence', readonly=False)
    byday = fields.Selection(BYDAY_SELECTION, string="By day", compute='_compute_recurrence', readonly=False)
    until = fields.Date(compute='_compute_recurrence', readonly=False)

    user_can_edit = fields.Boolean(compute='_compute_user_can_edit')

    def _compute_display_time(self):
        for meeting in self:
            meeting.display_time = self._get_display_time(meeting.start, meeting.stop, meeting.duration, meeting.allday)

    @api.depends('allday', 'start', 'stop')
    def _compute_dates(self):
        """ Adapt the value of start_date(time)/stop_date(time)
            according to start/stop fields and allday. Also, compute
            the duration for not allday meeting ; otherwise the
            duration is set to zero, since the meeting last all the day.
        """
        for meeting in self:
            if meeting.allday and meeting.start and meeting.stop:
                meeting.start_date = meeting.start.date()
                meeting.stop_date = meeting.stop.date()
            else:
                meeting.start_date = False
                meeting.stop_date = False

    @api.depends('stop', 'start')
    def _compute_duration(self):
        for event in self:
            event.duration = self._get_duration(event.start, event.stop)

    @api.depends('start', 'duration')
    def _compute_stop(self):
        # stop and duration fields both depends on the start field.
        # But they also depends on each other.
        # When start is updated, we want to update the stop datetime based on
        # the *current* duration. In other words, we want: change start => keep the duration fixed and
        # recompute stop accordingly.
        # However, while computing stop, duration is marked to be recomputed. Calling `event.duration` would trigger
        # its recomputation. To avoid this we manually mark the field as computed.
        duration_field = self._fields['duration']
        self.env.remove_to_compute(duration_field, self)
        for event in self:
            # Round the duration (in hours) to the minute to avoid weird situations where the event
            # stops at 4:19:59, later displayed as 4:19.
            event.stop = event.start and event.start + timedelta(minutes=round((event.duration or 1.0) * 60))
            if event.allday:
                event.stop -= timedelta(seconds=1)

    @api.depends('recurrence_id', 'recurrency')
    def _compute_rrule_type_ui(self):
        defaults = self.env["calendar.recurrence"].default_get(["interval", "rrule_type"])
        for event in self:
            if event.recurrency:
                if event.recurrence_id:
                    event.rrule_type_ui = 'custom' if event.recurrence_id.interval != 1 else (event.recurrence_id.rrule_type)
                else:
                    event.rrule_type_ui = defaults["rrule_type"]

    @api.depends('recurrence_id', 'recurrency', 'rrule_type_ui')
    def _compute_recurrence(self):
        recurrence_fields = self._get_recurrent_fields()
        false_values = {field: False for field in recurrence_fields}  # computes need to set a value
        defaults = self.env['calendar.recurrence'].default_get(recurrence_fields)
        default_rrule_values = self.recurrence_id.default_get(recurrence_fields)
        for event in self:
            if event.recurrency:
                current_rrule = (event.rrule_type if event.rrule_type_ui == "custom" else event.rrule_type_ui)
                event.update(defaults)  # default recurrence values are needed to correctly compute the recurrence params
                event_values = event._get_recurrence_params()
                rrule_values = {
                    field: event.recurrence_id[field]
                    for field in recurrence_fields
                    if event.recurrence_id[field]
                }
                rrule_values = rrule_values or default_rrule_values
                rrule_values['rrule_type'] = current_rrule or rrule_values.get('rrule_type') or defaults['rrule_type']
                event.update({**false_values, **defaults, **event_values, **rrule_values})
            else:
                event.update(false_values)

    def _inverse_dates(self):
        """ This method is used to set the start and stop values of all day events.
            The calendar view needs date_start and date_stop values to display correctly the allday events across
            several days. As the user edit the {start,stop}_date fields when allday is true,
            this inverse method is needed to update the  start/stop value and have a relevant calendar view.
        """
        for meeting in self:
            if meeting.allday:

                # Convention break:
                # stop and start are NOT in UTC in allday event
                # in this case, they actually represent a date
                # because fullcalendar just drops times for full day events.
                # i.e. Christmas is on 25/12 for everyone
                # even if people don't celebrate it simultaneously
                enddate = fields.Datetime.from_string(meeting.stop_date)
                enddate = enddate.replace(hour=18)

                startdate = fields.Datetime.from_string(meeting.start_date)
                startdate = startdate.replace(hour=8)  # Set 8 AM

                meeting.write({
                    'start': startdate.replace(tzinfo=None),
                    'stop': enddate.replace(tzinfo=None)
                })

    def _compute_user_can_edit(self):
        for event in self:
            # By default, only current attendees and the organizer can edit the event.
            editor_candidates = event.partner_ids.user_ids + event.user_id
            # Right before saving the event, old partners must be able to save changes.
            if event._origin:
                editor_candidates += event._origin.partner_ids.user_ids
            event.user_can_edit = self.env.user.id in editor_candidates.ids

    @api.model
    def _get_recurrent_fields(self):
        return {'byday', 'until', 'rrule_type', 'month_by', 'event_tz', 'rrule',
                'interval', 'count', 'end_type', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat',
                'sun', 'day', 'weekday'}

    def _get_recurrence_params(self):
        if not self:
            return {}
        event_date = self._get_start_date()
        weekday_field_name = weekday_to_field(event_date.weekday())
        return {
            weekday_field_name: True,
            'weekday': weekday_field_name.upper(),
            'byday': str(get_weekday_occurence(event_date)),
            'day': event_date.day,
        }

    def _get_start_date(self):
        """Return the event starting date in the event's timezone.
        If no starting time is assigned (yet), return today as default
        :return: date
        """
        if not self.start:
            return fields.Date.today()
        if self.recurrency and self.event_tz:
            tz = pytz.timezone(self.event_tz)
            # Ensure that all day events date are not calculated around midnight. TZ shift would potentially return bad date
            start = self.start if not self.allday else self.start.replace(hour=12)
            return pytz.utc.localize(start).astimezone(tz).date()
        return self.start.date()

    def _get_duration(self, start, stop):
        """ Get the duration value between the 2 given dates. """
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)
