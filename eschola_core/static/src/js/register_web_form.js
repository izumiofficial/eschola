/** @odoo-module */
import { markup } from "@odoo/owl";
import dom from "@web/legacy/js/core/dom";
import { cookie } from "@web/core/browser/cookie";;
import { loadWysiwygFromTextarea } from "@web_editor/js/frontend/loadWysiwygFromTextarea";
import publicWidget from "@web/legacy/js/public/public_widget";
import { session } from "@web/session";
import { escape } from "@web/core/utils/strings";
import { _t } from "@web/core/l10n/translation";
import { renderToElement } from "@web/core/utils/render";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";

console.log('Javascript File loaded successfully :D');
publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    selector: '.register_template_form',
    events: {
        'click .add_line': '_onClickAdd_line',
        'click .remove_line': '_onClickRemove_line',
        'click .create_record': '_onClickSubmit',
    },
    _onClickAdd_line: function(ev){
        var $new_card = $('.add_extra').clone(true);
        $new_card.removeClass('d-none');
        $new_card.removeClass('add_extra');
        $new_card.addClass('student_record');
        $new_card.insertBefore($('.add_extra'));
        console.log('New line created');
    },
    _onClickRemove_line: function(ev){
        $('#cloned_row').remove();
    },
    _onClickSubmit: function(ev){
        var self = this;
        var student_data = [];
        $('tr.student_record').each(function() {
            let name = $(this).find('input[name="name"]').val();
            let gender = $(this).find('select[name="gender"]').val();
            let email = $(this).find('input[name="email"]').val();
            let mobile = $(this).find('input[name="mobile"]').val();
            let grade = $(this).find('select[name="grade"]').val();
            let religion = $(this).find('select[name="religion"]').val();
            let country = $(this).find('select[name="country"]').val();
            let nationality = $(this).find('select[name="nationality"]').val();

            student_data.push({
                'name' : name,
                'gender' : gender,
                'email' : email,
                'mobile' : mobile,
                'grade' : grade,
                'religion' : religion,
                'country' : country,
                'nationality' : nationality,
            });
        });
        $('textarea[name="student_line_ids"]').val(JSON.stringify(student_data));
    },
});