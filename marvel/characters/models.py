from django.db import models
from django.utils.timezone import now
# Create your models here.

class Character(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=True, default='')
    imageURL = models.CharField(max_length=100, blank=True, default='')
    imageFullURL =  models.CharField(max_length=100, blank=True, default='')
    imageExtension = models.CharField(max_length=50, blank=True, default='')
    hasAllTeammates = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField( blank=True, null=True)
   
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'imageURL': self.imageURL,
            'imageFullURL': self.imageFullURL,
            'imageExtension': self.imageExtension,
            'hasAllTeammates': True if self.hasAllTeammates else False,
          }

class Comic(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=True, null=True, default='')
    upc = models.CharField(max_length=200, blank=True, default='')
    imageURL = models.CharField(max_length=100, blank=True, default='')
    imageFullURL =  models.CharField(max_length=100, blank=True, default='')
    imageExtension = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField( blank=True, null=True)
    characters = models.ManyToManyField(Character, through='CharacterComic')

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'upc': self.upc,
            'imageURL': self.imageURL,
            'imageFullURL': self.imageFullURL,
            'imageExtension': self.imageExtension,
            'characters': [c.as_dict() for c in self.characters.all()]
          }

class CharacterComic(models.Model):
    character = models.ForeignKey(Character, related_name='character', on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, related_name='comic', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('character', 'comic')

    def as_dict(self):
        return {
            'comic': self.comic.as_dict(),
            'character': self.character.as_dict()
        }