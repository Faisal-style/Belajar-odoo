from odoo import fields, models


class Member(models.Model):
    _name = "library.member"
    _description = "Library Member"
    _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]
    partner_id = fields.Many2one(
        "res.partner",
        delegate=True,
        ondelete="cascade",
        required=True
    )
    card_number = fields.Char()

    #redifinisi partner model
    name = fields.Char(related="partner_id.name", inherited=True, tracking=True, readonly=False)