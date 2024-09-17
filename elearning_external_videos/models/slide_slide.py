# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import io
import requests
import PyPDF2
from odoo import api, fields, models, _
from werkzeug import urls
import hashlib
import hmac
import re
import time
from odoo.exceptions import UserError, AccessError, ValidationError
import mimetypes
from odoo.tools.mimetypes import guess_mimetype

class Channel(models.Model):
    """ A channel is a container of slides. """
    _inherit = 'slide.channel'
    _name = 'slide.channel'

    nbr_clapprvideo = fields.Integer('External Videos (livestream and other supported)', compute='_compute_slides_statistics', store=True)
    nbr_localvideo = fields.Integer('Local Video', compute='_compute_slides_statistics', store=True)
    nbr_local_external = fields.Integer('Local and External Videos', compute='_compute_slides_statistics', store=True)

class Slide(models.Model):
    _inherit = 'slide.slide'

    # content
    slide_category = fields.Selection(
                        selection_add=[('local_external', 'Local or External Video')],
                        ondelete={
                            'local_external': 'cascade'})
    external_default_type = fields.Selection(selection=[
        ('clapprvideo', 'External video (mp4, etc, livestream m3u8 and other supported formats)'),
        ('localvideo', 'Local Video (Ensure upload size limit in your server)')],
        ondelete={'clapprvideo': 'cascade',
                  'localvideo': 'cascade'},
        default=None)
    slide_type = fields.Selection(selection_add=[
        ('clapprvideo', 'External video (mp4, etc, livestream m3u8 and other supported formats)'),
        ('localvideo', 'Local Video (Ensure upload size limit in your server)')])
    external_url = fields.Char(string="External video URL")
    localvideo_mimetype = fields.Char(string="Localvideo mime type")
    nbr_clapprvideo = fields.Integer('External Video (livestream and other supported)', compute='_compute_slides_statistics', store=True)
    nbr_localvideo = fields.Integer('Local Video', compute='_compute_slides_statistics', store=True)
    nbr_local_external = fields.Integer('Local and External Videos', compute='_compute_slides_statistics', store=True)
    video_source_type = fields.Selection(selection_add=[
        ('clapprvideo', 'External video (mp4, etc, livestream m3u8 and other supported formats)'),
        ('localvideo', 'Local Video (Ensure upload size limit in your server)')],
    )
    video_binary_content = fields.Binary('Video Content', readonly=False) # Used to filter file input to videos only
    localvideo_filename = fields.Char('Video Filename')
    video_attachment = fields.Many2one('ir.attachment', string='Video Content', attachment=True, readonly=False) # Used to filter file input to videos only

    @api.onchange('external_default_type', 'slide_category')
    def onchange_external_default_type(self):
        if self.slide_category == 'local_external' and self.external_default_type:
            self.slide_type = self.external_default_type


    @api.depends('slide_category', 'google_drive_id', 'video_source_type', 'youtube_id')
    def _compute_embed_code(self):
        res = super(Slide, self)._compute_embed_code()
        for record in self:
            if record.slide_type == 'clapprvideo':
                content_url = record.external_url
                record.embed_code = content_url
            '''if record.slide_type == 'zoom_meeting':
                config = self.env['ir.config_parameter'].sudo()
                config_elearning_zoom_integration = config.get_param('elearning_zoom_integration')
                if config_elearning_zoom_integration:
                    zoom_api_key = config.get_param('elearning_zoom_api_key')
                    zoom_api_secret = config.get_param('elearning_zoom_api_secret')
                    zoom_data = {'apiKey': zoom_api_key.strip(),
                                 'apiSecret': zoom_api_secret.strip(),
                                 'meetingNumber': record.zoom_meeting_ID.strip(),
                                 'role': 0}  # role 0 is atendee
                    zoom_signature = self.generateZoomSignature(zoom_data)
                    current_user_name = 'Username'
                    zoom_name = str(base64.b64encode(current_user_name.encode('utf-8')), 'utf-8')
                    content_url = '/elearning_external_videos/static/meeting.html?name=' + zoom_name + '&mn=' + record.zoom_meeting_ID.strip() + '&email=&pwd=' + record.zoom_meeting_pwd.strip() + '&role=0&lang=es-ES&signature=' + zoom_signature + '&china=0&apiKey=' + zoom_api_key + ''
                    record.embed_code = '<!--<div class="hidecontrols"></div>--><iframe allow="microphone; camera; fullscreen" id="zoom_meeting_' + str(
                        record.id) + '" class="external_video" src="' + content_url + '" frameborder="0" wmode="transparent" oncontextmenu="return false"></iframe>'
                else:
                    raise ValidationError('You must enable Zoom Meetings in Elearning/Settings')'''
            if record.slide_type == 'localvideo':
                content_url = self.env['ir.config_parameter'].get_param('web.base.url') + '/web/content/%s' % str(record.video_attachment.id)
                record.embed_code = '<video class="local_video" controls controlsList="nodownload"><source src="' + content_url + '" type="' + record.localvideo_mimetype + '"/></video>'

    @api.onchange('slide_type', 'external_url')
    def onchange_slide_type(self):
        for record in self:
            if record.slide_type == 'zoom_meeting':
                config = self.env['ir.config_parameter'].sudo()
                config_elearning_zoom_integration = config.get_param('elearning_zoom_integration')
                if not config_elearning_zoom_integration:
                    raise ValidationError('You must enable Zoom Meetings in Elearning/Settings')

    #@api.onchange('video_binary_content')
    def _on_change_datas(self):
        vals = {
            "video/mp4": b'MPEG-4',
            "video/webm": b'libVorbis',
            "video/ogg": b'Ogg'
        }
        if self.video_binary_content and self.localvideo_mimetype:
            if self.slide_type == 'localvideo':
                if self.localvideo_mimetype not in ["video/mp4", "video/webm", "video/ogg"]:
                    self.video_binary_content = False
                    return {
                            'warning': {
                                'title': 'Warning!',
                                'message': 'The media file format is not supported. Please upload only mp4, ogg or webm files.'
                            }
                    }
    
    @api.depends('video_url')
    def _compute_video_source_type(self):
        for slide in self:
            video_source_type = False
            youtube_match = re.match(self.YOUTUBE_VIDEO_ID_REGEX, slide.video_url) if slide.video_url else False
            if youtube_match and len(youtube_match.groups()) == 2 and len(youtube_match.group(2)) == 11:
                video_source_type = 'youtube'
            if slide.video_url and not video_source_type and re.match(self.GOOGLE_DRIVE_DOCUMENT_ID_REGEX, slide.video_url):
                video_source_type = 'google_drive'
            vimeo_match = re.search(self.VIMEO_VIDEO_ID_REGEX, slide.video_url) if slide.video_url else False
            if not video_source_type and vimeo_match and len(vimeo_match.groups()) == 3:
                video_source_type = 'vimeo'
            if slide.slide_type == 'clapprvideo':
                video_source_type = 'clapprvideo'
            if slide.slide_type == 'localvideo':
                video_source_type = 'localvideo'

            slide.video_source_type = video_source_type

    @api.model
    def create(self, vals):
        res = super(Slide, self).create(vals)
        if res:
            if res.video_binary_content:
                attach_id = self.env['ir.attachment'].create({
                                                    'name': res.localvideo_filename,
                                                    'datas': res.video_binary_content,
                                                    'res_model': 'slide.slide',
                                                    'res_id': res.id,
                                                    'public': True})
                if attach_id:
                    res.video_attachment = attach_id.id
                    res.localvideo_mimetype = attach_id.mimetype
            '''if res.video_attachment:
                res.video_attachment.public = True'''
        return res
    

    def write(self, vals):
        res = super(Slide, self).write(vals)
        if res:
            for rec in self:
                if vals.get('video_binary_content', False):
                    rec.video_attachment.sudo().unlink()
                    attach_id = self.env['ir.attachment'].create({
                                                        'name': rec.localvideo_filename,
                                                        'datas': rec.video_binary_content,
                                                        'res_model': 'slide.slide',
                                                        'res_id': rec.id,
                                                        'public': True})
                    if attach_id:
                        rec.video_attachment = attach_id.id
                        rec.localvideo_mimetype = attach_id.mimetype
                '''if vals.get('video_attachment', False):
                    rec.video_attachment.public = True'''
        return res
