import requests

def buscar_pokemon(nome):
  url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"

  res = requests.json()

  print(res)


buscar_pokemon("pikachu")
