from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'
    sale_order_ids = fields.Many2many('sale.order',
                                      string = "Sale Orders")

    @api.onchange('sale_order_ids')
    def _onchange_sale_order_ids(self):
        print(self)
        for rec in self:
            #print(rec)
            lines = [(5, 0, 0)]
            for line in self.sale_order_ids.order_line:
                print(line.price_subtotal)
                vals = {
                    'name': self.partner_id.name,
                    'account_id':21,
                    'currency_id':2,
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty ,
                    'product_uom_id':line.product_uom.id,
                    'price_unit':line.price_unit,
                    'tax_ids':line.tax_id,
                    'credit':line.price_subtotal,
                    'debit':0,
                    'price_subtotal':line.price_subtotal,
                    'amount_currency':-line.price_subtotal,
                }
                lines.append((0, 0, vals))
            rec.invoice_line_ids = lines
            self._onchange_invoice_line_ids()
            self._onchange_recompute_dynamic_lines()
            self._recompute_dynamic_lines()

    def action_post(self):
        #print('hii')
        # if self.invoice_line_ids:
        #         print('hello')
        return  super(AccountMove, self).action_post()

