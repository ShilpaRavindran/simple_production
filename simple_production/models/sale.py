from odoo import  fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    transfer_status = fields.Char(string='Transfer Status',
                                  compute='_compute_transfer_status')

    def _compute_transfer_status(self):
        so_sequence = self.name
        print(so_sequence,"seq")
        self.transfer_status = 'Not Done'
        picking_origin = self.env['stock.picking'].search(
            [('origin', '=', so_sequence)])
        print(picking_origin)
        for record in picking_origin:
            print(record,"record")
            current_state = record.state
            print(current_state, 'current_state')
            for rec in self:
                if current_state == 'done':
                    rec.transfer_status = 'Done'
                elif current_state == 'cancel':
                    rec.transfer_status = 'Cancelled'


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    transfer_status = fields.Char(string='Transfer Status',
                                  compute='_compute_transfer_status')

    def _compute_transfer_status(self):
        po_sequence = self.name
        print(po_sequence, "seq")
        picking_origin = self.env['stock.picking'].search(
            [('origin', '=', po_sequence)])
        print(picking_origin)
        self.transfer_status = 'Not Done'
        print(self.transfer_status,"trnfr status")
        for record in picking_origin:
            print(record)
            current_state = record.state
            print(current_state, "current_state")
            for rec in self:
                if current_state == 'done':
                    rec.transfer_status = 'Done'
                elif current_state == 'cancel':
                    rec.transfer_status = 'Cancelled'


