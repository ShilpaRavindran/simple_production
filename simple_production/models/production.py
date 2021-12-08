from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimpleProduction(models.Model):
    _name = 'simple.production'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Simple Production'
    name = fields.Char(string = 'Reference',
                       required=True, copy=False,
                       readonly=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.product', string="Product")
    component_id = fields.Many2one('production.component', string="Component")
    quantity = fields.Float(string='Quantity', readonly=False,
                             related = 'component_id.quantity',store =True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],default='draft', string='State', tracking =True)
    component_production_ids = fields.One2many('production.line',
                                               'production_line_id',store=True)


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code \
                               ('simple.production') or _('New')
        res = super(SimpleProduction, self).create(vals)
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        return {'domain': {
            'component_id': [('product_id', '=', self.product_id.id),
                           ]}}

    @api.constrains('quantity')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity != 0 and rec.component_id.quantity != 0:
                qty = rec.quantity % rec.component_id.quantity
                # print(qty)
                if qty != 0:
                    raise ValidationError(
                        _('It should be multiple of Quantity'))

    @api.onchange('component_id','quantity')
    def _onchange_component_id(self):
        # products = self.component_id.component_ids
        # print(products)
        # print(self.quantity)
        # print(self)
        for rec in self:
            qty = rec.quantity
            lines = [(5,0,0)]
            for line in rec.component_id.component_ids:
                vals = {
                    'product_id': line.id,
                    'product_uom_qty': line.product_qty * qty,
                }
                print(vals)
                lines.append((0,0,vals))
            rec.component_production_ids = lines


    def action_confirm(self):
        self.state = 'confirmed'
        stock_location = self.env.ref(
            'stock.stock_location_stock')
        production_location = self.env.ref(
            'simple_production.location_simple_production_location')
        for line in self.component_production_ids:
            uom = line.product_id.product_id.uom_id
            move = self.env['stock.move'].create({
                'name' : self.name,
                'location_id': stock_location.id,
                'location_dest_id': production_location.id,
                'product_id': line.product_id.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': uom.id ,
            })
            move._action_confirm()
            move._action_assign()
            move.move_line_ids.write({'qty_done': line.product_uom_qty})
            move._action_done()

    def action_done(self):
        self.state = 'done'
        stock_location = self.env.ref(
            'stock.stock_location_stock')
        production_location = self.env.ref(
            'simple_production.location_simple_production_location')
        move = self.env['stock.move'].create({
            'name': self.name,
            'location_id': production_location.id,
            'location_dest_id': stock_location.id,
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
        })
        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write({'qty_done': self.quantity})
        move._action_done()



    def action_cancel(self):
        self.state = 'cancel'

    def action_open_move(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Move',
            # 'reference': self.name,
            'view_mode': 'tree,form',
            'res_model': 'stock.move.line',
            'domain': [
                       ('state', '=', 'done'),
                       ('reference', '=', self.name)],
            'context': "{'create': False}"
        }

class ProductionLine(models.Model):
    _name = 'production.line'
    product_id = fields.Many2one('production.component.line', string="Component")
    product_uom_qty = fields.Float(string="To Consume", store=True)
    production_line_id = fields.Many2one('simple.production')
