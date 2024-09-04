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
        // Count the number of existing clones
        var numClones = $('.add_extra_card').length - 1; // Subtract 1 to exclude the original

        if (numClones < 4) {
            var $new_card = $('.add_extra_card').clone(true);
            $new_card.removeClass('d-none');
            $new_card.removeClass('add_extra_card');
            $new_card.insertBefore($('.add_extra_card'));
            console.log('New card created');
        } else {
            ev.preventDefault();
            console.log('Maximum number of entries reached');
            alert('Maximum number of entries reached');
            $(ev.target).prop('disabled', true);
        }
    },
    _onClickRemove_line: function(ev){
        $('#cloned_row').remove();
    },
    _onClickSubmit: async function(ev){
        var self = this;

    },
});