from services.helpers import EasyRSA, Container


container = Container("4110bf40aa62")

EasyRSA(container=container)

EasyRSA.get_clients_data("Stepa123")