import endpoints
from protorpc import (
    message_types,
    messages,
    remote,
)

class Character(messages.Message):
    name = messages.StringField(1)

class Characters(messages.Message):
    records = messages.MessageField(Character, 1, repeated=True)


characters = Characters(records=[
    Character(name='Rick'),
    Character(name='Morty'),
    Character(name='Bart'),
    Character(name='Homer'),
])

GET_RESOURCE = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.IntegerField(1, variant=messages.Variant.INT32)
)

@endpoints.api(name='characters', version='v1')
class CharacterApi(remote.Service):

    @endpoints.method(
        message_types.VoidMessage,
        Characters,
        path='characters',
        http_method='GET',
        name='characters.list'
    )
    def list_characters(self, request):
        return characters


    @endpoints.method(
        GET_RESOURCE,
        Character,
        path='characters/{id}',
        http_method='GET',
        name='characters.get'
    )
    def get_character(self, request):
        try:
            return characters.records[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException(
                'Character {} not found'.format(request.id)
            )

    @endpoints.method(
        Character,
        Characters,
        path='characters/add',
        http_method='POST',
        name='characters.add'
    )
    def add_character(self, request):
        characters.records.append(Character(name=request.name))
        return characters


# Version 2
better_characters = Characters(records=[
    Character(name="Better Rick"),
    Character(name="Better Morty"),
    Character(name="Better Bart"),
    Character(name="Better Homer"),
])

@endpoints.api(name='characters', version='v2')
class BetterCharacterApi(remote.Service):

    @endpoints.method(
        message_types.VoidMessage,
        Characters,
        path='characters',
        http_method='GET',
        name='characters.list'
    )
    def list_characters(self, request):
        return better_characters


    @endpoints.method(
        GET_RESOURCE,
        Character,
        path='characters/{id}',
        http_method='GET',
        name='characters.get'
    )
    def get_character(self, request):
        try:
            return better_characters.records[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException(
                'Better Character {} not found'.format(request.id)
            )

    @endpoints.method(
        Character,
        Characters,
        path='characters/add',
        http_method='POST',
        name='characters.add'
    )
    def add_character(self, request):
        better_characters.records.append(Character(name=request.name))
        return better_characters

app = endpoints.api_server([CharacterApi, BetterCharacterApi])
