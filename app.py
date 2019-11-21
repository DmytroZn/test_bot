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
     
        bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            reply_markup=kb)
        
    else:
        print('NON PARANT')
        
        
        if call.data.split('_')[1]:
        
   
            look_cart = InlineKeyboardMarkup()
            ##################
            look = InlineKeyboardButton(text='Look my cart', callback_data=f'Look my cart_{category.id}')
            back = InlineKeyboardButton(text='<< back', callback_data=f'back_{category.id}')
            look_cart.add(back,look)
           
            print('200')
            
            u = models.Product.objects(category=call.data.split('_')[1])
            
            for i in u:
                keyboard = InlineKeyboardMarkup()
                b = InlineKeyboardButton(text='add to cart', callback_data=f'add to cart_{i.id}')
                keyboard.add(b)
             
                bot.send_message(call.message.chat.id, i.title)
                bot.send_photo(call.message.chat.id, 'https://images8.alphacoders.com/953/thumb-1920-953503.jpg')
                bot.send_message(call.message.chat.id, i.description, reply_markup=keyboard)





            bot.send_message(call.message.chat.id, ' _' , reply_markup=look_cart)
            print(f'call.message.chat.id: {call.message.chat.id}')
            print(f'call.message.message_id: {call.message.message_id}')
   
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'add to cart')
def add_to_cart(call):
    
    mod = models.User.objects(id_user=str(call.from_user.id)).first()
    print(mod.id)

    m = models.Cart(**{'user':models.User.objects(id_user=str(call.from_user.id)).first(), 'product': call.data[12:]}).save()

    b = models.Product.objects(id=call.data[12:]).first()
    print(b.title)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f'You added {b.title}') 
                    

  
@bot.callback_query_handler(func=lambda call: call.data == '_back_')
def back_to(call):
    print(f'call.message.chat.id: {call.message.chat.id}')
    print(f'call.message.message_id: {call.message.message_id}')
    print('_back_')
    # obj_id = call.data.split('_')[1]
    # category = models.Category.objects(id=obj_id).get()
    bot.register_next_step_handler(6790, show_products_or_sub_category)
    print('_back_to')
    # show_products_or_sub_category

  


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'Look my cart')
def look_my_cart(call):
    

    mod = models.User.objects(id_user=str(call.from_user.id)).first()
    look = models.Cart.objects(user=mod.id).first()
    look2 = models.Cart.objects(user=mod.id).all()


    obj_id = call.data.split('_')[1]
    category = models.Category.objects(id=obj_id).get()

    buy = InlineKeyboardMarkup()
    buy_one = InlineKeyboardMarkup()
    buy1 = InlineKeyboardButton('Buy', callback_data='buy')
    back = InlineKeyboardButton('<< back', callback_data=f'back_{category.id}')
    buy.add(back, buy1)
    buy_one.add(back)

    if look2:
        for i in look2:
            print('fod')
            print(i.id)
            dell = InlineKeyboardMarkup()
            dell1 = InlineKeyboardButton('Delete', callback_data=f'dell_{i.id}')
            dell.add(dell1)
            bot.send_message(call.message.chat.id, i.product.title, reply_markup=dell)
           
            print(i.product.title)

            
        bot.send_message(call.message.chat.id, 'You can buy', reply_markup=buy)
    else:   

        bot.send_message(call.message.chat.id, 'You don`t have any products', reply_markup=buy_one)



@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'dell')
def delete_product(call):
    cart = models.Cart.objects(id=call.data.split('_')[1]).delete()
  
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f'You delete') 
     
    bot.edit_message_text(text='You deleted product from cart.', chat_id=call.message.chat.id,
                        message_id=call.message.message_id)
        
    

@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def buy_product(call):
    mod = models.User.objects(id_user=str(call.from_user.id)).first()
    look = models.Cart.objects(user=mod.id).all()

    if look:
        for i in look:
            look.delete()
       


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


    print(text)

    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=kb)











if __name__ == '__main__':
    bot.polling(none_stop=True)
    # app.run()




