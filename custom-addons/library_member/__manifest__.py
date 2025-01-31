
{
    'name': "Library Member",
    'license': 'AGPL-3',
    'description': """
Manage member borrowing books
    """,
    'author': "My Company",
    'depends': ["library_app", "mail"],
    "application": False,
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/member_view.xml',
        'views/library_menu.xml',
        'views/book_list_template.xml'
    ],


}

