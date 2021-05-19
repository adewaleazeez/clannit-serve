"use strict";
var type = [ 'primary', 'info', 'success', 'warning', 'danger' ];

function showNotification(from, align) {
    "use strict";
    var color = Math.floor((Math.random() * 4) + 1);
    $.notify({
        icon   : "icon-bell icons",
        message: "Welcome to <b>PVR Lite Admin</b> - a beautiful bootstrap 4 dashboard."
    }, {
        type     : type[ color ],
        timer    : 8000,
        placement: {
            from : from,
            align: align
        }
    });
}

var Toastr = function () {
        "use strict";
        $(function () {
            var i = -1;
            var toastCount = 0;
            var $toastlast;

            var getMessage = function () {
                var msgs = [ 'My name is Inigo Montoya. You killed my father. Prepare to die!',
                    '<div><input class="input-small" value="textbox"/>&nbsp;<a href="javascript:void(0)" target="_blank">This is a hyperlink</a></div><div><button type="button" id="okBtn" class="btn btn-primary">Close me</button><button type="button" id="surpriseBtn" class="btn" style="margin: 0 8px 0 8px">Surprise me</button></div>',
                    'Are you the six fingered man?',
                    'Inconceivable!',
                    'I do not think that means what you think it means.',
                    'Have fun storming the castle!'
                ];
                i++;
                if (i === msgs.length) {
                    i = 0;
                }

                return msgs[ i ];
            };

            var getMessageWithClearButton = function (msg) {
                msg = msg ? msg : 'Clear itself?';
                msg += '<br /><br /><button type="button" class="btn clear">Yes</button>';
                return msg;
            };

            $('#closeButton').click(function () {
                if ($(this).is(':checked')) {
                    $('#addBehaviorOnToastCloseClick').prop('disabled', false);
                } else {
                    $('#addBehaviorOnToastCloseClick').prop('disabled', true);
                    $('#addBehaviorOnToastCloseClick').prop('checked', false);
                }
            });

            $('#showtoast').click(function () {
                var shortCutFunction = $("#toastTypeGroup input:radio:checked").val();
                var msg = $('#message').val();
                var title = $('#title').val() || '';
                var $showDuration = $('#showDuration');
                var $hideDuration = $('#hideDuration');
                var $timeOut = $('#timeOut');
                var $extendedTimeOut = $('#extendedTimeOut');
                var $showEasing = $('#showEasing');
                var $hideEasing = $('#hideEasing');
                var $showMethod = $('#showMethod');
                var $hideMethod = $('#hideMethod');
                var toastIndex = toastCount++;
                var addClear = $('#addClear').prop('checked');

                toastr.options = {
                    closeButton      : $('#closeButton').prop('checked'),
                    debug            : $('#debugInfo').prop('checked'),
                    newestOnTop      : $('#newestOnTop').prop('checked'),
                    progressBar      : $('#progressBar').prop('checked'),
                    rtl              : $('#rtl').prop('checked'),
                    positionClass    : $('#positionGroup input:radio:checked').val() || 'toast-top-right',
                    preventDuplicates: $('#preventDuplicates').prop('checked'),
                    onclick          : null
                };

                if ($('#addBehaviorOnToastClick').prop('checked')) {
                    toastr.options.onclick = function () {
                        alert('You can perform some custom action after a toast goes away');
                    };
                }

                if ($('#addBehaviorOnToastCloseClick').prop('checked')) {
                    toastr.options.onCloseClick = function () {
                        alert('You can perform some custom action when the close button is clicked');
                    };
                }

                if ($showDuration.val().length) {
                    toastr.options.showDuration = parseInt($showDuration.val());
                }

                if ($hideDuration.val().length) {
                    toastr.options.hideDuration = parseInt($hideDuration.val());
                }

                if ($timeOut.val().length) {
                    toastr.options.timeOut = addClear ? 0 : parseInt($timeOut.val());
                }

                if ($extendedTimeOut.val().length) {
                    toastr.options.extendedTimeOut = addClear ? 0 : parseInt($extendedTimeOut.val());
                }

                if ($showEasing.val().length) {
                    toastr.options.showEasing = $showEasing.val();
                }

                if ($hideEasing.val().length) {
                    toastr.options.hideEasing = $hideEasing.val();
                }

                if ($showMethod.val().length) {
                    toastr.options.showMethod = $showMethod.val();
                }

                if ($hideMethod.val().length) {
                    toastr.options.hideMethod = $hideMethod.val();
                }

                if (addClear) {
                    msg = getMessageWithClearButton(msg);
                    toastr.options.tapToDismiss = false;
                }
                if (!msg) {
                    msg = getMessage();
                }

                $('#toastrOptions').text('Command: toastr["'
                    + shortCutFunction
                    + '"]("'
                    + msg
                    + (title ? '", "' + title : '')
                    + '")\n\ntoastr.options = '
                    + JSON.stringify(toastr.options, null, 2)
                );

                var $toast = toastr[ shortCutFunction ](msg, title);
                $toastlast = $toast;

                if (typeof $toast === 'undefined') {
                    return;
                }

                if ($toast.find('#okBtn').length) {
                    $toast.delegate('#okBtn', 'click', function () {
                        alert('you clicked me. i was toast #' + toastIndex + '. goodbye!');
                        $toast.remove();
                    });
                }
                if ($toast.find('#surpriseBtn').length) {
                    $toast.delegate('#surpriseBtn', 'click', function () {
                        alert('Surprise! you clicked me. i was toast #' + toastIndex + '. You could perform an action here.');
                    });
                }
                if ($toast.find('.clear').length) {
                    $toast.delegate('.clear', 'click', function () {
                        toastr.clear($toast, {force: true});
                    });
                }
            });

            function getLastToast() {
                return $toastlast;
            }

            $('#clearlasttoast').click(function () {
                toastr.clear(getLastToast());
            });
            $('#cleartoasts').click(function () {
                toastr.clear();
            });
        });
    },
    Notification = function () {
        "use strict";
        return {
            init: function () {
                Toastr()
            }
        }
    }();
$(function () {
    Notification.init();
});