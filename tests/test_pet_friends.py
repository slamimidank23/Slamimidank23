import os
from api import PetFriends
from settings import valid_email, valid_password,invalid_email,invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Вход в систему"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_valid_user_negative(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_password_is_none(email=valid_email):

    status, result = pf.get_api_key_password_is_none(email)
    assert status == 403


def test_get_api_key_email_is_none(password=valid_password):
    status, result = pf.get_api_key_email_is_none(password)
    assert status == 403
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_valid_key_negative(filter=""):
    _, auth_key = pf.get_api_key(invalid_email,invalid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_add_new_pet_with_valid_data(name="Piter", animal_type='dog', age='2', pet_photo='images/sdc.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_name_type_age_with_valid_data(name='', animal_type='', age='', pet_photo='images/sdc.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "GoodFriend", "Cat", "3", "images/sad_cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_delete_self_pet_negative():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Lilit", "kitty cat", "3", "images/sdc.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 400


def test_successful_delete_more_index_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "GoodFriend", "Cat", "3", "images/sad_cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][4]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name="Bars", animal_type='cat', age='2'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info_negative(name="Кошатина", animal_type='кот', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400


def test_add_new_pet_without_photo(name='Bers', animal_type='dog', age='2'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo_negative(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


def test_add_photo_of_a_pet(pet_photo='images/sdc.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_without_photo(auth_key, "", "", "")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_a_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo']


def test_add_photo_of_a_pet_negative(pet_photo='images/sdc.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_without_photo(auth_key, "", "", "")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_a_pet(auth_key, pet_id, pet_photo)

    assert status == 400

