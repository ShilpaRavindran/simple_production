# <?xml version="1.0" encoding="utf-8" ?>
# <odoo>
#     <data noupdate="1">
#         <record id="email_template_payment_link" model="mail.template">
#           <field name="name">Payment Link e-mail Template</field>
#           <field name="email_from">${object.company_id.email}</field>
#           <field name="subject">Payment Link</field>
#           <field name="email_to">${object.partner_id.email}</field>
#           <field name="lang">${object.lang}</field>
#           <field name="model_id" ref="simple_production.model_account_move"/>
#           <field name="auto_delete" eval="False"/>
#             <field name="body_html">
#                 <![CDATA[
# 	      <p>Dear ${(object.partner_id.name)},<br/><br/>
# 	      Here is your invoice ${(object.name)}
# 	      amounting in ${format_amount(object.amount_total, object.currency_id)}.<br/>
# 	        You can continue your payment through this link.<br/><br/>
# 	        <input type="button" NAME="button" Value="Payment" onClick="action_pay()"><br/>
# 	        ${object.get_base_url()}/website_payment/pay?reference=${(object.name)}&amount=${object.amount_total}&currency_id=${object.currency_id.id}&partner_id=${object.partner_id.id}&company_id=${object.company_id.id}&access_token=${object.access_token}<br/></p>
#               Do not hesitate to contact us if you have any questions.<br/><br/>
#               Regards,<br/><br/>
#               ${(object.company_id.name)}
# 	    ]]>
#
#             </field>
#         </record>
#     </data>
# </odoo>

# ${object.get_base_url()} / my / invoices /${
#     object.id}?model = account.invoice & res_id =${object.id} & access_token =${
#     object.access_token}


# print(self.name, "name")
# print(self.amount_total, "amount")
# print(self.currency_id.id, "currency")
# print(self.partner_id.id, "partner")
# print(self.access_token, "access token")
#
# link = ('%s/website_payment/pay?reference=%s&amount=%s&currency_id=%s'
#         '&partner_id=%s&access_token=%s') % (
#            self.get_base_url(),
#            urls.url_quote_plus(self.name),
#            self.amount_total,
#            self.currency_id.id,
#            self.partner_id.id,
#            self.access_token
#        )
# print(link, 'link')