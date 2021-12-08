from odoo import api, fields, models, _



class ProductionComponent(models.Model):
    _name = 'production.component'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'
    product_id = fields.Many2one('product.product',string="Product",required=True)
    quantity = fields.Float(string='Quantity')
    component_ids = fields.One2many('production.component.line','line_id')



class ComponentLine(models.Model):
    _name = 'production.component.line'
    _rec_name = 'product_id'
    product_id = fields.Many2one('product.product', string="Component")
    product_qty = fields.Float(string="Quantity")
    line_id = fields.Many2one('production.component')
    # production_line_id = fields.Many2one('simple.production')



