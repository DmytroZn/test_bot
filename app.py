import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import config
import keyboards
from models import models
from keyboards import ReplyKB

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
  
    dict_of_user = message.from_user
    print(dict_of_user.id)
    if not models.User.objects(id_user=str(dict_of_user.id)):
        data_of_user = models.User(**{
            'id_user' : str(dict_of_user.id),
            'first_name' : dict_of_user.first_name,
            'username' : dict_of_user.username,
            'last_name' : dict_of_user.last_name
            }).save()
    
    
    greeting_str = f'Hello {dict_of_user.first_name} {dict_of_user.last_name}'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())
    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == keyboards.beginning_kb['news'])
def say_news(message):
    # prod = models.Product.objects(category='5dcfe1badcd794512cc89b03')

    inlin = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='test1', callback_data='testing')
    inlin.add(in1)
    bot.send_photo(message.chat.id, 'https://images8.alphacoders.com/953/thumb-1920-953503.jpg', caption='po', reply_markup=inlin)

    # bot.send_message(message.chat.id, 'We created this bot 23.11.2019', reply_markup=inlin)


@bot.message_handler(func=lambda message: message.text == keyboards.beginning_kb['sales'])
def say_sales(message):

    bot.send_message(message.chat.id, 'Now we don`t have product for sale')


@bot.message_handler(func=lambda message: message.text == keyboards.beginning_kb['about'])
def say_about(message):
    text = '''
    This is bot-shop. 
    You can see products, choice products from categories and add products to your cart also buy.
    
    If you want have similar bot like this you can write to email: dmytro.zn@gmail.com'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text == keyboards.beginning_kb['cart'])
def say_cart(message):
    cat = models.Category.objects().first()

    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='My cart', callback_data=f'look my cart_{cat.id}')
    keyboard.add(button)
    bot.send_message(message.chat.id, text='Open cart', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'testing')
def sow(call):
#     prod = models.Product.objects(category='5dcfe1badcd794512cc89b03').all()
    
    inline_one = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='sdf', callback_data='sss')
    inline_one.add(b)
#     in1 = [InlineKeyboardButton(text=f'{i.title}\t', callback_data=f'{i.id}_prodgood') for i in prod]
#     l = InlineKeyboardButton(text='cart', callback_data='cart')
#     inline_one.add(*in1)
#     inline_one.add(l)
    # bot.send_photo(call.message.chat.id, 'https://images8.alphacoders.com/953/thumb-1920-953503.jpg', caption='po')
    # bot.send_location(call.message.chat.id, latitude=50.458136, longitude=30.512276)
    # bot.SuccessfulPayment(currency='USD', total_amount=145, invoice_payload='yy', 
    #                             telegram_payment_charge_id='sdf', provider_payment_charge_id='gg')
    # bot.edit_message_text(text='test\n test2', chat_id=call.message.chat.id,
    #                             message_id=call.message.message_id)
    # bot.edit_message_media('https://images8.alphacoders.com/953/thumb-1920-953503.jpg', chat_id=call.message.chat.id,
    #           message_id=call.message.message_id)
    # editMessageMedia
    # bot.edit_message_caption(caption='category.title', chat_id=call.message.chat.id,
    #                         message_id=call.message.message_id)

    bot.delete_message(chat_id=call.message.chat.id,
                            message_id=call.message.message_id)
    g = models.Product.objects(title='Cartoon').first()
    photo = g.photo.read()
    content_type = g.photo.content_type


    bot.send_photo(call.message.chat.id, photo, caption='po')
    bot.send_message(call.message.chat.id, content_type, reply_markup=inline_one)
  
# @bot.callback_query_handler(func=lambda call: call.data.split('_')[1] == 'prodgood')
# def soe2(call):
#     a = call.data.split('_')[0]
#     bot.edit_message_text(text='new', chat_id=call.message.chat.id,
#                                 message_id=call.message.message_id)
   

@bot.message_handler(func=lambda message: message.text == keyboards.beginning_kb['products'])
def show_categories(message):
        
    kb = keyboards.InlineKB(key='root', lookup_field='id', named_arg='category')

    bot.send_message(message.chat.id, 'Chooce category', reply_markup=kb.generate_kb())


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'category')
def show_products_or_sub_category(call):
    
    """
    :param call
    :return listed
    """

    obj_id = call.data.split('_')[1]
    category = models.Category.objects(id=obj_id).get()
 
    if category.is_parent:

        kb = keyboards.InlineKB(
            iterable=category.subcategory,
            lookup_field='id',
            named_arg='category'
        )
        kb.generate_kb()
        kb.add(InlineKeyboardButton(text=f'<< {category.title}',
                            callback_data=f'back_{category.id}'))
     

        bot.delete_message(chat_id=call.message.chat.id,
                            message_id=call.message.message_id)
        bot.send_message(text=category.title, chat_id=call.message.chat.id,reply_markup=kb)
        # bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
        #                     message_id=call.message.message_id,
        #                     reply_markup=kb)

    else:
        print('NON PARANT')
        if call.data.split('_')[1]:
            products = models.Product.objects(category=call.data.split('_')[1])
            keyboard = InlineKeyboardMarkup(row_width=1)
            prods = [InlineKeyboardButton(text=i.title, callback_data=f'show product_{i.id}_{category.id}') for i in products]
            back = InlineKeyboardButton(text=f'<< back', callback_data=f'back_{category.id}')
            if len(prods) == 0:
                text = 'Empty'
            else:
                text = category.title
            keyboard.add(*prods)
            keyboard.add(back)

            bot.delete_message(chat_id=call.message.chat.id,
                            message_id=call.message.message_id)

            bot.send_message(text=text, chat_id=call.message.chat.id, reply_markup=keyboard)
            # bot.edit_message_text(text=text, chat_id=call.message.chat.id,
            #                 message_id=call.message.message_id,
            #                 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'show product')
def show_prod(call):

    product = models.Product.objects(id=call.data.split('_')[1]).first()

    keyboard = InlineKeyboardMarkup()
    add_product = InlineKeyboardButton(text='Add to cart', callback_data=f'add to cart_{product.id}')
    back = InlineKeyboardButton(text='<< back', callback_data=f'category_{call.data.split("_")[2]}') # call.data.split("_")[2]}')
    look_cart = InlineKeyboardButton(text='Look my cart', callback_data=f'look my cart_{call.data.split("_")[2]}') 
    keyboard.add(add_product)
    keyboard.add(back, look_cart)
################
    # bot.delete_message(chat_id=call.message.chat.id,
    #                         message_id=call.message.message_id)
    # g = models.Product.objects(title='Cartoon').first()
    # photo = g.photo.read()
    # content_type = g.photo.content_type


    # bot.send_photo(call.message.chat.id, photo, caption='po')
    # bot.send_message(call.message.chat.id, content_type, reply_markup=inline_one)

#####################
    bot.delete_message(chat_id=call.message.chat.id,
                            message_id=call.message.message_id)
    text = f"""<b>{product.title}</b>\n {product.description} \n {product.get_price} USD \n """
    photo = product.photo.read()
    bot.send_photo(call.message.chat.id, photo, caption=text, parse_mode='HTML', reply_markup=keyboard)


    
    # bot.edit_message_text(text=f"""{product.title}\n {product.description} \n {product.get_price} USD \n """, chat_id=call.message.chat.id,
    #                         message_id=call.message.message_id, reply_markup=keyboard)

    
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'add to cart')
def add_to_cart(call):
    
    mod = models.User.objects(id_user=str(call.from_user.id)).first()
    print(mod.id)

    m = models.Cart(**{'user':models.User.objects(id_user=str(call.from_user.id)).first(), 'product': call.data[12:]}).save()

    b = models.Product.objects(id=call.data[12:]).first()
    print(b.title)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f'You added {b.title}') 


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'look my cart')
def look_my_cart(call):
    try:
        cart_del = models.Cart.objects(id=call.data.split('_')[2]).delete()
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f'You delete') 
    except IndexError:
        pass
 
    user = models.User.objects(id_user=str(call.from_user.id)).first()
    cart = models.Cart.objects(user=user.id).all()
    
    list_of_price = [i.product.price for i in cart]
    amount = (models.get_suum_of_prices(list_of_price)) / 100                                         

    keyboard = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text='<< back', callback_data=f'category_{call.data.split("_")[1]}_{None}')
    buy = InlineKeyboardButton(text=f'buy {amount} USD', callback_data=f'buy_{call.data.split("_")[1]}')
    prod_from_cart = [InlineKeyboardButton(text=f'{i.product.title} delete', callback_data=f'look my cart_{call.data.split("_")[1]}_{i.id}') for i in cart]
    if len(prod_from_cart) == 0:
        text='You don`t have any products \n but you can buy something'
        keyboard.add(back)
    else:
        text = 'My cart'
        keyboard.add(*prod_from_cart)
        keyboard.add(back, buy)

    bot.delete_message(chat_id=call.message.chat.id,
                            message_id=call.message.message_id)

    bot.send_message(text=text, chat_id=call.message.chat.id,
                            reply_markup=keyboard)

   
# @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'dell')
# def delete_product(call):
#     print('dell')
#     print(call.data)
#     cart = models.Cart.objects(id=call.data.split('_')[1]).delete()
  
#     bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f'You delete') 
     

@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'buy')
def buy_product(call):
    keyboard = InlineKeyboardMarkup()
    back = InlineKeyboardButton(text='<< back', callback_data=f'look my cart_{call.data.split("_")[1]}')
    keyboard.add(back)
    bot.edit_message_text(text='Serice for don`t work now, try do it late.', chat_id=call.message.chat.id,
                            message_id=call.message.message_id, reply_markup=keyboard)
    # mod = models.User.objects(id_user=str(call.from_user.id)).first()
    # look = models.Cart.objects(user=mod.id).all()

    # if look:
    #     for i in look:
    #         look.delete()


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'back')
def go_back(call):
    obj_id = call.data.split('_')[1]
    category = models.Category.objects(id=obj_id).get()
   
    if category.is_root:
        kb = keyboards.InlineKB(key='root', lookup_field='id', named_arg='category')
        kb.generate_kb()
    else:
        kb = keyboards.InlineKB(
            iterable=category.parent.subcategory,
            lookup_field='id',
            named_arg='category'
        )
        kb.generate_kb()
        kb.add(InlineKeyboardButton(text=f'<<< {category.parent.title}',
                                    callback_data=f'back_{category.parent.id}'))

    text = 'Categories' if not category.parent else category.parent.title

    bot.delete_message(chat_id=call.message.chat.id,
                            message_id=call.message.message_id)

    bot.send_message(text=text, chat_id=call.message.chat.id,
                            reply_markup=kb)
    # bot.edit_message_text(text=text, chat_id=call.message.chat.id,
    #                     message_id=call.message.message_id,
    #                     reply_markup=kb)


if __name__ == '__main__':
    bot.polling(none_stop=True)
    # app.run()