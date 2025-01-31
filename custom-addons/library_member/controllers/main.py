from odoo import http
from odoo.addons.library_app.controllers.main import Books


class BooksExtended(Books):
    @http.route()
    def list(self, **kwargs):
        response = super().list(**kwargs)
        if kwargs.get("available"):
            all_book = response.qcontext["books"]
            available_books = all_book.filtered("is_available")
            response.qcontext["books"] = available_books
        return response