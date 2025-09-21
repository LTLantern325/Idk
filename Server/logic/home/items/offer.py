"""
Python conversion of Supercell.Laser.Logic.Home.Items.Offer.cs
Offer system for shop items
"""

from enum import IntEnum
from typing import Optional
from ..helper.byte_stream_helper import ByteStreamHelper

class ShopItem(IntEnum):
    """Shop item types enum"""
    FREE_BOX = 0
    COIN = 1
    GUARANTEED_BOX = 2
    GUARANTEED_HERO = 3
    SKIN = 4
    ITEM = 5
    BRAWL_BOX = 6
    TICKET = 7
    HERO_POWER = 8
    COIN_DOUBLER = 9
    MEGA_BOX = 10
    KEYS = 11
    WILDCARD_POWER = 12
    EVENT_SLOT = 13
    BIG_BOX = 14
    AD_BOX = 15
    GEMS = 16
    STAR_POINTS = 17
    EMOTE = 19
    EMOTE_BUNDLE = 20
    RANDOM_EMOTES = 21
    RANDOM_EMOTES_FOR_BRAWLER = 22
    RANDOM_EMOTE_OF_RARITY = 23
    SKIN_AND_HERO = 24
    PLAYER_THUMBNAIL = 25
    PURCHASE_OPTION_SKIN = 26
    RANDOM_EMOTES_PACK_OF_RARITY = 27
    BRAWL_PASS_TOKENS = 28
    CLUB_FEATURE = 29
    GUARANTEED_HERO_WITH_LEVEL = 30
    GUARANTEED_BOX_WITH_LEVEL = 31
    GEAR_TOKEN = 32
    GEAR_SCRAP = 33
    SPRAY = 35

class Offer:
    """Shop offer class"""

    def __init__(self, offer_type: Optional[ShopItem] = None, count: int = 0, 
                 item_global_id: int = 0, skin_global_id: int = 0):
        """Initialize offer"""
        self.type = offer_type if offer_type is not None else ShopItem.FREE_BOX
        self.count = count
        self.item_data_id = item_global_id
        self.skin_data_id = skin_global_id
        self.cost = 0
        self.currency_type = ShopItem.GEMS

    def is_free(self) -> bool:
        """Check if offer is free"""
        return self.cost == 0

    def is_currency_offer(self) -> bool:
        """Check if offer gives currency"""
        return self.type in [ShopItem.COIN, ShopItem.GEMS, ShopItem.STAR_POINTS]

    def is_box_offer(self) -> bool:
        """Check if offer gives boxes"""
        return self.type in [
            ShopItem.FREE_BOX, ShopItem.BRAWL_BOX, ShopItem.BIG_BOX, 
            ShopItem.MEGA_BOX, ShopItem.GUARANTEED_BOX, ShopItem.AD_BOX
        ]

    def encode(self, stream) -> None:
        """Encode offer to stream"""
        stream.write_v_int(int(self.type))
        stream.write_v_int(self.count)
        ByteStreamHelper.write_data_reference(stream, self.item_data_id)
        stream.write_v_int(self.skin_data_id)
