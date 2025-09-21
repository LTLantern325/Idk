"""
Python conversion of Supercell.Laser.Logic.Home.Items.OfferBundle.cs
Offer bundle for grouped shop offers
"""

from typing import List
from .offer import Offer, ShopItem

class OfferBundle:
    """Bundle of multiple offers"""

    def __init__(self):
        """Initialize offer bundle"""
        self.offers: List[Offer] = []
        self.bundle_cost = 0
        self.bundle_currency = ShopItem.GEMS
        self.bundle_name = ""
        self.bundle_description = ""
        self.is_featured = False
        self.discount_percentage = 0
        self.purchase_limit = 1
        self.purchases_made = 0

    def add_offer(self, offer: Offer) -> None:
        """Add offer to bundle"""
        self.offers.append(offer)

    def get_offers(self) -> List[Offer]:
        """Get all offers in bundle"""
        return self.offers.copy()

    def get_offer_count(self) -> int:
        """Get number of offers"""
        return len(self.offers)

    def set_bundle_cost(self, cost: int, currency: ShopItem = ShopItem.GEMS) -> None:
        """Set bundle cost and currency"""
        self.bundle_cost = max(0, cost)
        self.bundle_currency = currency

    def has_discount(self) -> bool:
        """Check if bundle has discount"""
        return self.discount_percentage > 0

    def get_discounted_cost(self) -> int:
        """Get cost after discount"""
        if self.discount_percentage > 0:
            return int(self.bundle_cost * (100 - self.discount_percentage) / 100)
        return self.bundle_cost

    def can_purchase(self) -> bool:
        """Check if bundle can be purchased"""
        return self.purchases_made < self.purchase_limit

    def encode(self, stream) -> None:
        """Encode bundle to stream"""
        stream.write_v_int(len(self.offers))
        for offer in self.offers:
            offer.encode(stream)

        stream.write_v_int(self.bundle_cost)
        stream.write_v_int(int(self.bundle_currency))
        stream.write_string(self.bundle_name)
        stream.write_string(self.bundle_description)
        stream.write_boolean(self.is_featured)
        stream.write_v_int(self.discount_percentage)
