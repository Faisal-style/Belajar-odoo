
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


# class Book(models.Model):
#     _name = "library.book"
#     _description = "book"
#     _inherit = "mail.thread"
#     _order = "name, date_published"
#
#     _rec_name = "name"
#     _table = "library_book"
#     _log_access = True
#     _auto = True
#
#     name = fields.Char("Title", required=True, tracking=True)
#     isbn = fields.Char("ISBN")
#     active = fields.Boolean("Active?", default=True)
#     date_published = fields.Date()
#     image = fields.Binary("Cover")
#     publisher_id = fields.Many2one("res.partner", string="Publisher", domain=[('is_company','=',True)], tracking=True)
#     author_ids = fields.Many2many("res.partner", string="Author", domain=[('is_company','=',False)], tracking=True)
#
#
#
#
#     def _check_isbn(self):
#         self.ensure_one()
#         digits = [int(x) for x in self.isbn if x.isdigit()]
#         if len(digits) == 13:
#             ponderation = [1, 3] * 6
#             terms = [a*b for a, b in zip(digits[:12], ponderation)]
#             remain = sum(terms) % 10
#             check = 10 - remain if remain != 0 else 0
#             return digits[-1] == check
#
#     def button_check_isbn(self):
#         for book in self:
#             if not book.isbn:
#                 raise ValidationError("Please provide an ISBN for %s" % book.name)
#             if book.isbn and not book._check_isbn():
#                 raise ValidationError("%s ISBN is invalid" % book.isbn)
#
#         return True


class Book(models.Model):
    _name = "library.book"
    _description = "Book"
    _inherit = "mail.thread"

    # String Fields:
    name = fields.Char(
        "Title",
        default = None,
        help = "Book cover title.",
        readonly = False,
        required = True,
        index = True,
        copy = False,
        deprecated = True,
        groups = "",
        states={}
    )
    isbn = fields.Char("ISBN")
    book_type = fields.Selection(
        [
            ("paper", "paperback"),
            ("hard", "Hardcover"),
            ("electronic", "Electronic"),
            ("other", "Other"),
        ], "Type"
    )
    notes = fields.Text("Internal Notes")
    descr = fields.Html("Description")

    #numeric field
    copies = fields.Integer(default=1)
    avg_rating = fields.Float("Average Rating", (3, 2))
    price = fields.Monetary("price", "currency_id")

    #price helper
    currency_id = fields.Many2one("res.currency")

    #date and time fields:
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default = lambda self: fields.Datetime.now()
    )


    #other fields
    active = fields.Boolean("Active?")
    image = fields.Binary("Cover")

    #Relational Fields
    publisher_id = fields.Many2one(
        "res.partner", string="Publisher", domain=[('is_company','=',True)], tracking=True
    )
    author_ids = fields.Many2many(
        "res.partner", string="Author", domain=[('is_company','=',False)], tracking=True
    )


    publisher_country_id = fields.Many2one(
        "res.country",
        string="Publisher Country",
        related="publisher_id.country_id",
        # compute="_compute_publisher_country",
        inverse="_inverse_publisher_country",
        search="_search_publisher_country"
    )

    # @api.depends("publisher_id.country_id")
    # def _compute_publisher_country(self):
    #     for book in self:
    #         book.publisher_country_id = book.publisher_id.country_id
    #
    # def _inverse_publisher_country(self):
    #     for book in self:
    #         book.publisher_id.country_id = book.publisher_country_id
    #
    # def _search_publisher_country(self, operator, value):
    #     return [
    #         ("publisher_id.country_id", operator, value)
    #     ]


    # python constraint level

    @api.constrains("isbn")
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderation = [1, 3] * 6
            terms = [a*b for a, b in zip(digits[:12], ponderation)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError("Please provide an ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)

        return True


    # sql constraint level
    _sql_constraints = [
        (
            "library_book_name_date_uq",
            "UNIQUE (name, date_published)",
            "Title and publication date must be unique"
        ),
        (
            "library_book_check_date",
            "CHECK (date_published <= current_date)",
            "Publication date must not be in the future"
        )
    ]



class Partner(models.Model):
    _inherit = "res.partner"
    book_ids = fields.One2many("library.book", "publisher_id", string=" ")

    def action_view_books(self):
        # This method will open the list of books for the current partner
        return {
            'type': 'ir.actions.act_window',
            'name': 'Books Published',
            'view_mode': 'tree,form',
            'res_model': 'library.book',
            'domain': [('publisher_id', '=', self.id)],
            'target': 'current',
            'context': {
                'default_publisher_id': self.id  # Mengirimkan ID publisher ke form buku
            }
        }

