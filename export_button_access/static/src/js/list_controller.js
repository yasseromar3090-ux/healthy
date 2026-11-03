odoo.define('export_button_access.hide_export', function (require) {
"use strict";

var session = require('web.session');
var core = require('web.core');

// Hide export button for users without permission
core.bus.on('web_client_ready', null, function () {
    session.user_has_group('export_button_access.group_export_data').then(function(has_group) {
        if (!has_group) {
            // Add CSS to hide export elements
            var style = document.createElement('style');
            style.textContent = `
                .o_cp_action_menus .o_dropdown_item[data-menu="export"],
                .o_cp_action_menus a:contains('Export'),
                button[data-section="other"][data-index="export"],
                .o_list_export_xlsx {
                    display: none !important;
                }
            `;
            document.head.appendChild(style);
        }
    });
});

});
