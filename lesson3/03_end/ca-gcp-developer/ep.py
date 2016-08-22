import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
# [END imports]


# [START messages]
class Character(messages.Message):
    """Character that stores the name."""
    name = messages.StringField(1)

class Characters(messages.Message):
    """Character that stores the name."""
    records = messages.MessageField(Character, 1, repeated=True)

characters = Characters(records=[
    Character(name="Rick"),
    Character(name="Morty"),
    Character(name="Bart"),
    Character(name="Homer"),
])

# ResourceContainers are used to encapsuate a request body and url
# parameters. This one is used to represent the Character ID for the
# get_character method.
GET_RESOURCE = endpoints.ResourceContainer(
    # The request body should be empty.
    message_types.VoidMessage,
    # Accept one url parameter: and integer named 'id'
    id=messages.IntegerField(1, variant=messages.Variant.INT32)
)



@endpoints.api(name='characters', version='v1')
class CharacterApi(remote.Service):
    @endpoints.method(
        # This method does not take a request message.
        message_types.VoidMessage,
        # This method returns a Characters message.
        Characters,
        path='characters',
        http_method='GET',
        name='characters.list')
    def list_character(self, unused_request):
        return characters

    @endpoints.method(
        # Use the ResourceContainer defined above to accept an empty body
        # but an ID in the query string.
        GET_RESOURCE,
        # This method returns a Character message.
        Character,
        # The path defines the source of the URL parameter 'id'. If not
        # specified here, it would need to be in the query string.
        path='characters/{id}',
        http_method='GET',
        name='characters.get')
    def get_character(self, request):
        try:
            # request.id is used to access the URL parameter.
            return characters.records[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException(
                'Character {} not found'.format(request.id))

    @endpoints.method(
        # This method accepts a request body containing a Character message
        # and adds it to the local NON-PERSISTENT list.
        Character,
        # This method returns a Character message.
        Characters,
        path='characters/add/',
        http_method='POST',
        name='characters.add')
    def add_character(self, request):
        characters.records.append(Character(name=request.name))
        return characters
    # [END CharacterApi]


better_characters = Characters(records=[
    Character(name="Better Rick"),
    Character(name="Better Morty"),
    Character(name="Better Bart"),
    Character(name="Better Homer"),
])


@endpoints.api(name='characters', version='v2')
class BetterCharacterApi(remote.Service):

    @endpoints.method(
        # This method does not take a request message.
        message_types.VoidMessage,
        # This method returns a Characters message.
        Characters,
        path='characters',
        http_method='GET',
        name='characters.list')
    def list_character(self, unused_request):
        return better_characters

    @endpoints.method(
        # Use the ResourceContainer defined above to accept an empty body
        # but an ID in the query string.
        GET_RESOURCE,
        # This method returns a Character message.
        Character,
        # The path defines the source of the URL parameter 'id'. If not
        # specified here, it would need to be in the query string.
        path='characters/{id}',
        http_method='GET',
        name='characters.get')
    def get_character(self, request):
        try:
            # request.id is used to access the URL parameter.
            return better_characters.records[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException(
                'Better Character {} not found'.format(request.id))

    @endpoints.method(
        # This method accepts a request body containing a Character message
        # and adds it to the local NON-PERSISTENT list.
        Character,
        # This method returns a Character message.
        Characters,
        path='characters/add/',
        http_method='POST',
        name='characters.add')
    def add_character(self, request):
        better_characters.records.append(Character(name=request.name))
        return better_characters
    # [END BetterCharacterApi]

app = endpoints.api_server([CharacterApi, BetterCharacterApi])
