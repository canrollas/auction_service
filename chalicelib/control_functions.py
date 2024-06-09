from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocumentField, IntField, BooleanField, \
    EmbeddedDocument
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')


class Tray(EmbeddedDocument):
    tray_id = IntField(required=True)
    tray_entry_time = DateTimeField(required=True)
    fish_type = StringField(required=True)
    weight = IntField(required=True)
    base_price = IntField(required=True)
    fisherman_id = IntField(required=True)
    sold_status = BooleanField(required=True,default=False) # False means not sold, True means sold
    sold_price = IntField(required=True,default=0) # 0 means not sold
    sold_time = DateTimeField(required=True,default=None) # None means not sold
    is_dept_collected = BooleanField(required=True,default=False) # False means not collected, True means collected

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
            sell_tray_event_message(self.tray_id, auction_id, self.fisherman_id, self.sold_price, self.base_price,
                                    self.sold_time, self.fish_type, self.weight, self.is_dept_collected)
        return super(Tray, self).validate(clean)

class Auction(Document):
    auction_id = IntField(required=True)
    auction_start_time = DateTimeField(required=True)
    trays = ListField(EmbeddedDocumentField(Tray))
    auction_status = StringField(required=True,default='ready') # ready, started, ended

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
            end_auction_event_message(self.auction_id , len(self.trays), len([tray for tray in self.trays if tray.sold_status]),
                                      len([tray for tray in self.trays if not tray.sold_status]), sum([tray.sold_price for tray in self.trays]))
        return super(Auction, self).validate(clean)




def sell_tray_event_message(tray_id, auction_id, fisherman_id, price, base_price, sold_time, fish_type, weight,
                            is_dept_collected):
    """
    This function uses this template to send a message to the Kafka topic 'sell_tray_event':
    {
      "tray_id": 1,
      "auction_id": 1,
      "fisherman_id": 1,
      "price": 100,
      "base_price": 100,
      "sold_time": "2021-09-01T12:00:00",
      "fish_type": "salmon",
      "weight": 10,
      "is_dept_collected": false
    }
    :param tray_id:
    :return:
    """
    message = {
        "tray_id": tray_id,
        "auction_id": auction_id,
        "fisherman_id": fisherman_id,
        "price": price,
        "base_price": base_price,
        "sold_time": sold_time,
        "fish_type": fish_type,
        "weight": weight,
        "is_dept_collected": is_dept_collected
    }
    producer.send('sell_tray_event', message)

    return message


def end_auction_event_message(auction_id, total_trays, total_sold_trays, total_unsold_trays, total_revenue):
    """
    This function uses this template to send a message to the Kafka topic 'end_auction_event':
    - auction-ended event => DB record after event triggered
    ````json
    {
      "auction_id": 1,
      "auction_end_time": "2021-09-01T12:00:00",
      "total_trays": 2,
      "total_sold_trays": 1,
      "total_unsold_trays": 1,
      "total_revenue": 100
    }
    ````
    :param auction_id:
    :return:
    """
    message = {
        "auction_id": auction_id,
        "auction_end_time": datetime.now(),
        "total_trays": total_trays,
        "total_sold_trays": total_sold_trays,
        "total_unsold_trays": total_unsold_trays,
        "total_revenue": total_revenue
    }
    producer.send('end_auction_event', message)

    return message