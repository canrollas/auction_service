from chalice import Chalice, Response

from chalicelib.control_functions import Auction

app = Chalice(app_name='auction_service')


@app.route('/api/auction', methods=['GET'])
def index():
    # get the url query param auction_id
    auction_id = app.current_request.query_params.get('auction_id')
    if auction_id:
        # find the auction from the database using the auction_id
        auction = Auction.objects(auction_id=auction_id).first()
        if auction:
            return auction.to_json()
        else:
            return Response(body='Auction not found', status_code=404)
    else:
        return Response(body='auction_id is required', status_code=400)



@app.route('/api/auction/start', methods=['POST'])
def start_auction_endpoint():
    # get the query param auction_id
    auction_id = app.current_request.query_params.get('auction_id')
    if auction_id:
        # find the auction from the database using the auction_id
        auction = Auction.objects(auction_id=auction_id).first()
        if auction:
            # update the auction status to 'started'
            auction.auction_status = 'started'
            auction.save()
            return auction.to_json()
        else:
            return Response(body='Auction not found', status_code=404)
    else:
        return Response(body='auction_id is required', status_code=400)


@app.route('/api/auctions/end', methods=['POST'])
def end_auction_endpoint():
    # get the query param auction_id
    auction_id = app.current_request.query_params.get('auction_id')
    if auction_id:
        # find the auction from the database using the auction_id
        auction = Auction.objects(auction_id=auction_id).first()
        if auction:
            # update the auction status to 'ended'
            auction.auction_status = 'ended'
            auction.save()
            return auction.to_json()
        else:
            return Response(body='Auction not found', status_code=404)
    else:
        return Response(body='auction_id is required', status_code=400)


@app.route('/api/auctions/update_tray', methods=['POST'])
def sell_tray_endpoint():
    # get the query param tray_id from the url
    tray_id = app.current_request.query_params.get('tray_id')
    # user can not change the tray_id and user must enter the sell price if the tray is sold etc. bussiness logic
    # get the request body
    request_body = app.current_request.json_body
    # find the auction from the database using the auction_id
    auction = Auction.objects(trays__tray_id=tray_id).first()
    if auction:
        # find the tray from the auction
        tray = [tray for tray in auction.trays if tray.tray_id == tray_id][0]
        # update the tray with the request body
        if tray is None:
            return Response(body='Tray not found', status_code=404)
        tray.update(**request_body)
        auction.save()
        return auction.to_json()
    else:
        return Response(body='Tray not found', status_code=404)





@app.route('/api/trays', methods=['GET'])
def get_auction_trays_endpoint():
    # return list of trays of the auction get the query param auction_id
    auction_id = app.current_request.query_params.get('auction_id')
    if auction_id:
        # find the auction from the database using the auction_id
        auction = Auction.objects(auction_id=auction_id).first()
        if auction:
            return auction.to_json()
        else:
            return Response(body='Auction not found', status_code=404)
    else:
        return Response(body='auction_id is required', status_code=400)



@app.route('/api/tray/{tray_id}', methods=['GET'])
def get_one_tray_endpoint(tray_id):
    # return one tray of the auction get the query param auction_id
    auction_id = app.current_request.query_params.get('auction_id')
    if auction_id:
        # find the auction from the database using the auction_id
        auction = Auction.objects(auction_id=auction_id).first()
        if auction:
            # find the tray from the auction
            tray = [tray for tray in auction.trays if tray.tray_id == tray_id][0]
            if tray:
                return tray.to_json()
            else:
                return Response(body='Tray not found', status_code=404)
        else:
            return Response(body='Auction not found', status_code=404)
    else:
        return Response(body='auction_id is required', status_code=400)



