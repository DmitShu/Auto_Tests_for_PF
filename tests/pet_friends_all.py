# TestRun 1
# Блок тестов для описанных методов PetFriends API v1 (https://petfriends1.herokuapp.com/apidocs/#/)
# Заданы валидные данные. ОР: везде статус должен быть 200.
# При успешном завершении всего рана добавляется один питомец.

from datetime import datetime
from api import PetFriends
from settings import *
import os
import pytest

pf = PetFriends()

@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест шел: {end_time - start_time}")
    """Будет выполняться перед каждым тестом и измерять время выполнения"""

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
    # print()
    # for i in result['pets']:
    #     print(i['id'])


def test_add_new_pet_with_valid_data(name=add_name, animal_type=add_animal_type,
                                     age=add_age, pet_photo=add_pet_photo):
    """Проверяем что можно добавить питомца с корректными данными из settings.py"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] != ''


def test_delete_pet_valid_user():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, tmp_name, tmp_animal_type, tmp_age, tmp_pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert str(pet_id) not in str(my_pets['pets'])


def test_add_new_pet_simple_with_valid_data(name=add_smpl_name, animal_type=add_smpl_animal_type,
                                     age=add_smpl_age):
    """Проверяем что можно добавить питомца без фото с корректными данными из settings.py"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] == ''


def test_update_pet_info_with_valid_data(name=upd_name, animal_type=upd_animal_type, age=upd_age):
    """Проверяем возможность обновления информации о питомце из settings.py"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_pet_photo_with_valid_data(pet_photo2=add_pet_photo2, pet_photo3=add_pet_photo3):
    """Проверяем возможность гарантированного добавления / замены фото питомцу (картинки из settings.py)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo2 = os.path.join(os.path.dirname(__file__), pet_photo2)
    pet_photo3 = os.path.join(os.path.dirname(__file__), pet_photo3)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        id_orig = my_pets['pets'][0]['id']
        status1, result = pf.add_pet_photo(auth_key, id_orig, pet_photo2)
        photo_orig = result['pet_photo']
        status2, result = pf.add_pet_photo(auth_key, id_orig, pet_photo3)

        # Проверяем что статус ответа = 200 и фото заменено.
        assert status1 and status2 == 200
        assert result['pet_photo'] != photo_orig
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")