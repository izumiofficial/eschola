/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { SessionFormViewDialog } from "../view_dialog/form_view_dialog";
import { CalendarQuickCreate } from "@calendar/views/calendar_form/calendar_quick_create";

export class SessionCalendarController extends CalendarController {

    setup() {
        super.setup();
        this.actionService = useService("action");
        this.user = useService("user");
        this.orm = useService("orm");
        onWillStart(async () => {
            this.isSystemUser = await this.user.hasGroup('base.group_system');
        });
    }

    onClickGenerateSessionButton() {
        console.log('Generate la woi');
        this.displayDialog(SessionFormViewDialog, {
            resModel: "generate.time.table",
            title: _t("Generate New Session"),
            viewId: this.model.formViewId,
        });
//        this.actionService.doAction({
//            type: 'ir.actions.act_window',
//            res_model: 'generate.time.table',
//            views: [[false, 'form']],
//        });
    }

}

SessionCalendarController.template = "eschola_elearning.CalendarController";