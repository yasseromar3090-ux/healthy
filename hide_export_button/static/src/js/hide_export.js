odoo.define('hide_export_button.hide_export', function (require) {
"use strict";

var Sidebar = require('web.Sidebar');
var session = require('web.session');

Sidebar.include({
    start: function () {
        var self = this;
        var _super = this._super.bind(this);
        
        // Check permission before rendering
        return session.user_has_group('hide_export_button.group_show_export_button').then(function(has_group) {
            // Filter out export items if user doesn't have permission
            if (!has_group && self.items && self.items.other) {
                self.items.other = _.filter(self.items.other, function(item) {
                    return item.label !== 'Export';
                });
            }
            return _super.apply(self, arguments);
        });
    },
});

});
