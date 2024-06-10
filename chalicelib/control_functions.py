
from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocumentField, IntField, BooleanField, \
    EmbeddedDocument


class Tray(EmbeddedDocument):
    tray_id = IntField(required=True)
    tray_entry_time = DateTimeField(required=True)
    fish_type = StringField(required=True)
    weight = IntField(required=True)
    base_price = IntField(required=True)
    fisherman_id = IntField(required=True)
    sold_status = BooleanField(required=True, default=False)  # False means not sold, True means sold
    sold_price = IntField(required=True, default=0)  # 0 means not sold
    sold_time = DateTimeField(required=True, default=None)  # None means not sold
    is_dept_collected = BooleanField(required=True, default=False)  # False means not collected, True means collected

    def validate(self, clean=True):
        if self.sold_status:
            if self.sold_price < self.base_price:
                raise ValueError('Sold price cannot be less than base price')
            if self.sold_time is None:
                raise ValueError('Sold time cannot be None')
            if self.sold_price == 0:
                raise ValueError('Sold price cannot be 0')
            # log the event to Kafka topic 'sell_tray_event' and get auction_id from the parent document
            auction_id = self._instance.auction_id

        return super(Tray, self).validate(clean)


class Auction(Document):
    auction_id = IntField(required=True)
    auction_start_time = DateTimeField(required=True)
    trays = ListField(EmbeddedDocumentField(Tray))
    auction_status = StringField(required=True, default='ready')  # ready, started, ended

    def validate(self, clean=True):
        if self.auction_status == 'started':
            for tray in self.trays:
                if tray.sold_status is False:
                    raise ValueError('All trays should be sold before starting the auction')
        if self.auction_status == 'ended':
            for tray in self.trays:
                if tray.sold_status is False:
                    raise ValueError('All trays should be sold before ending the auction')
            # log the event to Kafka topic 'end_auction_event'

        return super(Auction, self).validate(clean)



