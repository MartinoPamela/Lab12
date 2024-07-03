from dataclasses import dataclass

from model.retailer import Retailer


@dataclass
class Connessione:
    v0: Retailer
    v1: Retailer
    peso: int
