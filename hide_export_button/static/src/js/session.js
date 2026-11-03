odoo.define('hide_export_button.session', function (require) {
"use strict";

var Session = require('web.Session');

Session.include({
    load_modules: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function() {
            return self.user_has_group('hide_export_button.group_show_export_button').then(function(has_group) {
                self.show_export_button = has_group;
            });
        });
    },
});

});
