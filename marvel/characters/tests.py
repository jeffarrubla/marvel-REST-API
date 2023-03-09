from django.test import TestCase
from django.urls import reverse
from .models import Character, Comic, CharacterComic
from rest_framework.test import APIClient
from rest_framework import status 
from datetime import datetime
from operator import itemgetter
import mock
from .marvelAPI import Marvel
from copy import deepcopy
# Create your tests here.

characters = [{
            "id": 1010705,
            "name": "Spectrum",
            "description": "",
            "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
            "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
            "imageExtension": "jpg",
            "hasAllTeammates": False,
            "created_at": "2023-03-08T15:42:14.744822Z",
            'updated_at':None
        },{
            "id": 1017824,
            "name": "Ms. America (America Chavez)",
            "description": "",
            "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available",
            "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg",
            "imageExtension": "jpg",
            "hasAllTeammates": False,
            "created_at": "2023-03-08T15:42:18.677560Z",
            'updated_at':None
        },{
                "id": 1010360,
                "name": "Thunderbolts",
                "description": "After a battle with Onslaught left the world without the majority of the heroes that made it feel safe, Baron Zemo devised a plan like no other in order to rule the world. Zemo gathered Beetle, Fixer, Goliath, Moonstone, and Screaming Mimi, all former members of the Masters of Evil, together to disguise themselves as a new heroic team in order to take advantage of the missing heroes and gain the trust of the authorities and public in general.",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": False,
                "created_at": "2023-03-08T15:42:28.678560Z",
                'updated_at':None
            },]

comics = [{
            "id": 101114,
            "title": "Thunderbolts (2022) #3",
            "description": '',
            "upc": "75960620386400311",
            "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/3/b0/6352e59c4148c",
            "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/3/b0/6352e59c4148c.jpg",
            "imageExtension": "jpg",
            }, {
            "id": 101115,
            "title": "Thunderbolts (2022) #4",
            "description": '',
            "upc": "75960620386400411",
            "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/1/20/63725579dc239",
            "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/1/20/63725579dc239.jpg",
            "imageExtension": "jpg",
            }]
class GetAllCharactersTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        for character in characters:
            Character.objects.create(**character)

        return super().setUp()
    
    def test_get_all_characters_successfully(self):
        response = self.client.get(reverse('character:get_all_characters-get_all_characters'),{},HTTP_USER_AGENT='Mozilla/5.0')

        list_1, list_2 = [sorted(l, key=itemgetter('id')) for l in (characters, response.json().get('Characters',[]))]
        self.assertEqual(any(x != y for x, y in zip(list_1, list_2)), False) # no differences
        self.assertEqual(len(characters),len( response.json().get('characters',[])) )
        self.assertEqual(len(characters), response.json().get('total')) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetCharacterTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        for character in characters:
            Character.objects.create(**character)

        return super().setUp()
    
    def test_get_character_successfully(self):
        response = self.client.get(reverse('character:get_character-get_character'),data={'name': 'Spectrum'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        l = response.json().get('info',[])
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0]==characters[0], True )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_character_fails(self):
        response = self.client.get(reverse('character:get_character-get_character'))#,HTTP_USER_AGENT='Mozilla/5.0', format='json')
        self.assertEqual(response.json().get('errors',{}),{'name': ['This field is required.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_character_not_found(self):
        response = self.client.get(reverse('character:get_character-get_character'),data={'name': 'Spec'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')
        l = response.json().get('info',[])
        self.assertEqual(len(l), 0)
        self.assertEqual(l, [] )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAndStoreCharacterTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        for character in characters[0:2]:
            Character.objects.create(**character)

        return super().setUp() 
    
    def get_character_mocked(self,*args):
        return [{
                "id": 1010360,
                "name": "Thunderbolts",
                "description": "After a battle with Onslaught left the world without the majority of the heroes that made it feel safe, Baron Zemo devised a plan like no other in order to rule the world. Zemo gathered Beetle, Fixer, Goliath, Moonstone, and Screaming Mimi, all former members of the Masters of Evil, together to disguise themselves as a new heroic team in order to take advantage of the missing heroes and gain the trust of the authorities and public in general.",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": False,
                "created_at": "2023-03-08T15:42:28.678560Z",
                'updated_at':None
            }]

    @mock.patch('characters.marvelAPI.Marvel.get_character', side_effect=get_character_mocked)
    def test_get_and_store_character_successfully(self, marvel_mock):
        response = self.client.get(reverse('character:get_and_store_character-get_and_store_character'),data={'name': 'Thunderbolts'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        self.assertEqual(self.get_character_mocked()[0]==response.json().get('info')[0], True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @mock.patch('characters.marvelAPI.Marvel.get_character', side_effect=lambda *args:[])
    def test_get_and_store_character_do_not_exist(self, marvel_mock):
        response = self.client.get(reverse('character:get_and_store_character-get_and_store_character'),data={'name': 'T'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        self.assertEqual(response.json().get('info'), "This character doesn't exist")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch('characters.marvelAPI.Marvel.get_character', side_effect=lambda *args:[])
    def test_get_and_store_character_no_input(self, marvel_mock):
        response = self.client.get(reverse('character:get_and_store_character-get_and_store_character'),data={})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        self.assertEqual(response.json().get('errors',{}),{'name': ['This field is required.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetAllComicsTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        for comic in comics:
            Comic.objects.create(**comic)

        return super().setUp()
    
    def test_get_all_comics_successfully(self):
        response = self.client.get(reverse('character:get_all_comics-get_all_comics'),{},HTTP_USER_AGENT='Mozilla/5.0')

        list_1, list_2 = [sorted(l, key=itemgetter('id')) for l in (comics, response.json().get('characters',[]))]
        self.assertEqual(any(x != y for x, y in zip(list_1, list_2)), False) # no differences
        self.assertEqual(len(comics),len( response.json().get('comics',[])) )
        self.assertEqual(len(comics), response.json().get('total')) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAndStoreComicsAndTeammatesTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        for character in characters:
            Character.objects.create(**character)

        for comic in comics:
            Comic.objects.create(**comic)
        for ids in [{'character':Character.objects.get(id=1010705), 'comic':Comic.objects.get(id=101114)},
                    {'character':Character.objects.get(id=1010360), 'comic':Comic.objects.get(id=101114)},
                    {'character':Character.objects.get(id=1010705), 'comic':Comic.objects.get(id=101115)},
                    {'character':Character.objects.get(id=1017824), 'comic':Comic.objects.get(id=101115)}]:
            CharacterComic.objects.create(**ids)
        return super().setUp() 

    @mock.patch('characters.marvelAPI.Marvel.get_and_store_comics_and_teammates', side_effect=lambda *args: (2,2))
    def test_get_and_store_comics_and_teammates_successfully(self, marvel_mock):
        response = self.client.get(reverse('character:get_and_store_comics_and_teammates-get_and_store_comics_and_teammates'),data={'name': 'Spectrum'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        characters_result = deepcopy(characters)
        for i in range(0,len(characters_result)):
            characters_result[i].pop('created_at')
            characters_result[i].pop('updated_at')

        comics_list = []
        for comic in response.json().get('info',[]):
            characters_response = comic.pop('characters',[])
            comics_list.append(comic)

            list_1, list_2 = [sorted(l, key=itemgetter('id')) for l in ([characters_result[0],characters_result[2]] if comic.get('id',0)==101114 else [characters_result[0],characters_result[1]], characters_response)]
            self.assertEqual(any(x != y for x, y in zip(list_1, list_2)), False) # no differences

        list_1, list_2 = [sorted(l, key=itemgetter('id')) for l in (comics, comics_list)]
        self.assertEqual(any(x != y for x, y in zip(list_1, list_2)), False) # no differences
        self.assertEqual(len(comics_list), len(comics))
        self.assertEqual(response.json().get("added number teammates"), 2)
        self.assertEqual(response.json().get("added number comics"), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @mock.patch('characters.marvelAPI.Marvel.get_character', side_effect=lambda _:())
    def test_get_and_store_comics_and_teammates_do_not_exist(self, marvel_mock):
        response = self.client.get(reverse('character:get_and_store_comics_and_teammates-get_and_store_comics_and_teammates'),data={'name': 'T'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        self.assertEqual(response.json().get('errors'), "The character T doesn't exist")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('characters.marvelAPI.Marvel.get_character', side_effect=lambda _:())
    def test_get_and_store_comics_and_teammates_no_input(self, marvel_mock):
        response = self.client.get(reverse('character:get_and_store_comics_and_teammates-get_and_store_comics_and_teammates'),data={})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')
        
        self.assertEqual(response.json().get('errors',{}),{'name': ['This field is required.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetTeammatesTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        for character in characters:
            Character.objects.create(**character)

        for comic in comics:
            Comic.objects.create(**comic)
        for ids in [{'character':Character.objects.get(id=1010705), 'comic':Comic.objects.get(id=101114)},
                    {'character':Character.objects.get(id=1010360), 'comic':Comic.objects.get(id=101114)},
                    {'character':Character.objects.get(id=1010705), 'comic':Comic.objects.get(id=101115)},
                    {'character':Character.objects.get(id=1017824), 'comic':Comic.objects.get(id=101115)}]:
            CharacterComic.objects.create(**ids)
        return super().setUp() 
    
    def test_get_teammates_successfully(self):
        response = self.client.get(reverse('character:get_teammates-get_teammates'),data={'name': 'Spectrum'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')

        characters_result = deepcopy(characters)
        for i in range(0,len(characters_result)):
            characters_result[i].pop('created_at')
            characters_result[i].pop('updated_at')
    
        list_1, list_2 = [sorted(l, key=itemgetter('id')) for l in ([characters_result[1],characters_result[2]], response.json().get('teammates',[]))]
        self.assertEqual(any(x != y for x, y in zip(list_1, list_2)), False) # no differences
        self.assertEqual(len(response.json().get('teammates',[])),2)
        self.assertEqual(response.json().get('total',0),2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_teammates_no_input(self):
        response = self.client.get(reverse('character:get_teammates-get_teammates'),data={})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')
        
        self.assertEqual(response.json().get('errors',{}),{'name': ['This field is required.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_and_store_comics_and_teammates_do_not_exist(self):
        response = self.client.get(reverse('character:get_teammates-get_teammates'),data={'name': 'T'})#,HTTP_USER_AGENT='Mozilla/5.0', format='json')
        
        self.assertEqual(len(response.json().get('teammates',[])),0)
        self.assertEqual(response.json().get('total',0),0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        