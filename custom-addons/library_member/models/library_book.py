from odoo import fields, models

class Book(models.Model):
    _inherit = "library.book"
    is_available = fields.Boolean("is_Available?")

    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10")
    publisher_id = fields.Many2one(index=True)

    def _check_isbn(self):
        self.ensure_one()
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderation = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderation)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check
        else:
            return super()._check_isbn()
