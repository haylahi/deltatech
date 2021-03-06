# -*- coding: utf-8 -*-
# ©  2015-2018 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import fields, api, models



class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'barcodes.barcode_events_mixin']

    def _add_product(self, product, qty=1.0):
        order_line = self.order_line.filtered(lambda r: r.product_id.id == product.id)
        if order_line:
            order_line.product_qty += qty
        else:
            # product_lang = product.with_context({
            #     'lang': self.partner_id.lang,
            #     'partner_id': self.partner_id.id,
            # })
            # name = product_lang.display_name
            # if product_lang.description_purchase:
            #     name += '\n' + product_lang.description_purchase

            vals = {
                'product_id': product.id,
                # 'name': name,
                'date_planned': fields.Datetime.now(),
                'product_uom': product.uom_po_id.id,
                'product_qty': 1,
                # 'price_unit': product.standard_price,
                'state': 'draft',
            }
            order_line = self.order_line.new(vals)
            order_line.product_id_change()
            self.order_line += order_line

    def on_barcode_scanned(self, barcode):
        if self.state != 'draft':
            return
        product = self.env['product.product'].search([('barcode', '=', barcode)])
        if product:
            self._add_product(product)