if(typeof NA_Bootstrap == 'undefined') window.NA_Bootstrap = {}

NA_Bootstrap.dialog = {
    dialogConfirm: function (message, title, callTrue, callFalse, animate) {
        if (typeof BootstrapDialog != 'undefined') {
            return BootstrapDialog.confirm({
                title: title || NA.common.message.titleInfo,
                message: message,
                type: BootstrapDialog.TYPE_WARNING,
                size: BootstrapDialog.SIZE_SMALL,
                animate: animate || false,
                cssClass: 'login-dialog',
                closeByBackdrop: false,
                closeByKeyboard: false,
                closable: false,
                draggable: true,
                btnCancelLabel: 'NO.',
                btnOKLabel: 'Yes.',
                btnOKClass: 'btn-success',
                callback: function (result) {
                    if (result) {
                        if (callTrue) {
                            callTrue();
                        }
                    }
                    else {
                        if (callFalse) {
                            callFalse();
                        }
                    }
                },
                onshown: function (dialogRef) {
                    var divHeader = NA.common.doc.querySelector('div.modal-header:nth-child(1)');
                    divHeader.style.backgroundColor = 'green';
                }
            });
        }
    },

    dialogAlert: function (message, title, callback) {
        if (typeof BootstrapDialog != 'undefined') {
            return BootstrapDialog.alert({
                title: title || NA.common.message.titleInfo,
                message: message,
                size: BootstrapDialog.SIZE_SMALL,
                //animate:false,
                cssClass: 'login-dialog',
                closeByBackdrop: false,
                closeByKeyboard: false,
                type: BootstrapDialog.TYPE_INFO,
                closable: false,
                draggable: true,
                buttonLabel: 'OK',
                callback: function (result) {
                    if (result) {
                        if (callback) {
                            callback();
                        }
                        return true;
                    }
                },
                onshown: function (dialogRef) {
                    var divHeader = NA.common.doc.querySelector('div.modal-header:nth-child(1)');
                    divHeader.style.backgroundColor = 'green';
                }
            });
        }
    }
}