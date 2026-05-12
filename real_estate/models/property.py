from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name='property'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'id'

    ref = fields.Char(default='New',readonly=True)
    name = fields.Char(string='Property Name',required=True)
    postcode = fields.Char(string='Postcode')
    date = fields.Date(string='Property Date')
    expected_selling_date = fields.Date()
    is_late=fields.Boolean()
    selling_price = fields.Float(string='Selling Price')
    expecting_price = fields.Float(string='Expected Price')
    bedrooms = fields.Integer(string='Bedrooms')
    garage = fields.Boolean()
    garden = fields.Boolean()
    description = fields.Char(string='Property Description',tracking=True)
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ],default='draft')
    active = fields.Boolean('Active',default=True)
    phone_id = fields.Char(related='owner_id.phone')
    property_line_ids = fields.One2many('property.line','property_id')
    #computed field
    # computed field لازم تستخدم مع depends
    #لاتخزن فى قواعد البيانات
    diff = fields.Float(string='Difference', compute='_compute_diff')
    @api.depends('selling_price','expecting_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff =rec.expecting_price - rec.selling_price
    #onchange
    @api.onchange('expecting_price')
    def _check_fields_not_negative(self):
        for rec in self:
            if rec.expecting_price < 0:
                return {
                    'warning': {'title':'Warning','message':'negative value','type':'notification'}
                }

    #constrains
    _sql_constraints = [
        ('unique_name','unique(name)','This name is exist'),
        ('unique_postcode', 'unique(postcode)', 'This postcode is exist')

    ]
    #________________________________________________________________________________________________________

    @api.model
    def create(self,vals):
        res = super(Property,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res
    # Check Bedrooms
    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Bedrooms cannot be 0")


    # draft state
    def crete_history_record(self,old_state,new_state,reason=""):
        for rec in self:
            rec.env['property_history'].create({
                'user_id':rec.env.uid,
                'property_id':rec.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason': reason or "",
                'property_history_lines': [
                    (0, 0, {
                        'description': line.description,
                        'area': line.area
                    }) for line in rec.property_line_ids
                ]
            })
    def action_draft(self):
        for rec in self:
            rec.crete_history_record(rec.state,'draft')
            print("inside action_draft")
            rec.write({'state':'draft'})

    #pending state
    def action_pending(self):
        for rec in self:
            rec.crete_history_record(rec.state,'pending')
            print("inside action pending")
            rec.state  ='pending'


    #sold state
    def action_sold(self):
        for rec in self:
            rec.crete_history_record(rec.state,'sold')
            rec.state = 'sold'

    # Server  Action Closed
    def action_closed(self):
        for rec in self:
            rec.crete_history_record(rec.state,'closed')
            rec.state = 'closed'



        #Automated Actions

    def check_expected_selling_date(self):
        property_ids = self.search([])
        print('inside check_expected_selling_date')
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    def action(self):
        print(self.env['owner'].create({
            'name':'Ahmed',
            'phone':'011489632',
        }))






    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_estate.change_state_action_wizard')
        action['context'] = {'default_property_id':self.id}
        return action



class PropertyLine(models.Model):
    _name='property.line'

    description = fields.Char(string='Property Description')
    area = fields.Float(string='Property Area')
    property_id  =fields.Many2one('property')
