from models import models

beginning_kb = {
    'news' : 'Last news',
    'products' : 'Products',
    'sales' : 'Product for sales',
    'about' : 'Information about shop'
}


from telebot.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

class ReplyKB(ReplyKeyboardMarkup):
    def __init__(self, one_time_keyboard=True, resize_keyboard=True, row_width=3):
        super().__init__(one_time_keyboard=one_time_keyboard, 
                        resize_keyboard=resize_keyboard,
                        row_width=row_width)
    def generate_kb(self, *args):
        """

        : param args: Buttons names
        : return: new kb

        """

        # keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [KeyboardButton(x) for x in args]
        self.add(*buttons)
        return self



class InlineKB(InlineKeyboardMarkup):

    queries = {
        'root' : models.Category.get_root_categories()
    }

    def __init__(self, named_arg, lookup_field='id', iterable=None, key=None, title_field= 'title', row_width=3):
        if all([iterable, key]):
            raise ValueError('Only one of fields: iterable, key can be set')
        super().__init__(row_width=row_width)
        self._iterable = iterable
        self._named_arg = named_arg
        self._lookup_field = lookup_field
        self._title_field = title_field
        self._query = self.queries.get(key)

    def generate_kb(self):
        buttons = []
        if not self._iterable:
            self._iterable = self._query
        for i in self._iterable:
            buttons.append(InlineKeyboardButton(
                text=str(getattr(i, self._title_field)),
                callback_data = f'{self._named_arg}_' + str(getattr(i, self._lookup_field))
            ))

        self.add(*buttons)
        return self


    # def generate_root_kb(self):
    #     if not self._iterable:
    #         self._iterable = models.Category.get_root_categories()
    #         return self.generate_kb()
    #     raise ValueError('Iterable already set')
################################3
# class My:

#     def __init__(self, attr):
#         self._attr = attr

# my_obj = My('val')
# print(my_obj._attr)
# my_obj.newattr = 'new_val'
# setattr(my_obj, 'newattr', 'new_val')
# print(getattr(my_obj, '_attr'))