from odoo import api , models ,fields

class PropertyHistory(models.Model):
    _name= 'property_history'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char('Old State')
    new_state = fields.Char('New State')
    reason = fields.Char('Reason')
    property_history_lines=fields.One2many('property_history_lines','property_history_id')



class PropertyHistoryLines(models.Model):
    _name='property_history_lines'

    description = fields.Char('Description')
    area = fields.Float('Area')
    property_history_id = fields.Many2one('property_history')
