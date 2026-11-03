# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class MassItemsQuanties(models.TransientModel):
    _name = 'mass.items.quantities'
    _description = 'Add Items'

    def _load_data(self):
        products = self._get_products_from_ids()
        parent_model = self._context['parent_model']
        parent_id = self._context['parent_id']
        model_record = self.env[parent_model].browse(parent_id)

        lines = []
        for product in products:
            val = {
                "name": model_record.name,
                "product": product.id,
                "default_code": product.default_code,
                "categ_id": product.categ_id.name,
                "product_uom": product.uom_id.id,
                "quantity": 1.0
            }

            lines.append(val)

        return lines

    item_lines = fields.One2many(
        'mass.items.line', 'name',
        default=_load_data,)

    def _get_products_from_ids(self):
        return self.env['sh.product.bundle'].search(
            [('id', 'in', self._context.get('product_ids', []))])

    def _get_products_from_mass_order_lines(self):
        return [line.product for line in self.item_lines]

    # return the duplicated product ids
    def _get_mixed_product_id(self):
        # get the product ids list from the order lines
        ids_in_order_lines = self._get_product_ids_in_order_lines()
        # get the mass product ids list from the wizard
        ids_in_mass_items = self._get_products_from_mass_order_lines()

        # return the duplicated product ids from two list
        return [
            val for val in ids_in_mass_items if val in ids_in_order_lines
        ]

    # return the product list ids from the order lines
    def _get_product_ids_in_order_lines(self):
        parent_model = self._context['parent_model']
        parent_id = self._context['parent_id']
        model_record = self.env[parent_model].browse(parent_id)

        product_lines = []
        if parent_model in ("sale.order", "purchase.order"):
            product_lines = model_record.order_line
        elif parent_model in ("stock.picking",):
            product_lines = model_record.move_lines
        elif parent_model in ("stock.inventory",):
            product_lines = model_record.line_ids
        elif parent_model in ("account.invoice",):
            product_lines = model_record.invoice_line_ids
        else:
            raise Warning(
                _(
                    """The model:%s
                    is not supported for massing adding lines!"""
                    % (parent_model)
                )
            )

        return [line.product_id for line in product_lines]

    # add the products into the lines
    def _add_product_items(self):
        # generate the product lines base on the product ids
        lines = []
        parent_model = self._context['parent_model']
        parent_id = self._context['parent_id']
        model_record = self.env[parent_model].browse(parent_id)

        for line in self.item_lines:
            if "sale.order" == parent_model:
                lines.append({
                    "product_id": line.sh.product.bundle.sh_product_id,
                    "product_uom": line.sh.product.bundle.sh_uom.id,
                    "product_uom_qty": line.sh_qty,
                    "price_unit": line.sh.product.bundle.sh_price_unit
                })
            elif "purchase.order" == parent_model:
                lines.append({
                    "product_id": line.product.id,
                    "product_uom": line.product.uom_id.id,
                    "product_qty": line.quantity,
                    "price_unit": 0,
                    "name": line.product.name,
                    "date_planned": fields.datetime.now()
                })
            elif "stock.picking" == parent_model:

                lines.append({
                    "product_id": line.product.id,
                    "product_uom": line.product.uom_id.id,
                    "product_uom_qty": line.quantity,
                    "location_id": model_record.location_id,
                    "location_dest_id": model_record.location_dest_id,
                    "name": line.product.name,
                })
            elif "stock.inventory" == parent_model:
                lines.append({
                    "product_id": line.product.id,
                    "product_uom_id": line.product.uom_id.id,
                    "product_qty": line.quantity,
                    "location_id": model_record.location_id,

                })
            elif "account.invoice" == parent_model:
                lines.append({
                    "product_id": line.product.id,
                    "uom_id": line.product.uom_id.id,
                    "quantity": line.quantity,
                    "name": line.product.name,
                    "price_unit": line.product.list_price,
                    "account_id": line.product.property_account_income_id,

                })


            else:
                raise Warning(
                    _(
                        """The model:%s
                        is not supported for massing adding lines!"""
                        % (parent_model)
                    )
                )

        if parent_model in ("sale.order", "purchase.order"):
            # write the products into the order lines
            model_record.order_line = lines
        elif parent_model in ("stock.picking"):
            # write the products into the order lines
            model_record.move_lines = lines
        elif parent_model in ("stock.inventory"):
            model_record.line_ids = lines
        elif parent_model in ("account.invoice"):
            model_record.invoice_line_ids = lines
       

    def _get_warning_message(self):
        # get the duplicate product ids from lines and mass products
        products = self._get_mixed_product_id()

        string = ""
        for product in products:
            string = string + product.name + "\n"

        return string

    @api.one
    def cancel_sheet(self):
        return {'type': 'ir.actions.act_window_close'}


    def add_products_with_quantity(self):
        mixed = self._get_mixed_product_id()

        # there is no duplicated product ids
        if not mixed:
            # add prodcuts into lines
            self._add_product_items()
            # close the wizard
            return {'type': 'ir.actions.act_window_close'}

        ctx = {
            'parent_id': self._context['parent_id'],
            'parent_model': self._context['parent_model'],
        }

        warning_message = self._get_warning_message()
        warning_obj = self.env['mass.items.confirm'].create(
            {'message': warning_message})

        return {
            'name': _('Confirm'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mass.items.confirm',
            'target': 'new',
            'res_id': warning_obj.id,
            'context': ctx,
        }


class MassItemsLine(models.TransientModel):
    _name = 'mass.items.line'
    _description = 'Item Line'

    name = fields.Char()
    product = fields.Many2one('sh.product.bundle', string='Name')
    default_code = fields.Char(readonly=True, string='Internal Reference',)
    categ = fields.Char(readonly=True, string='Internal Category')

    quantity = fields.Float()

    @api.onchange('	Bundle_Products')
    def _load_data(self):
        if self.Bundle_Products and self.Bundle_Products.id:
            product = self.env['sh.product.bundle'].search(
                [('id', '=', self.sh.product.bundle.sh_product_id)])

            self.default_code = Bundle_Products.default_code

            if product.categ_id and product.categ_id.name:
                self.categ = product.categ_id.name
            else:
                self.categ = ""


