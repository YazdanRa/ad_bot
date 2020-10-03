import datetime
from sqlalchemy import Column, Integer, String,Date,Text,Float,ForeignKey,Boolean,Binary
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.engine import url
import sqlalchemy

engine = create_engine("postgresql+psycopg2://postgres:24111999@/adsbot?host=127.0.0.1",echo=True)
#engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/bot')



from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    first_name= Column(String(convert_unicode=True))
    last_name=Column(String(convert_unicode=True))
    username = Column(String(convert_unicode=True))
    balance=Column(Float,default=0.00)
    earning=Column(Float,default=0.00)
    refferal=Column(Integer,default=0)
    refferal_earn=Column(Float,default=0)
    user_hash=Column(String(convert_unicode=True))
    refferal_hash=Column(String(convert_unicode=True))
    email=Column(String(convert_unicode=True))
    ads_count=Column(Integer,default=0)
    ban=Column(Boolean,default=False)
    joined=Column(Date)
    ip=Column(INET)




    def __str__(self):
        return self.first_name, self.last_name, self.username,self.chat_id


class Transaction(Base):
    __tablename__='trans'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    txn=Column(String(convert_unicode=True))
    amt=Column(Float,default=0)
    status_url=Column(String(convert_unicode=True))
    status=Column(String(convert_unicode=True),default='Unconfirmed')
   


    def __str__(self):
        return f'Transction ID :{self.txn}\nAmount : {str(self.amt)}\nStatus : {self.status}\nURL : {self.status_url}'

class Deposit(Base):
    __tablename__='deposit'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    txn=Column(String(convert_unicode=True))

    def __str__(self):
        return f'Transction ID :{self.txn}'

class Withdraw(Base):
    __tablename__='withdraw'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    username=Column(String(convert_unicode=True))
    amt=Column(Integer)
    address=Column(String(convert_unicode=True))
    message_id=Column(String(convert_unicode=True))
    txn=Column(String(convert_unicode=True))
    status=Column(String(convert_unicode=True),default='Unconfirmed')
    
    def __str__(self):
        return self.chat_id,self.address,self.amt,self.username

class Alert(Base):
    __tablename__='alter'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    nsfw=Column(String(convert_unicode=True),default="Disabled🔕")
    sites=Column(String(convert_unicode=True),default="Enabled🔔")
    bots=Column(String(convert_unicode=True),default="Enabled🔔")
    channel=Column(String(convert_unicode=True),default="Enabled🔔")
    post=Column(String(convert_unicode=True),default="Enabled🔔")

    def __str__(self):
        return self.chat_id,self.nsfw,self.sites,self.bots,self.channel,self.post


class Ads(Base):
    __tablename__='ads'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    ad_type=Column(String(convert_unicode=True))
    ad_id=Column(String(convert_unicode=True))
    link=Column(String(convert_unicode=True))
    title=Column(String(convert_unicode=True))
    desc=Column(String(convert_unicode=True))
    porn=Column(String(convert_unicode=True))
    ppc=Column(Float)
    budget=Column(Float)
    status=Column(String(convert_unicode=True),default="Enabled🔔")
    short_url=Column(String(convert_unicode=True))
    visits=Column(Integer,default=0)
    complete=Column(String(convert_unicode=True),default='No')
    post_message=Column(Integer)
    r_balance=Column(Float)
    verify=Column(Boolean)
    comment=Column(String(convert_unicode=True))
    username_needed=Column(String(convert_unicode=True),default='No')
    date=Column(Date,default=datetime.datetime.now())

    def __str__(self):
        return self.chat_id,self.ad_type,self.ad_id,self.link,self.title,self.desc,self.porn,self.cpc,self.budget

class Task(Base):
    __tablename__='task'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    ad_id=Column(String(convert_unicode=True))

    def __str__(self):
        return self.chat_id,self.ad_id

class Testgroup(Base):
    __tablename__='testgroup'
    id= Column(Integer, primary_key=True)
    username=Column(String(convert_unicode=True))
    ad_id=Column(String(convert_unicode=True))

    def __str__(self):
        return self.username,self.ad_id

class Minimum(Base):
    __tablename__='min'
    id= Column(Integer, primary_key=True)
    min_cpc_site=Column(Float,default=0.1)
    min_cpc_channel=Column(Float,default=0.15)
    min_cpc_post=Column(Float,default=0.07)
    min_cpc_bot=Column(Float,default=0.2)
    min_cpc_group=Column(Float,default=0.1)
    min_cpc_yt=Column(Float,default=0.1)
    min_budget_site=Column(Float,default=2)
    min_budget_channel=Column(Float,default=5)
    min_budget_post=Column(Float,default=2)
    min_budget_group=Column(Float,default=5)
    min_budget_yt=Column(Float,default=8)
    min_deposit=Column(Float,default=10)
    min_withdraw=Column(Float,default=40)
    bulk_message_price=Column(Float,default=0.2)

    def __str__(self):
        return self.id

class API_KEY(Base):
    __tablename__='api'
    id= Column(Integer, primary_key=True)
    public_key=Column(String(convert_unicode=True))
    private_key=Column(String(convert_unicode=True))
    tron_key=Column(String(convert_unicode=True))
    tron_address=Column(String(convert_unicode=True))

    def __str__(self):
        return self.id

class Wallet(Base):
    __tablename__='wallet'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    trx=Column(String(convert_unicode=True))
    btc=Column(String(convert_unicode=True))
    eth=Column(String(convert_unicode=True))
    bch=Column(String(convert_unicode=True))
    waves=Column(String(convert_unicode=True))
    doge=Column(String(convert_unicode=True))
    ltc=Column(String(convert_unicode=True))
    dash=Column(String(convert_unicode=True))
    xrp=Column(String(convert_unicode=True))
    bnb=Column(String(convert_unicode=True))

    def __str__(self):
        return self.id

class CheckUser(Base):
    __tablename__='check_user'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    ad_id=Column(String(convert_unicode=True))
    username=Column(String(convert_unicode=True))
    date=Column(Date)
    ppc=Column(Float)

    def __str__(self):
        return self.id

class ShortURL(Base):
    __tablename__='short_url'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    short_url=Column(String(convert_unicode=True))
    long_url=Column(String(convert_unicode=True))
    ad_id=Column(String(convert_unicode=True))
    status=Column(String(convert_unicode=True))

    def __str__(self):
        return self.id
    
class BulkMessage(Base):
    __tablename__='bulk_messages'
    id= Column(Integer, primary_key=True)
    order_id=Column(String(convert_unicode=True))
    chat_id=Column(Integer)
    content_type=Column(String(convert_unicode=True))
    text=Column(String(convert_unicode=True))
    file_name=Column(String(convert_unicode=True))
    total_users=Column(Integer)
    price=Column(Float)
    remaining=Column(String(convert_unicode=True))
    status=Column(String(convert_unicode=True),default='Incomplete')

class IPWhitelist(Base):
    __tablename__='whitelist'
    id= Column(Integer, primary_key=True)
    address=Column(INET)

    def __str__(self):
        return self.id
    




Base.metadata.create_all(engine)