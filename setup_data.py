# exec(open("./setup_data.py").read())

from move_app.models import Move
from pokemon_app.models import Pokemon

psychic = Move(name = 'Psychic')
psychic.save()

charizard = Pokemon(name = 'Charizard', level = 25, date_encountered = "2007-04-07", captured = True)
charizard.save()

pokemon1 = Pokemon.objects.get(id=1)  # Retrieve a Pokemon object
move1 = Move.objects.get(id=1) 
pokemon1.moves.add(move1)