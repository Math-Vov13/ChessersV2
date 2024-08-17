from .gui import Guis
from .console import Console

from . import enums

class create_UI_Object():
    def __new__(cls, addInterfaces: bool = False):
        if addInterfaces:
            ## ONLY FOR THE MOMENT !
            print("I'm sorry, but the game has no interfaces at the moment...")
            return Console()
        
            # return object.__new__(Guis)
        else:
            return Console()