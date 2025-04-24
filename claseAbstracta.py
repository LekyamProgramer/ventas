from abc import ABC, abstractmethod
from typing import List,Dict,Any

class Interface(ABC):
    @abstractmethod
    def save(self,data:str):
       pass

    @abstractmethod
    def read (self)->str:
       pass
    
    @abstractmethod
    def find (self, atributo: str, buscando:str)-> str:
       pass
