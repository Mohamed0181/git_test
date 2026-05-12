from odoo import fields , models

class Owner(models.Model):
    _name = 'owner'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name',required=1,tracking=True)
    phone  = fields.Char(string='Phone',size=11,required=True,tracking=1)
    address = fields.Char(string='Address')
    email = fields.Char(string='Email',tracking=1)
    property_ids = fields.One2many('property','owner_id')
