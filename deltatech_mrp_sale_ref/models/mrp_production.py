# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com       
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api
from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_order_id = fields.Many2one('sale.order', compute="_compute_sale_order", string="Sale Order")

    @api.multi
    def _compute_sale_order(self):
        mto_route = self.env.ref('stock.route_warehouse0_mto')
        for production in self:
            if mto_route.id in production.product_id.route_ids.ids:
                for prod_procurement in production.procurement_ids:
                    for procurement in prod_procurement.group_id.procurement_ids:
                        if procurement.sale_line_id:
                            production.sale_order_id = procurement.sale_line_id.order_id
