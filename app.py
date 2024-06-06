from chalice import Chalice

app = Chalice(app_name='auction_service')


@app.route('/api/auctions', methods=['GET'])
def index():
    return {'hello': 'world'}


