from django.shortcuts import render
from .marvelAPI import Marvel
from rest_framework import viewsets, status
from rest_framework.decorators import action 
from rest_framework.response import Response
from .serializers import CharacterSerializer, NameSerializer, ComicSerializer, CharacterComicSerializer
from .models import Character, CharacterComic, Comic

# Create your views here.

class CharacterViewSet(viewsets.ModelViewSet):
    handler = Marvel()
    serializer_class = None
    queryset = Character.objects.all()

    @action(methods=['GET'], detail=False, url_name='get_and_store_character', url_path='get-and-store-character')
    def get_and_store_character(self, request):
        name_serializer = NameSerializer(data=request.GET)

        if not name_serializer.is_valid():
            return Response({'errors': name_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            character_info= Character.objects.filter(name=name_serializer.validated_data.get('name').title()).values()
            
            if len(character_info)>0:
                return Response({'info': character_info}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(character_info)==0:
            character_info = self.handler.get_character(name_serializer.validated_data.get('name'), Character, CharacterComic)
            character_serializer = CharacterSerializer(data=character_info,many=True)
            if not character_serializer.is_valid():
                return Response({'error': character_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            character_serializer.save()
            character_info = character_serializer.validated_data

        if len(character_info)==0:
            return Response({'info': 'This character doesn\'t exist'}, status=status.HTTP_200_OK)

        return Response({'info': character_info}, status=status.HTTP_201_CREATED)
    
    @action(methods=['GET'], detail=False, url_name='get_and_store_comics_and_teammates', url_path='get-and-store-comics-and-teammates')
    def get_and_store_comics_and_teammates(self, request):
        name_serializer = NameSerializer(data=request.GET)

        if not name_serializer.is_valid():
            return Response({'errors': name_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            character = Character.objects.get(name=name_serializer.validated_data.get('name').title())
        except:
            return Response({'errors': 'The character {} doesn\'t exist'.format(name_serializer.validated_data.get('name'))}, status=status.HTTP_400_BAD_REQUEST)

        count_teammates, count_comics = self.handler.get_and_store_comics_and_teammates(character, Character,CharacterComic, Comic, ComicSerializer, CharacterSerializer, CharacterComicSerializer )
        query = CharacterComic.objects.filter(character=character.id)
    
        comics = [c.as_dict().pop('comic') for c in query]

        return Response({'info': comics,'added number teammates':count_teammates,'added number comics': count_comics }, status=status.HTTP_201_CREATED)
    
    @action(methods=['GET'], detail=False, url_name='get_character', url_path='get-character')
    def get_character(self, request):
        name_serializer = NameSerializer(data=request.GET)

        if not name_serializer.is_valid():
            return Response({'errors': name_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'info':Character.objects.filter(name=name_serializer.validated_data.get('name').title()).values()}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_name='get_teammates', url_path='get-teammates')
    def get_teammates(self,request):
        try:
            name_serializer = NameSerializer(data=request.GET)

            if not name_serializer.is_valid():
                return Response({'errors': name_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            character_id= Character.objects.filter(name=name_serializer.validated_data.get('name').title()).values_list('id', flat=True).first()
            comics_id =CharacterComic.objects.filter(character=character_id).values_list('comic_id', flat=True)
            result = CharacterComic.objects.filter(comic__in=comics_id).exclude(character=character_id)
            teammates = [dict(s) for s in set(frozenset(r.as_dict().get('character').items()) for r in result)]

            return Response({'total':len(teammates),'teammates':teammates}, status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response({'error': 'Character {} doesn\'t exist on DB'.format(request.GET['name']), 'e':str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['GET'], detail=False, url_name='get_all_characters', url_path='get-all-characters')
    def get_all_characters(self, request):
        characters = Character.objects.values()
        return Response({'total':len(characters),'characters':characters}, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_name='get_all_comics', url_path='get-all-comics')
    def get_all_comics(self, request):
        comics = Comic.objects.values()
        return Response({'total':len(comics),'comics':comics}, status=status.HTTP_200_OK)
    