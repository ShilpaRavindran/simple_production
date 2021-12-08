from odoo import api, fields, models, _


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        product_rule = self.env['stock.putaway.rule'].search(
            [('product_id', '=', self.product_id.id)])
        self.location_id =product_rule.location_out_id
        #print(self.location_id)

    def action_validate(self):
        #print('hi')
        rule_location = self.env['stock.putaway.rule'].search(
            [('location_out_id','=',self.location_id.id),
             ('product_id','=',self.product_id.id)])
        #print(rule_location)
        if rule_location:
            #print('hello')
            return self.do_scrap()
        return super(StockScrap, self).action_validate()
