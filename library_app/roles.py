from rolepermissions.roles import AbstractUserRole

class Writer(AbstractUserRole):

    available_permissions = {'create_book': True, 'edit_book': True, 'exclude_own_book': True}