from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            print(f"Inside action confirm for Order: {order.name}")
        return res

    property_id = fields.Many2one('property')
