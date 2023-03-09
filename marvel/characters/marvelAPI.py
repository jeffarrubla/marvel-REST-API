import requests
import os 
import time   #this is needed to produce a time stamp
import hashlib
from datetime import datetime 
from django.db.models.base import ModelBase
from rest_framework.serializers import SerializerMetaclass

class Marvel():
    public_key = None
    private_key = None
    headers = {
        'user-agent':'Mozilla/5.0',
        'Accept': 'application/json'
    }

    def __init__(self) -> None:
        self.public_key =os.environ.get('PUBLIC_KEY',None)
        self.private_key =os.environ.get('PRIVATE_KEY',None)

    def build_url_and_get_results(self, query: str) -> list:
        offset=0
        limit=50
        count = 0
        total = 1
        results = []
        base_url = 'http://gateway.marvel.com/v1/public/'
        #next lines are for generating the hash required by Marvel API
        ts = str(time.time())  
        m = hashlib.md5() 
        ts_byte = bytes(ts, 'utf-8') 
        m.update(ts_byte) 
        m.update(str.encode(self.private_key))
        m.update(str.encode(self.public_key)) 
        
        try:
            while count < total:
                r = requests.get('{base}{query}ts={ts}&apikey={key}&hash={hash}&limit={limit}&offset={offset}&'.format(
                                                base=base_url,
                                                query = query,
                                                ts=ts,
                                                key=self.public_key,
                                                hash=m.hexdigest(), 
                                                limit=limit,
                                                offset=offset) )
                    
                data = r.json().get('data',{})
                offset+=limit
                count+= data.get('count',0)
                total = data.get('total',0)
                results+=data.get('results',[])        
        except Exception as e:
            raise Exception({'error':str(e)})

        return results
        
    def get_img_urls_and_info_from_object(self,thumbnail: dict) -> tuple:
        img_url= thumbnail.get('path','')
        img_extension=thumbnail.get('extension','')
        img_full_url =  '.'.join(filter(None, [img_url, img_extension]))

        return img_url, img_extension, img_full_url
    
    def format_characters_and_ids(self, characters: list, id_comic: int=0, character_model: ModelBase= None, charactercomic_model: ModelBase= None) -> tuple:
        characters_list = []
        charactercomics_ids = []
        for char in characters:
            character_info= character_model.objects.filter(id=char.get('id',"")).values()
            if len(character_info) == 0:
                img_url, img_extension,img_full_url = self.get_img_urls_and_info_from_object(char.get('thumbnail',{}))
                characters_list.append( {'id': char.get('id',""),
                                'name':char.get('name',""),
                                'description': char.get('description',""),
                                'imageURL': img_url,
                                'imageFullURL': img_full_url,
                                'imageExtension': img_extension
                                })
                        
            charactercomic_info = charactercomic_model.objects.filter(**{'character':char.get('id',""), 'comic':id_comic}).values()
            if len(charactercomic_info)==0:
                charactercomics_ids.append({'character':char.get('id',""), 'comic':id_comic})

        return characters_list, charactercomics_ids
    
    def get_character(self,name:str, character_model: ModelBase= None, charactercomic_model: ModelBase= None) -> list:
        characters = self.build_url_and_get_results('characters?name={name}&'.format(name=name))
        result,_ = self.format_characters_and_ids(characters, character_model=character_model, charactercomic_model=charactercomic_model)

        return result
    
    def get_and_store_comics_and_teammates(self, character: object, character_model: ModelBase= None, charactercomic_model: ModelBase= None, comic_model: ModelBase= None, 
                                           serializer_comic: SerializerMetaclass = None, serializer_character: SerializerMetaclass = None, serializer_charactercomic: SerializerMetaclass = None) -> tuple:
        comic_formatted = {}
        characters_formatted = []
        count_teammates = 0
        count_comics = 0
        comics = self.build_url_and_get_results('characters/{id_char}/comics?'.format(id_char=character.id))

        for comic in comics:
            img_url, img_extension,img_full_url =self.get_img_urls_and_info_from_object(comic.get('thumbnail',{}))
            characters_list = self.build_url_and_get_results('comics/{id_comic}/characters?'.format(id_comic=comic.get('id',"")))
            characters_formatted, charactercomics_ids = self.format_characters_and_ids(characters_list,comic.get('id',""), character_model=character_model, charactercomic_model=charactercomic_model)
           
            comic_formatted = {'id': comic.get('id',""),
                                'title':comic.get('title',""),
                                'description': comic.get('description',""),
                                'upc': comic.get('upc',""),
                                'imageURL': img_url,
                                'imageFullURL': img_full_url,
                                'imageExtension': img_extension,
                                'characters': charactercomics_ids
                                }  
            
            character_serializer = serializer_character(data=characters_formatted,many=True)
            if not character_serializer.is_valid():
                raise Exception({'error': character_serializer.errors})

            character_serializer.save()
            count_teammates += len(character_serializer.validated_data)

            comic_info = comic_model.objects.filter(id=comic.get('id',0))

            if len(comic_info)==0:
                comic_serializer = serializer_comic(data=comic_formatted)
                if not comic_serializer.is_valid(raise_exception=False):
                    raise Exception({'error':comic_serializer.errors})
                
                comic_serializer.save()
                count_comics += 1
            
            charactercomic_serializer = serializer_charactercomic(data=charactercomics_ids, many=True)
            if not charactercomic_serializer.is_valid():
                raise Exception({'error':charactercomic_serializer.errors})
            charactercomic_serializer.save()
            
        character_serializer = serializer_character(character,data={'id':character.id, 'updated_at':datetime.now(), 'hasAllTeammates': True},partial=True)
        if not character_serializer.is_valid():
            raise Exception({'error': character_serializer.errors})

        character_serializer.save()

        return count_teammates, count_comics