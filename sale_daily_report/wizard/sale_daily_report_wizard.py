# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat
from datetime import date, datetime
import time


class StockCardReportWizard(models.TransientModel):
    _name = 'sale.daily.report.wizard'
    _description = 'sale daily Report Wizard'

    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Period',
    )
    date_from = fields.Date(
        string='Date',
        required=True,
    )
    date_to = fields.Date(
        string='End Date',
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',

    )
    users_ids = fields.Many2many(
        comodel_name='res.users',
        string='Salesman',
        required=True,
    )

    @api.onchange('date_range_id')
    def _onchange_date_range_id(self):
        self.date_from = self.date_range_id.date_start
        self.date_to = self.date_range_id.date_end

    @api.multi

    def custom_button(self):
        self.env.cr.execute("delete from public.test_daily_report")
        #self.env.cr.execute("delete from public.sale_card_report_wizard")

       # self.env.cr.execute("delete from public.sale_card_report_wizard")
        #self.env.cr.execute("insert into public.test_report (id) values (%s)" ,tuple(self.product_ids.ids))
        qry = """ 
        insert into public.test_daily_report (id) 
        select id from public.res_users where id in %s """
        self.env.cr.execute(qry, [tuple(self.users_ids.ids)])

        # date_from=time.strftime("%Y-%m-%d",[tuple(self.date_from)])
        # date_to = time.strftime("%Y-%m-%d",[tuple(self.date_to)])
       # f=''
        #d_f = time.strftime("%Y-%m-%d",datetime(self.date_from))
        # date_from = self.date_from.strftime("%Y-%m-%d")
        # qry_2 = """
        #         insert into public.test_report_date (date_from)
        #         values %s,%s,%s,%s,%s,%s,%s,%s,%s,%s """
        # self.env.cr.execute(qry_2,(tuple(date_from),))
        # qry_3 = """
        #                 insert into public.test_report_date_2 (date_to)
        #                 values %s """
        # self.env.cr.execute(qry_3,[tuple(join(str(self.date_to)))])

       #  query = """ insert into public.test_report (id) values  %s"""
       #  self.env.cr.execute(query, [tuple(self.product_ids.ids)])
        #stock_card_results = self._cr.fetchall()
        # self.env.cr.executemany("""
        #     INSERT INTO
        #         public.test_report
        #         (id)
        #     VALUES
        #         (%(id)s)
        # """, stock_card_results)
        # columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in stock_card_results.keys())
        # values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in stock_card_results.values())
        # self.env.cr.execute = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('public.test_report', columns, values)

        # for mydict in stock_card_results:
        #  placeholders = ', '.join(['%s'] * len(mydict))
        #  columns = ', '.join(mydict.keys())
        #  sql = "INSERT INTO {0} VALUES {1}" .format ('public.test_report', columns, placeholders)
        #  self._cr.execute(sql, mydict.values())


        # ReportLine = self.env['stock.card.view']
        # self.results = [ReportLine.new(line).id for line in stock_card_results]
        return{
            "type": "ir.actions.act_url",
            #"url":"http://109.205.176.129:8080/jasperserver/rest_v2/reports/reports/Sales_man_daily.pdf",
            "url":"http://109.205.176.129:8080/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2Freports&reportUnit=%2Freports%2FSales_man_daily&standAlone=true&decorate=no&j_acegi_security_check?&j_username=jasperadmin&j_password=jasperadmin",
            #"http://localhost:8080/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2Freports&reportUnit=%2Freports%2FSales_man_daily&standAlone=true&decorate=no&j_acegi_security_check?&j_username=jasperadmin&j_password=jasperadmin",

            "target": "new", }


    def _prepare_stock_card_report(self):
        self.ensure_one()
        return {
            'date_from': self.date_from,
            'date_to': self.date_to or fields.Date.context_today(self),
            'users_ids': [(6, 0, self.partner_ids.ids)],
            'location_id': self.location_id.id,
        }

    @api.multi
    def export(self):
        self.env.cr.execute("delete from public.test_daily_report")
        qry = """ 
              insert into public.test_daily_report (id) 
              select id from public.res_users where id in %s """
        self.env.cr.execute(qry, [tuple(self.users_ids.ids)])
        return {
            "type": "ir.actions.act_url",
            "url": "http://109.205.176.129:8080/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&output=pdf&ParentFolderUri=%2Freports&reportUnit=%2Freports%2FSales_man_daily&standAlone=true&decorate=no&j_acegi_security_check?&j_username=jasperadmin&j_password=jasperadmin",
            #"url": "http://109.205.176.129:8080/jasperserver/rest_v2/reports/reports/Sales_man_daily.pdf",
            # "url":"http://109.205.176.129:8080/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&output=pdf&ParentFolderUri=%2Freports&reportUnit=%2Freports%2FSales_man_daily&standAlone=true&decorate=no&j_acegi_security_check?&j_username=jasperadmin&j_password=jasperadmin",
            # "http://localhost:8080/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2Freports&reportUnit=%2Freports%2FSales_man_daily&standAlone=true&decorate=no&j_acegi_security_check?&j_username=jasperadmin&j_password=jasperadmin",

            "target": "new", }
