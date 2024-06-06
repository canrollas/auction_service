# Auction Service API 
## Description 

- Trays entered event will be handled by the auction service.
- We need :
  - Auction_id
  - Auction_ready_time 
  - List trays 
    - tray_id
    - tray_entry_time 
    - fish_type
    - weight 
    - base_price 
    - fisherman_id 
````json 
{
    "auction_id": 1,
    "auction_ready_time": "2021-09-01T12:00:00",
    "auction_start_time": "2021-09-01T12:00:00",
    "trays": [
        {
            "tray_id": 1,
            "tray_entry_time": "2021-09-01T12:00:00",
            "fish_type": "salmon",
            "weight": 10,
            "base_price": 100,
            "fisherman_id": 1
        },
        {
            "tray_id": 2,
            "tray_entry_time": "2021-09-01T12:00:00",
            "fish_type": "salmon",
            "weight": 10,
            "base_price": 100,
            "fisherman_id": 1
        }
    ]
}
````

1) Receive the auction event on kafka topic trays-entered 
2) start auction end point
3) end auction end point 
4) sell tray end point
5) update sell tray end point 
6) Send tray sold event on kafka topic tray-sold
7) Send auction ended event on kafka topic auction-ended
8) Get auction trays end point => returns the id of the trays that are in the auction
9) Get one tray end point => returns the tray details
10) Get auction end point => returns the auction details

- tray-sold event => DB record after event triggered
````json 
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
````

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
 
- Local development setups
1) clone repo
2) pip install -r requirements.txt 
3) chalice local
