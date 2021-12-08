from odoo import api, fields, models
import hashlib
import hmac


class InvoiceMailTemplate(models.Model):
    _inherit = 'account.move'
    access_token = fields.Char(compute='_compute_values')

    @api.depends('amount_total', 'name', 'partner_id', 'currency_id')
    def _compute_values(self):
        secret = self.env['ir.config_parameter'].sudo().get_param(
            'database.secret')
        for payment_link in self:
            token_str = '%s%s%s' % (
            payment_link.partner_id.id, payment_link.amount_total,
            payment_link.currency_id.id)
            payment_link.access_token = hmac.new(secret.encode('utf-8'),
                                                 token_str.encode('utf-8'),
                                                 hashlib.sha256).hexdigest()

    def action_post(self):
        template_id = self.env.ref('simple_production.email_template_payment_link').id
        print(template_id)

        send = self.env['mail.template'].browse(template_id).send_mail\
            (self.id ,force_send=True)
        print(send,"send id")
        return  super(InvoiceMailTemplate,self).action_post()

