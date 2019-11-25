from mongoengine import *
from models import models
from photos import *
connect('web_shop_bot')




##############################################

# for i in range(5):
#     obj = models.Category(**{'title':f'root {i}',
#                         'description':f'descr {i}'}).save()

#     obj.add_subcategory(
#         models.Category(**{'title': f'sub {i}',
#                             'description': f'descr {i}'})
#     )
###########################################

# objects = models.Category.objects(parent__ne=None)

# for i in objects:
#     i.add_subcategory(
#         models.Category(**{'title': f'sub-sub {i}',
#                             'description': f'd {i}'})
#     )

###################################3

           
# prod1 = models.Product.objects(title='test 3')


# prod1 = models.Product(**{'title': 'test10',
#                         'description': 'You can see',
#                         'price': 300,
#                         'category': '5dcfe1badcd794512cc89b03',
#                         # 'photo': None
#                        }).save()

# open_cart = open('photos/uuu.png', 'rb')
# prod1.photo.replace(open_cart, content_type='image/png')
# prod1.save()

# por = models.Product.objects(title='Iphone 8').first()
# por.photo.put(open_cart, content_type='uuu/png')
# por.save()



open_cart = open('photos/Meizu_16Xs.jpg', 'rb')

prod1 = models.Product.objects(title='Meizu 16Xs').first()
prod1.photo.put(open_cart, content_type='iPhone_7/jpg')
prod1.save()

# /home/dmytro/Documents/ITEA2/les12/pro/photos