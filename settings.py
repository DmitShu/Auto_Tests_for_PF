'''Тестовые данные для блока TestRun 1 (pet_friends_test_run_1_code_200.py)
   (Валидные, используются и в тестах последующих блоках, где требуется)'''

# test_get_api_key_for_valid_user
from logins import *

#Логины и пароли вынесены в отдельный файл.

# test_add_new_pet_with_valid_data
add_name='Веткудай'
add_animal_type='КОТЭ'
add_age='200'
add_pet_photo='images/pic1.jpg'

# test_add_new_pet_simple_with_valid_data
add_smpl_name='Просто'
add_smpl_animal_type='инкогнито'
add_smpl_age='404'

# test_update_pet_info_with_valid_data
upd_name='Демонэ'
upd_animal_type='рогатый'
upd_age='666'

# test_add_pet_photo_with_valid_data
add_pet_photo2='images/pic2.jpg'
add_pet_photo3='images/pic3.jpg'

# test_delete_tmp_pet
tmp_name='delme'
tmp_animal_type='delme'
tmp_age='111'
tmp_pet_photo='images/pic2.jpg'


'''Тестовые данные для блока TestRun 2 (pet_friends_test_run_2_code_403.py)'''

invalid_key1 = {'key': 'somerandomstaff'}

# test_get_api_key_for_invalid_user
# test_get_api_key_for_invalid_pass
invalid_email = "mrjds8dsg4@mrjds8dsg4"
invalid_password = "mrjds8dsg4dd673"


'''Тестовые данные для блока TestRun 3 (pet_friends_test_run_3_code_400.py)'''

big_data=9999*'Z'
pet_photo_invalid='images/pic4.wtf'
bad_filter='ОГОГО'

'''Тестовые данные для блока TestRun 4 (pet_friends_test_run_4_foreign_pets)'''

'''Генераторы данных'''

def generate_string(n):
   return "x" * n

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

def is_age_valid(age):
    # Проверяем, что возраст - это число от 1 до 49 и целое
    return age.isdigit() \
           and 0 < int(age) < 50 \
           and float(age) == int(age)
