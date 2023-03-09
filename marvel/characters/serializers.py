from rest_framework import serializers
from .models import Character, Comic, CharacterComic

class NameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, allow_blank=False)

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

    def get_or_create(self):
        defaults = self.validated_data.copy()
        identifier = defaults.pop('id')
        return Character.objects.get_or_create(id=identifier, defaults=defaults)

    def create(self, validated_data):
        id = validated_data.pop('id')
        character, created = Character.objects.get_or_create(id=id
            , defaults={ **validated_data} )
        return character

class CharacterComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterComic 
        fields = '__all__'

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = '__all__'

    def create(self, validated_data):
        id = validated_data.pop('id')
        comic, created = Comic.objects.get_or_create(id=id
            , defaults={ **validated_data} )

        return comic
