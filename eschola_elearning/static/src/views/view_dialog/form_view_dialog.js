/** @odoo-module */

import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";

import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";

import { formView } from '@web/views/form/form_view';
import { FormController } from '@web/views/form/form_controller';

//import { useLeaveCancelWizard } from '../hooks';

export class SessionDialogFormController extends FormController {

    setup() {
        super.setup();
//        this.leaveCancelWizard = useLeaveCancelWizard();
        this.orm = useService("orm");
    }

    async onClick(action) {
        await this.orm.call("generate.time.table");
        this.props.onLeaveUpdated();
    }
}

SessionDialogFormController.props = {
    ...FormController.props,
}

registry.category('views').add('session_dialog_form', {
    ...formView,
    Controller: SessionDialogFormController,
});

export class SessionFormViewDialog extends FormViewDialog {
    setup() {
        super.setup();

        this.viewProps = Object.assign(this.viewProps, {
            type: "session_dialog_form",
        })
    }
}

SessionFormViewDialog.props = {
    ...SessionFormViewDialog.props,
}