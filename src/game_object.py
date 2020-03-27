from abc import ABC, abstractclassmethod


class Game_object(ABC):
    # abstract class for my game objects
    @abstractclassmethod
    def move(self): pass

    @abstractclassmethod
    def draw(self): pass

    @abstractclassmethod
    def reset(self): pass
