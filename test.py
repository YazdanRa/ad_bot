
from models import API_KEY,engine
from coinpayments import CoinPaymentsAPI


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session(autoflush=True)

api_key=session.query(API_KEY).first()

API_KEY= api_key.public_key
API_SECRET=api_key.private_key


payment=CoinPaymentsAPI(API_KEY,API_SECRET)

#deposit=payment.get_tx_ids()
#deposit=payment.get_tx_info(txid='CPEI2EQTYZ5WZTKAWQL3YBOWP6',full=1)
doge=payment.get_callback_address(currency='BNB',ipn_url='http://192.168.43.62:5000/process/')['result']['address']
print(doge)