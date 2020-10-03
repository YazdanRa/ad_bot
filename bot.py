#!/usr/bin/python

import telebot
import time
import hashlib
from models import User,engine,User,Transaction,Deposit,Withdraw,Alert,Ads,Task,API_KEY,Wallet,Testgroup,CheckUser,Minimum,BulkMessage,IPWhitelist
import datetime
from telebot.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import re
import os
import string 
import random
import threading
import requests
import json
from calendar import mdays
from datetime import datetime, timedelta,date
from coinpayments import CoinPaymentsAPI
from dateutil.relativedelta import *    
from apscheduler.schedulers.background import BackgroundScheduler
import traceback
import sqlalchemy
from tronpy import Tron
from tronpy.keys import PrivateKey
import urllib.parse
import atexit



token='1023938466:AAEQ_3Z3dAJr5LDS_oNaOLGeph3vvrMW79k'
#token='1023938466:AAFSRCGOQAajiyY7SE5kxTDTcaPDecOQAjs' #test
bot=telebot.TeleBot(token)
admin=[431108047,552376726,1068108948]

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session(autoflush=True)

import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

api_key=session.query(API_KEY).first()

API_KEY= api_key.public_key
API_SECRET=api_key.private_key

tron_client = Tron()

payment=CoinPaymentsAPI(API_KEY,API_SECRET)

minimum=session.query(Minimum).first()

sched=BackgroundScheduler(timezone='UTC')

msg=[]
usernam=[]
ad_i=[]
comme=[]

#todo : group verification text 


def user_data(message):
    user=session.query(User).filter(User.chat_id == message.chat.id).all()
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username=message.from_user.username
    userhash = hashlib.md5(str(message.chat.id).encode('utf-8')).hexdigest()
    chat_id = message.chat.id
    
    if first_name == None:
        first_name = 'None'
    if last_name == None:
        last_name = 'None'
    if username == None:
        username = 'None'
    if chat_id == None:
        chat_id = 'None'
    
    if not len(user):
        session.add(User(chat_id=message.chat.id,username=username,first_name=first_name,last_name=last_name,joined=datetime.today(),user_hash=userhash[:10],refferal_hash=message.text[7:]))
        session.commit()
        session.add(Alert(chat_id=chat_id))
        session.commit()
        
        """doge=payment.get_callback_address(currency='DOGE',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        trx=payment.get_callback_address(currency='TRX',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        btc=payment.get_callback_address(currency='BTC',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        eth=payment.get_callback_address(currency='ETH',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        xrp=payment.get_callback_address(currency='XRP',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        dash=payment.get_callback_address(currency='DASH',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        bch=payment.get_callback_address(currency='BCH',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        ltc=payment.get_callback_address(currency='LTC',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        bnb=payment.get_callback_address(currency='BNB',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        session.add(Wallet(chat_id=chat_id,doge=doge,trx=trx,btc=btc,eth=eth,xrp=xrp,dash=dash,bch=bch,ltc=ltc,bnb=bnb))
        session.commit()"""
    if len(user):
        z=session.query(User).filter(User.chat_id == message.from_user.id).one()
        if z.ban==False:
            session.query(User).filter(User.chat_id == message.from_user.id).update({User.first_name:first_name,User.last_name:last_name,User.username:username},synchronize_session='fetch')
            session.commit()
        else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

   
        




@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.chat.type=='private':
        a=[]
        user_id=session.query(User).all()
        for i in user_id:
            a.append(i.chat_id)
        if message.chat.id in a:
            pass
        else:
            try:
                session.query(User).filter(User.user_hash==message.text[7:]).update({User.refferal : User.refferal+1})
                session.commit()
                q=session.query(User).filter(User.user_hash==message.text[7:]).one()
                bot.send_message(q.chat_id,f"{message.from_user.first_name} joined the bot through your referral link\n\nYour Total Referers : {q.refferal}",parse_mode='markdown')
            except Exception:
                pass
        user_data(message)
        start_msg="""Welcome to *Rapid Click BOT!*🔥

This bot let you earn TRON (TRX) by completing simple tasks.

Press 📣 *Join channels* to earn by joining channels
Press 🌐 *Visit Links* to earn by clicking links
Press 📄 *Read Post* to earn by reading post
Press 👥  *Join chats* to earn by joining chats
Press ▶️  *YouTube Video* to earn by watching Videos

You can also create your own ads with 🖥    *My Promotions*    🖥"""
        
        try:
            bot.send_message(message.chat.id,start_msg,reply_markup=start_markup(),parse_mode='markdown')
        except Exception:
            bot.send_message(message.chat.id,"Aww :( , Something went wrong,Please try again.")
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    
      

@bot.message_handler(regexp='👫 Referral System')
def refferals_handler(message):
    user=session.query(User).filter(message.chat.id==User.chat_id).one()
    if user.ban==False:
        msg=f"You have {user.refferal} referrals, and earned {user.refferal_earn} TRX.\n\nTo refer people, send them to:\nhttps://t.me/Rapidclickbot?start={user.user_hash}\n\nYou will earn 10% of each user's earnings from tasks."
        bot.send_message(message.chat.id,msg,reply_markup=refferal_markup(message))
    else:
        bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")



       

@bot.message_handler(regexp='💰 Balance')
def User_handler(message):
        user=session.query(User).filter(User.chat_id==message.chat.id).one()
        if user.ban==False:
            bot.send_message(message.chat.id,f'*Balance* {user.balance} TRX\n\n*Available For Payout:* {user.earning} TRX\n\n*Email :* `{user.email}`',reply_markup=balance_markup(),parse_mode='markdown')
        else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='📧 Update Email')
def email_handler(message):
    user=session.query(User).filter(User.chat_id==message.chat.id).one()
    if user.ban==False:
        sent=bot.send_message(message.chat.id,"Send Your Email Address")
        bot.register_next_step_handler(sent,email)
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

def email(message):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    user=session.query(User).filter(User.chat_id==message.chat.id).one()
    if user.ban==False:
        try:
            if(re.search(regex,message.text)):
                session.query(User).filter(User.chat_id==message.chat.id).update({User.email:message.text})
                session.commit()
                bot.send_message(message.chat.id,"✅ Email Set Sucessfully")
            else:
                bot.send_message(message.chat.id,'❌ Invalid Email..!')
        except Exception :
            bot.send_message(message.chat.id,'❌ Invalid Email..!')
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='➕ Deposit')
def deposit_handler(message):
    user=session.query(User).filter(User.chat_id==message.chat.id).one()
    wallet=session.query(Wallet).filter(Wallet.chat_id == message.chat.id).all()
    if not len(wallet):
        doge=payment.get_callback_address(currency='DOGE',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        trx=payment.get_callback_address(currency='TRX',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        btc=payment.get_callback_address(currency='BTC',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        eth=payment.get_callback_address(currency='ETH',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        xrp=payment.get_callback_address(currency='XRP',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        dash=payment.get_callback_address(currency='DASH',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        bch=payment.get_callback_address(currency='BCH',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        ltc=payment.get_callback_address(currency='LTC',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        bnb=payment.get_callback_address(currency='BNB',ipn_url='http://162.0.230.68:5000/process/')['result']['address']
        session.add(Wallet(chat_id=message.chat.id,doge=doge,trx=trx,btc=btc,eth=eth,xrp=xrp,dash=dash,bch=bch,ltc=ltc,bnb=bnb))
        session.commit()

    if user.ban==False:
        #bot.send_message(message.chat.id,"🛠 Under Maintainence",parse_mode='markdown')
        a=f"*Select below Cryptocurrency To deposit*\n\nThe amount you deposit will be converted to TRX at it current market value.\n\nTRX coins can be used to start any campaigns. \n\n\n*Deposits are not subject to a fee.*"
        bot.send_message(message.chat.id,a,parse_mode='markdown',reply_markup=deposit_markup())
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")
            



def get_deposit(message):
    N = 10
    try:
        if int(message.text) >= 10 : 
            print(int(message.text))
            bal=session.query(User).filter(User.chat_id==message.chat.id).one()
            if bal.email==None:
                deposit=payment.create_transaction(amount=int(message.text),currency1='TRX',currency2='TRX')
                print(deposit)
            else:
                deposit=payment.create_transaction(amount=int(message.text),currency1='TRX',currency2='TRX',buyer_email=bal.email)
            amount=deposit['result']['amount']
            txn=deposit['result']['txn_id']
            details=f'✅ *Transction Created Sucessfully*\n\n💲 *Amount* : {amount[:8]} TRX\n🔺 *Transction ID* : `{txn}`\n\n*Note :*\n🔺 You will get E-mail notification when transaction is completed\n🔺 It will be credited to your wallet after 3 confirmations'
            bot.send_message(message.chat.id,details,reply_markup=transaction_link_markup(deposit['result']['checkout_url']),parse_mode='markdown')
            
            session.add(Transaction(chat_id=message.chat.id,amt=amount,txn=txn,status_url=deposit['result']['status_url']))
            session.commit()
            session.add(Deposit(chat_id=message.chat.id,txn=txn))
            session.commit()
        else:
            bot.send_message(message.chat.id,"Minimum Deposit *10 TRX*",parse_mode='markdown')
    except Exception:
        bot.send_message(message.chat.id,"Invalid TRX")
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

@bot.message_handler(regexp='➖ Withdraw')
def withdraw_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    ip_list=session.query(IPWhitelist).all()
    g=[]
    for k in ip_list:
        g.append(k.address)
    if bal.ip == None or bal.ip == '' or bal.ip in g: 
        if bal.ban==False:
            if bal.earning >=minimum.min_withdraw:
                        N = 4
                        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                                    string.digits, k = N)) 
                        chat_id=message.chat.id                            
                        data=f'Send the amount of TRX\n\nAvailable Balance for payout: *{bal.earning} TRX*'
                        #get=session.query(Withdraw).filter(Withdraw.chat_id==message.chat.id).all()
                        session.add(Withdraw(chat_id=message.chat.id,username=message.from_user.username,message_id=res))
                        session.commit()
                        sent=bot.send_message(message.chat.id,data,parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                        bot.register_next_step_handler(sent,amount_withdrw,res)
            else:
                m=f'Your Balance for payout is too small to withdraw.\n\nAvailable Balance for payout: *{bal.earning} TRX*\n\nMinimum withdrawal: *{minimum.min_withdraw} TRX* '
                bot.send_message(message.chat.id,m,parse_mode='markdown')
        else:
                bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")
    else:
        ip=session.query(User).filter(User.ip==bal.ip).count()
        if bal.ban==False:
            if bal.earning >=minimum.min_withdraw:
                    if ip > 1:
                        bot.send_message('-1001372007234',f'IP :{bal.ip}')
                        data=f"📱 We found more than one account with your IP Address."
                        sent=bot.send_message(message.chat.id,data,parse_mode='markdown')
                    else:
                        N = 4
                        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                                    string.digits, k = N)) 
                        chat_id=message.chat.id                            
                        data=f'Send the amount of TRX\n\nAvailable Balance for payout: *{bal.earning} TRX*'
                        #get=session.query(Withdraw).filter(Withdraw.chat_id==message.chat.id).all()
                        session.add(Withdraw(chat_id=message.chat.id,username=message.from_user.username,message_id=res))
                        session.commit()
                        sent=bot.send_message(message.chat.id,data,parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                        bot.register_next_step_handler(sent,amount_withdrw,res)
            else:
                m=f'Your Balance for payout is too small to withdraw.\n\nAvailable Balance for payout: *{bal.earning} TRX*\n\nMinimum withdrawal: *{minimum.min_withdraw} TRX* '
                bot.send_message(message.chat.id,m,parse_mode='markdown')
        else:
                bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")
        

def amount_withdrw(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Withdrawal request has been canceled.",reply_markup=balance_markup())
        session.query(Withdraw).filter(Withdraw.message_id==res).delete()
        session.commit()
    else:
        amount=message.text
        try:
            if int(amount)>=minimum.min_withdraw:
                session.query(Withdraw).filter(Withdraw.message_id==res).update({Withdraw.amt:int(message.text)})
                session.commit()
                sent=bot.send_message(message.chat.id,"Send your TRX address",reply_markup=cancel_new_ad_markup())
                bot.register_next_step_handler(sent,address,res)
            else:
                bot.send_message(message.chat.id,"Minimum 20 TRX Needed")
        except Exception :
            bot.send_message(message.chat.id,"Invalid TRX")
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

def address(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Withdrawal request has been canceled.",reply_markup=balance_markup())
        session.query(Withdraw).filter(Withdraw.message_id==res).delete()
        session.commit()
    else:
        address_trx=message.text
        try:
            validate=tron_client.is_address(address_trx)
            if validate==True:
                session.query(Withdraw).filter(Withdraw.message_id==res).update({Withdraw.address:message.text})
                session.commit()
                a=session.query(Withdraw).filter(Withdraw.message_id==res).one()
                data=f'✅ <b>Your Withdrawal Request is Sucessful</b>\n\n Amount : {a.amt}\n Address : {a.address}\n\n 🔄 <i>Wating For Approval by Admin</i>'
                bot.send_message(message.chat.id,data,parse_mode='HTML')
                data_channel=f"ID:{res}\nChat ID :{message.chat.id}\nUsername : @{message.from_user.username}\nAmount : {a.amt}\nAddress :{a.address}\nStatus : Unconfirmed "
                bot.send_message('-1001437033283',data_channel,disable_web_page_preview=True,reply_markup=deposit_approve_markup(),parse_mode='HTML')
            else:
                sent=bot.send_message(message.chat.id,"🚫 *TRX address is Invaild*",parse_mode='markdown')
                bot.register_next_step_handler(sent,address,res)
        except:
            bot.send_message(message.chat.id,"🚫 *TRX address is Invaild*",parse_mode='markdown')
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

#@bot.message_handler(commands=['pay'])
def approve_handler(message):
    if message.chat.id in admin:
        text=message.text[4:8]
        try:    
            a=session.query(Withdraw).filter(Withdraw.message_id==text).one() 
            if a.status=='Unconfirmed':
                print(a.amt)
                priv_key = PrivateKey.fromhex(api_key.tron_key)
                txn = (
                    tron_client.trx.transfer(from_=api_key.tron_address,to=a.address,amount=int(str(int(a.amt))+'000000'))
                    .memo("From RapidClick BOT")
                    .build()
                    .inspect()
                    .sign(priv_key)
                    .broadcast()
                    
                    
                )
                print(txn)
                data=f'💰Your Withdrawal of <b>{a.amt} TRX</b> is Successful.\n\nTransaction ID : <a href="https://tronscan.org/#/transaction/{txn.txid}">{txn.txid}</a>'
                bot.send_message(a.chat_id,data,parse_mode="HTML",disable_web_page_preview=True)
                bot.send_message(message.chat.id,"Transaction Sucessfull")
                data=f'➕ New Withdraw:\n <b>{a.chat_id}</b> just withdrawal <b>{a.amt} TRX</b>\n\nTransaction ID : <a href="https://tronscan.org/#/transaction/{txn.txid}">{txn.txid}</a>'
                bot.send_message('@Rapidclick_Transactions',data,parse_mode='HTML',disable_web_page_preview=True)
                session.query(User).filter(User.chat_id==a.chat_id).update({User.balance:User.balance-(a.amt),User.earning:User.earning-(a.amt)})
                session.commit()
                session.query(Withdraw).filter(Withdraw.message_id==text).update({Withdraw.txn:txn.txid,Withdraw.status:'Confirmed'})
                session.commit()
        except Exception:
            bot.send_message(message.chat.id,"INCOMPLETE")
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
#

@bot.message_handler(regexp='🕧 Transaction Histoy')
def trans_hist(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        bot.send_message(message.chat.id,"*Choose the Transaction*",parse_mode='markdown',reply_markup=transaction_history_markup())
    else:
        bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")


@bot.message_handler(regexp='🔙 Go to Menu')
def menu_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        bot.send_message(message.chat.id,"✅ You're in Menu",reply_markup=start_markup())
    else:
        bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")


@bot.message_handler(regexp='⚙️ Settings')
def setting_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        bot.send_message(message.chat.id,"Choose a setting to edit below",reply_markup=setting_markup())
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='🖥    My Promotions    🖥')
def advertise_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        try:
            a=session.query(Ads).filter(Ads.chat_id==message.chat.id,Ads.complete=='Yes').count()
            bot.send_message(message.chat.id,f"You have *{a} Advertisments*",reply_markup=advertise_markup(),parse_mode='markdown')
            am=session.query(Ads).filter(Ads.chat_id==message.chat.id,Ads.complete=='Yes').all()
            for i in am:
                if i.ad_type=='site':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id),disable_web_page_preview=True)
                if i.ad_type=='bot':
                    regex = re.compile(
                    r'^https?://'  # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                    r'localhost|'  # localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?'  # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    if bool(regex.search(i.link))==True:
                        result=re.search('https://t.me/(.*)?start=',i.link)
                        user=result.group(1).replace('?','')

                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{user}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    else:
                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
                if i.ad_type=='channel':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
                if i.ad_type=='post':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nPost Message ID : {i.post_message}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
                if i.ad_type=='group':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nUsername : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nVerification: {i.verify}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
                if i.ad_type=='youtube':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.send_message(message.chat.id,a,parse_mode='markdown',reply_markup=manage_ad_markup(i.ad_id),disable_web_page_preview=True)
        except Exception:
            bot.send_message(message.chat.id,"You don't have any Advertisment",reply_markup=advertise_markup())
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='➕ Add New Advertisement')
def new_ad_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        a=session.query(Ads).filter(Ads.chat_id==message.chat.id,Ads.complete=='Yes').count()
        bot.send_message(message.chat.id,"What would you like to promote?👇",reply_markup=new_ad_markup())
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='❌ Cancel')
def cancel_ad_handler(message):
    bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())

@bot.message_handler(regexp='💻 Website/URL')
def web_ad_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        N = 10
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = N)) 
        session.add(Ads(chat_id=message.chat.id,ad_type='site',ad_id=res))
        session.commit()
        data=f"Advertise ID : {res}\n\nEnter the URL to send traffic to:\nNote : It should begin with https:// or http://"
        sent=bot.send_message(message.chat.id,data,reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,http_adder,res)
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")
    

@bot.message_handler(regexp='📲 Bots')
def bot_add(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        N = 10
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = N)) 
        session.add(Ads(chat_id=message.chat.id,ad_type='bot',ad_id=res))
        session.commit()
        data=f"Advertise ID : {res}\n\nEnter BOT URL or the Send the Bot Username:"
        sent=bot.send_message(message.chat.id,data,reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,http_adder,res)
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='📢 Channels')
def channel_add(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        N = 10
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = N)) 
        session.add(Ads(chat_id=message.chat.id,ad_type='channel',ad_id=res))
        session.commit()
        data=f"Advertise ID : {res}\n\nMake this bot admin and Forward the message from that channel "
        sent=bot.send_message(message.chat.id,data,reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,http_adder,res)
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='👁 Post')
def post_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        N = 10
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = N)) 
        session.add(Ads(chat_id=message.chat.id,ad_type='post',ad_id=res))
        session.commit()
        data=f"Advertise ID : {res}\n\n Forward the Post from the channel which you wan to promote:\n\n🔺 Note : Bot must be admin in that channel"
        sent=bot.send_message(message.chat.id,data,reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,http_adder,res)
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

@bot.message_handler(regexp='👥 Group')
def group_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        N = 10
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = N)) 
        session.add(Ads(chat_id=message.chat.id,ad_type='group',ad_id=res))
        session.commit()
        data=f"Advertise ID : {res}\n\nPlease send Group username"
        sent=bot.send_message(message.chat.id,data,reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,http_adder,res)
    else:
        bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")


@bot.message_handler(regexp='▶️ Youtube')
def yt__handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        N = 10
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = N)) 
        session.add(Ads(chat_id=message.chat.id,ad_type='youtube',ad_id=res))
        session.commit()
        data=f"Advertise ID : {res}\n\nPlease send Youtube Link"
        sent=bot.send_message(message.chat.id,data,reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,http_adder,res)
    else:
        bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")

def http_adder(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    else:
        z=session.query(Ads).filter(Ads.ad_id==res).one()
        if z.ad_type=='site':
            url=message.text
            regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if bool(regex.search(url))==True:
                response=requests.get(message.text)
                if response.status_code==200:
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:url})
                    session.commit()
                    sent=bot.send_message(message.chat.id,"Enter a title for your ad:\n\n*Note :* It must be between 5 and 80 characters.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,title_adder,res)
                else:
                    bot.send_message(message.chat.id,f"❌ Invalid URL \n\n *Status Code :* {response.status_code}",parse_mode='markdown',reply_markup=advertise_markup())
            else:
                bot.send_message(message.chat.id,f"❌ Invalid URL",reply_markup=advertise_markup())
        if z.ad_type=='youtube':
            url=message.text
            regex = re.compile(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')
            if bool(regex.search(url))==True:
                print(video_id(url))
                response=requests.get(message.text)
                if response.status_code==200:
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:"https://www.youtube.com/embed/"+video_id(url)})
                    session.commit()
                    sent=bot.send_message(message.chat.id,"Enter a title for your ad:\n\n*Note :* It must be between 5 and 80 characters.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,title_adder,res)
                else:
                    bot.send_message(message.chat.id,f"❌ Invalid URL \n\n *Status Code :* {response.status_code}",parse_mode='markdown',reply_markup=advertise_markup())
            else:
                bot.send_message(message.chat.id,f"❌ Invalid URL",reply_markup=advertise_markup())



        if z.ad_type=='bot':
            regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if bool(re.search('@',message.text))==True:
                user=message.text.replace("@",'')
                sent=bot.send_message(message.chat.id,f"Please forward any message from {message.text} to this chat:")
                bot.register_next_step_handler(sent,forwardhandler,res,user)
            elif bool(regex.search(message.text))==True:
                try:
                    result=re.search('https://t.me/(.*)?start=',message.text)
                    print(result.group(1).replace('?',''))
                    sent=bot.send_message(message.chat.id,f"Please forward any message from @{result.group(1).replace('?','')} to this chat:")
                    bot.register_next_step_handler(sent,forwardhandler,res,message.text)
                except:
                    bot.send_message(message.chat.id,"Bot URL is Invalid ,Try With Username")
            else:
                bot.send_message(message.chat.id,"Invalid Username",reply_markup=advertise_markup())
                session.query(Ads).filter(Ads.ad_id==res).delete()
                session.commit()
        if z.ad_type=='channel':
            try:
                a=bot.get_chat_member(message.forward_from_chat.id,1023938466)
                if a.status =='administrator':
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:message.forward_from_chat.username})
                    session.commit()
                    sent=bot.send_message(message.chat.id,"Enter a title for your ad:\n\n*Note :* It must be between 5 and 80 characters.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,title_adder,res)
                else:
                    bot.send_message(message.chat.id,"Bot is not admin in chat\n\nMake this bot admin and Forward the message from that channel:",reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,http_adder,res)
            except:
                bot.send_message(message.chat.id,"Invalid Post Info",reply_markup=advertise_markup())
                session.query(Ads).filter(Ads.ad_id==res).delete()
                session.commit()
        if z.ad_type=='post':
            try:
                session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:message.forward_from_chat.username,Ads.post_message:message.forward_from_message_id})
                session.commit()
                sent=bot.send_message(message.chat.id," What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  0.07  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                bot.register_next_step_handler(sent,ppc_adder,res)
            except :
                bot.send_message(message.chat.id,"Invalid Post Info",reply_markup=advertise_markup())
                session.query(Ads).filter(Ads.ad_id==res).delete()
                session.commit()
        if z.ad_type=='group':
            if bool(re.search('@',message.text))==True:
                user=message.text.replace("@",'')
                session.add(Testgroup(username=user,ad_id=res))
                session.commit()
                sent=bot.send_message(message.chat.id,f"Please send /verify@botname in {message.text}")
                bot.register_next_step_handler(sent,forwardhandler,res,user)
            else:
                bot.send_message(message.chat.id,"Invalid Username",reply_markup=advertise_markup())
                session.query(Ads).filter(Ads.ad_id==res).delete()
                session.commit()




@bot.message_handler(commands=['verify'])
def verify_group(message):
    
    try:
        a=session.query(Testgroup).filter(Testgroup.username==message.chat.username).one()
        z=session.query(Ads).filter(Ads.ad_id==a.ad_id).one()
        res=z.ad_id
        if message.chat.type=='supergroup':
            if message.from_user.id==z.chat_id:
                ad=bot.get_chat_member(message.chat.id,1023938466)
                if ad.status =='administrator':
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:message.chat.username})
                    sent=bot.send_message(message.from_user.id,"Enter a title for your ad:\n\n*Note :* It must be between 5 and 80 characters.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,title_adder,res)
                else:
                    bot.send_message(message.from_user.id,f"Bot is not admin in @{message.chat.username} ")
            else:
                bot.send_message(message.from_user.id,f"You're not valid user to send command in @{message.chat.username}")
        else:
            bot.send_message(message.from_user.id,"It is not Supergroup.")

    except sqlalchemy.orm.exc.NoResultFound:
        bot.send_message(message.from_user.id,"Invalid Action")
    except:
        bot.send_message(message.from_user.id,'Aww :) Something went wrong . Please Try again later')
    session.query(Testgroup).filter(Testgroup.username==message.chat.username).delete()
    session.commit()

def video_id(value):
    query = urllib.parse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


def forwardhandler(message,res,user):
    z=session.query(Ads).filter(Ads.ad_id==res).one()
    if z.ad_type=='bot':
        regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if bool(regex.search(user))==True:
                print(user)
                result=re.search('https://t.me/(.*)?start=',user)
                username=result.group(1).replace('?','')
                print(username)
                if message.forward_from.username==username and message.forward_from.is_bot==True:
                        today = datetime.date(datetime.now())
                        yesterday = today - timedelta(days=1)
                        unixtime = time.mktime(yesterday.timetuple())
                        if message.forward_date>=unixtime:
                            session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:user})
                            session.commit()
                            sent=bot.send_message(message.chat.id,"Enter a title for your ad:\n\n*Note :* It must be between 5 and 80 characters.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                            bot.register_next_step_handler(sent,title_adder,res)
                        else:
                            sent=bot.send_message(message.chat.id,"The message you forwarded is too old. 🕰\n\nPlease send a newer message from bot.")
                            bot.register_next_step_handler(sent,forwardhandler,res,user)
                else:
                    bot.send_message(message.chat.id,"Username Not Found",reply_markup=advertise_markup())
                    session.query(Ads).filter(Ads.ad_id==res).delete()
                    session.commit()
        else:
            if message.forward_from.username==user and message.forward_from.is_bot==True:
                    today = datetime.date(datetime.now())
                    yesterday = today - timedelta(days=1)
                    unixtime = time.mktime(yesterday.timetuple())
                    if message.forward_date>=unixtime:
                        session.query(Ads).filter(Ads.ad_id==res).update({Ads.link:user})
                        sent=bot.send_message(message.chat.id,"Enter a title for your ad:\n\n*Note :* It must be between 5 and 80 characters.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                        bot.register_next_step_handler(sent,title_adder,res)
                    else:
                        sent=bot.send_message(message.chat.id,"The message you forwarded is too old. 🕰\n\nPlease send a newer message from bot.")
                        bot.register_next_step_handler(sent,forwardhandler,res,user)
            else:
                bot.send_message(message.chat.id,"Username Not Found",reply_markup=advertise_markup())
                session.query(Ads).filter(Ads.ad_id==res).delete()
                session.commit()
        
    


def title_adder(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    else:
        if len(message.text) >=5 and len(message.text) <= 80:
            session.query(Ads).filter(Ads.ad_id==res).update({Ads.title:message.text})
            session.commit()
            sent=bot.send_message(message.chat.id,"Enter a description for your advertisment\n\nIt must be between 10 and 180 characters.")
            bot.register_next_step_handler(sent,description_adder,res)
        else:
            again=bot.send_message(message.chat.id,"Please enter a title between 5 and 80 characters.")
            bot.register_next_step_handler(again,title_adder,res)

def description_adder(message,res):  
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    else:

        if len(message.text) >=10 and len(message.text) <= 180:
            session.query(Ads).filter(Ads.ad_id==res).update({Ads.desc:message.text})
            session.commit()
            sent=bot.send_message(message.chat.id,"Does your advertisement contain *pornographic / NSFW* content?",parse_mode='markdown',reply_markup=nsfw_ad_markup())
            bot.register_next_step_handler(sent,nsfw_adder,res)
        else:
            again=bot.send_message(message.chat.id,"Please enter a title between 10 and 180 characters.")
            bot.register_next_step_handler(again,description_adder,res)

def nsfw_adder(message,res):
    z=session.query(Ads).filter(Ads.ad_id==res).one()
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    elif message.text=='✅ Yes':
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.porn:'Yes'})
        session.commit()
        if z.ad_type=='site':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is {minimum.min_cpc_site} TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='bot':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  {minimum.min_cpc_bot}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='channel':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  {minimum.min_cpc_channel}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='post':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  {minimum.min_cpc_post}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='group':
            sent=bot.send_message(message.chat.id," You need users to verify by specific text or comment?",parse_mode='markdown',reply_markup=verify_ad_markup())
            bot.register_next_step_handler(sent,group_veri,res)
        if z.ad_type=='youtube':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  {minimum.min_cpc_yt}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
    elif message.text=='🚫 No':
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.porn:'No'})
        session.commit()
        if z.ad_type=='site':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is {minimum.min_cpc_site} TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='bot':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is {minimum.min_cpc_bot}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='channel':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  {minimum.min_cpc_channel}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        if z.ad_type=='group':
            sent=bot.send_message(message.chat.id," You need users to verify by specific text or comment?",parse_mode='markdown',reply_markup=verify_ad_markup())
            bot.register_next_step_handler(sent,group_veri,res)
        if z.ad_type=='youtube':
            sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is  {minimum.min_cpc_yt}  TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        
    else:
        sent=bot.send_message(message.chat.id,"Invalid Data..!",reply_markup=nsfw_ad_markup())
        bot.register_next_step_handler(sent,nsfw_adder,res)

def group_veri(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    elif message.text=='🔺 Yes':
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.verify:True})
        session.commit()
        sent=bot.send_message(message.chat.id," Send the text or comment  between 5 to 100 letters\n\n▪️ Note : User get there earnings when the send this text on your group.",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,add_comment,res)
    elif message.text=='🔻 No':
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.porn:False})
        session.commit()
        sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is {minimum.min_cpc_group} TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,ppc_adder,res)

def add_comment(message,res):
    if len(message.text)>=5 and len(message.text)<=100:
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.comment:message.text})
        session.commit()
        sent=bot.send_message(message.chat.id,f" What is the max you want to *Pay Per Click?*\n\nThe minimum amount is {minimum.min_cpc_group} TRX.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,ppc_adder,res)
    else:
        again=bot.send_message(message.chat.id,"Please enter a title between 5 and 100 characters.")
        bot.register_next_step_handler(again,add_comment,res)

def ppc_adder(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    else:
        z=session.query(Ads).filter(Ads.ad_id==res).one()
        try:
            adg=float(message.text)
            if z.ad_type=='site':
                if adg>=minimum.min_cpc_site:
                    ppc_nu(message,adg,res)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_site}* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,ppc_adder,res)
            if z.ad_type =='bot':
                if adg>=minimum.min_cpc_bot:
                    ppc_nu(message,adg,res)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_bot}* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,ppc_adder,res)
            if z.ad_type=='channel':
                if adg>=minimum.min_cpc_channel:
                    ppc_nu(message,adg,res)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_channel}* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,ppc_adder,res)
            if z.ad_type=='youtube':
                if adg>=minimum.min_cpc_yt:
                    ppc_nu(message,adg,res)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_yt}* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,ppc_adder,res)
            if z.ad_type=='post':
                if adg>=minimum.min_cpc_post:
                    ppc_nu(message,adg,res)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter value between *{minimum.min_cpc_post}* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,ppc_adder,res)
            if z.ad_type=='group':
                if adg>=minimum.min_cpc_group:
                    ppc_nu(message,adg,res)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_group}* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,ppc_adder,res)
        except Exception:
            sent=bot.send_message(message.chat.id,"You must enter a value between *0.20* and *25 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,ppc_adder,res)
        
def ppc_nu(message,adg,res):
    a=session.query(User).filter(User.chat_id==message.chat.id).one()
    z=session.query(Ads).filter(Ads.ad_id==res).one()
    if adg <=a.balance:
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
        session.commit()
        if z.ad_type=='site':
            sent=bot.send_message(message.chat.id,f"How much do you want to spend per day?\n\nThe minimum amount is *{minimum.min_budget_site} TRX*.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
        if z.ad_type=='bot':
            sent=bot.send_message(message.chat.id,f"How much do you want to spend per day?\n\nThe minimum amount is *{minimum.min_budget_bot} TRX*.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
        if z.ad_type=='channel':
            sent=bot.send_message(message.chat.id,f"How much do you want to spend per day?\n\nThe minimum amount is *{minimum.min_budget_channel} TRX*.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
        if z.ad_type=='post':
            sent=bot.send_message(message.chat.id,f"How much do you want to spend per day?\n\nThe minimum amount is *{minimum.min_budget_post} TRX*.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
        if z.ad_type=='group':
            sent=bot.send_message(message.chat.id,f"How much do you want to spend per day?\n\nThe minimum amount is *{minimum.min_budget_group} TRX*.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
        if z.ad_type=='youtube':
            sent=bot.send_message(message.chat.id,f"How much do you want to spend per day?\n\nThe minimum amount is *{minimum.min_budget_yt} TRX*.\n\nEnter a value in TRX:",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
    else:
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
        bot.send_message(message.chat.id,"🔺 Insufficient TRX your Account Please Deposit",reply_markup=advertise_markup())


def spend_per_add(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your advertisment has been canceled.",reply_markup=advertise_markup())
        session.query(Ads).filter(Ads.ad_id==res).delete()
        session.commit()
    else:
        z=session.query(Ads).filter(Ads.ad_id==res).one()
        try:
            msd=float(message.text)
            if z.ad_type=='site':
                if msd>=minimum.min_budget_site:
                    spend_per(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_site}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,spend_per_add,res)
            if z.ad_type=='bot':
                if msd>=minimum.min_budget_bot:
                    spend_per(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_bot}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,spend_per_add,res)
            if z.ad_type=='channel':
                if msd>=minimum.min_budget_channel:
                    spend_per(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_channel}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,spend_per_add,res)
            if z.ad_type=='post':
                if msd>=minimum.min_budget_post:
                    spend_per(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_post}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,spend_per_add,res)
            if z.ad_type=='group':
                if msd>=minimum.min_budget_group:
                    spend_per(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_group}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,spend_per_add,res)
            if z.ad_type=='youtube':
                if msd>=minimum.min_budget_yt:
                    spend_per(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_yt}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,spend_per_add,res)
        except Exception:
            
            sent=bot.send_message(message.chat.id,"Invalid TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,spend_per_add,res)
            
def spend_per(message,res,msd):
    a=session.query(User).filter(User.chat_id==message.chat.id).one()

    if msd <= a.balance:
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.budget:msd,Ads.complete:'Yes',Ads.r_balance:msd})
        session.commit()
        session.query(User).filter(User.chat_id==message.chat.id).update({User.ads_count:User.ads_count+1})
        session.commit()
        bot.send_message(message.chat.id,"Advertisement Created Sucessfully",reply_markup=advertise_markup())
        am=session.query(Ads).filter(Ads.chat_id==message.chat.id,Ads.complete=='Yes').all()
        for i in am:
            if i.ad_type=='site':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,disable_web_page_preview=True,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='bot':
                regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if bool(regex.search(i.link))==True:
                    result=re.search('https://t.me/(.*)?start=',i.link)
                    user=result.group(1).replace('?','')

                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{user}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                else:
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\n*Status : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='channel':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='post':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nPost Message ID : {i.post_message}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='group':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nUsername : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nVerification: {i.verify}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='youtube':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,parse_mode='markdown',reply_markup=manage_ad_markup(i.ad_id),disable_web_page_preview=True)
    else:
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.budget:msd,Ads.r_balance:msd,Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached ',Ads.complete:'Yes'})
        session.commit()
        bot.send_message(message.chat.id,"🔺 Insufficient TRX your Acoount Please Deposit",reply_markup=advertise_markup())
        am=session.query(Ads).filter(Ads.chat_id==message.chat.id,Ads.complete=='Yes').all()
        for i in am:
            if i.ad_type=='site':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,parse_mode='markdown',reply_markup=manage_ad_markup(i.ad_id),disable_web_page_preview=True)
            if i.ad_type=='bot':
                regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if bool(regex.search(i.link))==True:
                    result=re.search('https://t.me/(.*)?start=',i.link)
                    user=result.group(1).replace('?','')

                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{user}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}\nRemaining Budget : {i.r_balance}"
                else:
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,parse_mode='markdown',reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='channel':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='post':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nPost Message ID : {i.post_message}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='group':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nUsername : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nVerification: {i.verify}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,reply_markup=manage_ad_markup(i.ad_id))
            if i.ad_type=='youtube':
                a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                bot.send_message(message.chat.id,a,parse_mode='markdown',reply_markup=manage_ad_markup(i.ad_id),disable_web_page_preview=True)

@bot.message_handler(regexp='ℹ️ Info')
def info_handler(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        all_data="""Welcome to Rapid Click Bot.

Here's how you can earn with our Bot.

1⃣ Join channels:
1. Press 📣 and wait for an ad to show up.
2. Go to the Telegram Channel and join it.
3. Press ✅ Joined and stay in the chat to get your reward.

2⃣ Visit websites:
1. Press 🌐 and wait for an ad to show up.
2. Press 🌐 Go to website to visit the site.
3. Stay on the site for the required amount of time to get your reward. 

3⃣ YouTube Videos:
1. Press ▶️ and wait for an ad to show up.
2. Press ▶️ YouTube video and you will be redirect to third part website, Stay on the site for the required amount of time to get your reward.

4⃣ Message bots:
1. Press 🤖 and wait for an ad to show up.
2. Press 🤖 Message bot and you will be redirected to the bot, then join to the bot.
3. Forward the message you get from the bot back to @Rapidclickbot to get your reward.

5⃣ Group Joins:
1. Press 👥 and wait for an ad to show up.
2. Go to the Telegram Group and join it.
3. Press ✅ Joined and copy given comment to send in group and stay in the chat to get your reward.

6⃣ View Posts:
1. Press 📄 and wait for an post to show up.
2. Read the post for 10 seconds.
3. Click ✅ Watched to claim your reward.

Official Support:
https://t.me/RapidClick_support 

Official  Channel:
https://t.me/Rapidclick_Announcment

Transactions:
https://t.me/Rapidclick_Transactions"""
        bot.send_message(message.chat.id,all_data,disable_web_page_preview=True,reply_markup=info_markup())
    else:
            bot.send_message(message.from_user.id,"Aww :) , You're Banned..!")


@bot.message_handler(regexp='🤖')
def message_bot_handler(message):
    bot_handle(message)


def bot_handle(message):
    list_=[]
    try:
        m=session.query(Alert).filter(Alert.chat_id==message.chat.id).one()
        n=session.query(Task).filter(Task.chat_id==message.chat.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            if m.nsfw=='Enabled🔔':
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='bot',Ads.username_needed=='No').all()
                    
            else:  
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='bot',Ads.porn=='No',Ads.username_needed=='No').all()
        else:
            if m.nsfw=='Enabled🔔':
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='bot.').all()
            else: 
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='bot',Ads.porn=='No').all()

        for i in a:
                    list_.append(i.ad_id)
        no=random.choice(list_)
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        data=f"*{z.title}*\n\n{z.desc}\n\n__⚠️ You will be redirected to a third party telegram bot.__\n\n---------------------\n1️⃣ Press the *Message bot* botton below.\n2️⃣ Send the bot a message using its *start* function.\n3️⃣ Click on ✅ Done"
        bot.send_message(message.chat.id,data,parse_mode='markdown',reply_markup=bot_task_markup(z.link))
        session.add(Task(chat_id=message.chat.id,ad_id=no))
        session.commit()
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new bot tasks are __{m.bots}__.\nNSFW advertisements are __{m.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message(message.chat.id,data,parse_mode='markdown')
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')



@bot.message_handler(regexp='📣')
def join_channel_handler(message):

            channel_handle(message)





def channel_handle(message):
    list_=[]
    try:
        m=session.query(Alert).filter(Alert.chat_id==message.chat.id).one()
        n=session.query(Task).filter(Task.chat_id==message.chat.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            if m.nsfw=='Enabled🔔':
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='channel',Ads.username_needed=='No').all()
                    
            else:  
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='channel',Ads.porn=='No',Ads.username_needed=='No').all()
        else:
            if m.nsfw=='Enabled🔔':
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='channel').all()
            else: 
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='channel',Ads.porn=='No').all()
        for i in a:
            list_.append(i.ad_id)
        no=random.choice(list_)
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        q=[]
        g=session.query(CheckUser).filter(CheckUser.chat_id==message.chat.id).all()
        for w in g:
            q.append(w.username)
        username='@'+z.link
        if username in q:
            channel_handle(message)
        else:
            data=f'{z.title}\n\n{z.desc}\n\n⚠️ You have to join Third party Telegram channel.\n\n---------------------\nYou must join @{z.link} to earn TRX.After joining the channel, press the "Joined" button.'
            bot.send_message(message.chat.id,data,reply_markup=channel_task_markup(z.link))
            session.add(Task(chat_id=message.chat.id,ad_id=no))
            session.commit()
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new Channel tasks are __{m.channel}__.\nNSFW advertisements are __{m.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message(message.chat.id,data,parse_mode='markdown')
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

@bot.message_handler(regexp='📄')
def viewpost_handler(message):
   
            post_handle(message)

def post_handle(message):
    list_=[]
    try:
        m=session.query(Alert).filter(Alert.chat_id==message.chat.id).one()
        n=session.query(Task).filter(Task.chat_id==message.chat.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='post',Ads.username_needed=='No').all()
        else:
            a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='post').all()
        
        for i in a:
            
            list_.append(i.ad_id)

        no=random.choice(list_)
    
       
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        data=f'View ID :`{z.ad_id}`\n\n*View the post for at least 10 seconds...*\n\n__Click on ✅ Read Post to proceed__'
        bot.send_message(message.chat.id,data,parse_mode='markdown',reply_markup=post_task_markup())
        session.add(Task(chat_id=message.chat.id,ad_id=no))
        session.commit()
                
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new Post tasks are __{m.post}__.\nNSFW advertisements are __{m.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message(message.chat.id,data,parse_mode='markdown')
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')




@bot.message_handler(regexp="🌐")
def site_handler(message):
    site_handle(message)
    


def site_handle(message):
    list_=[]
    try:
        m=session.query(Alert).filter(Alert.chat_id==message.chat.id).one()
        n=session.query(Task).filter(Task.chat_id==message.chat.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            if m.nsfw=='Enabled🔔':
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='site',Ads.username_needed=='No').all()
                    
            else:  
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='site',Ads.porn=='No',Ads.username_needed=='No').all()
        else:
            if m.nsfw=='Enabled🔔':
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='site').all()
            else: 
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='site',Ads.porn=='No').all()

        for i in a:
            list_.append(i.ad_id)
        no=random.choice(list_)
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        data=f'*{z.title}*\n\n{z.desc}\n\n_You are redirecting to third party website_\n'
        url="http://162.0.230.68:5000/short?longurl={}&chat_id={}&ad={}".format(z.link,message.chat.id,z.ad_id)
        short_url=requests.get(url).json()

        bot.send_message(message.chat.id,data,parse_mode='markdown',reply_markup=site_task_markup(short_url['short_url']))
        session.add(Task(chat_id=message.chat.id,ad_id=no))
        session.commit()    
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new Post tasks are __{m.post}__.\nNSFW advertisements are __{m.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
        bot.send_message(message.chat.id,data,parse_mode='markdown')


@bot.message_handler(regexp="▶️")
def yt_handler(message):
    yt_handle(message)
    


def yt_handle(message):
    list_=[]
    try:
        m=session.query(Alert).filter(Alert.chat_id==message.chat.id).one()
        n=session.query(Task).filter(Task.chat_id==message.chat.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            if m.nsfw=='Enabled🔔':
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='youtube',Ads.username_needed=='No').all()
                    
            else:  
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='youtube',Ads.porn=='No',Ads.username_needed=='No').all()
        else:
            if m.nsfw=='Enabled🔔':
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='youtube').all()
            else: 
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='youtube',Ads.porn=='No').all()

        for i in a:
            list_.append(i.ad_id)
        no=random.choice(list_)
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        data=f'*{z.title}*\n\n{z.desc}\n\n_You are redirecting to third party website_\n'
        url="http://162.0.230.68:5000/yt?longurl={}&chat_id={}&ad={}".format(z.link,message.chat.id,z.ad_id)
        short_url=requests.get(url).json()

        bot.send_message(message.chat.id,data,parse_mode='markdown',reply_markup=site_task_markup(short_url['short_url']))
        session.add(Task(chat_id=message.chat.id,ad_id=no))
        session.commit()    
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new Post tasks are __{m.post}__.\nNSFW advertisements are __{m.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
        bot.send_message(message.chat.id,data,parse_mode='markdown')



@bot.message_handler(regexp="👥")
def group_handlr(message):
            group_handle_unverified(message)

def group_handle(message):
    list_=[]
    k=session.query(Alert).filter(Alert.chat_id==message.from_user.id).one()
    try:
        
        n=session.query(Task).filter(Task.chat_id==message.from_user.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            if k.nsfw=='Enabled🔔':
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group',Ads.username_needed=='No').all()
                    
            else:  
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group',Ads.porn=='No',Ads.username_needed=='No').all()
        else:
            if k.nsfw=='Enabled🔔':
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group').all()
            else: 
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group',Ads.porn=='No').all()
        for i in a:
            list_.append(i.ad_id)
            print(i.ad_id)
        no=random.choice(list_)
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        q=[]
        g=session.query(CheckUser).filter(CheckUser.chat_id==message.from_user.id).all()
        for w in g.username:
            q.append(w)
        username='@'+z.link
        if username in q:
            group_handle(message)
        else:
            data=f'{z.title}\n\n{z.desc}\n\n⚠️ You have to join Third party Telegram group.\n\n---------------------\nYou must join @{z.link} and verify to earn TRX.After joining the channel, press the "Joined" button.'
            bot.send_message(message.from_user.id,data,reply_markup=group_task_markup(z.link))
            session.add(Task(chat_id=message.from_user.id,ad_id=no))
            session.commit()
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new Channel tasks are __{k.channel}__.\nNSFW advertisements are __{k.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message(message.from_user.id,data,parse_mode='markdown')
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    
def group_handle_unverified(message):
    list_=[]
    
    try:
        k=session.query(Alert).filter(Alert.chat_id==message.chat.id).one()
        n=session.query(Task).filter(Task.chat_id==message.chat.id).all()
        f=[]
        for j in n:
            f.append(j.ad_id)
        if message.chat.username==None:
            if k.nsfw=='Enabled🔔':
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group',Ads.username_needed=='No').all()
                    
            else:  
                    a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group',Ads.porn=='No',Ads.username_needed=='No').all()
        else:
            if k.nsfw=='Enabled🔔':
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group').all()
            else: 
                a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group',Ads.porn=='No').all()

        for i in a:
            list_.append(i.ad_id)
        print(list_)    
        no=random.choice(list_)
        print(no)
        z=session.query(Ads).filter(Ads.ad_id==no).one()
        q=[]
        g=session.query(CheckUser).filter(CheckUser.chat_id==message.chat.id).all()
        for w in g:
            q.append(w.username)
        username='@'+z.link
        if username in q:
            group_handle_unverified(message)
        else:
            data=f'{z.title}\n\n{z.desc}\n\n⚠️ You have to join Third party Telegram group.\n\n---------------------\nYou must join @{z.link} and verify to earn TRX.After joining the channel, press the "Joined" button.'
            bot.send_message(message.chat.id,data,reply_markup=group_task_markup(z.link))
            session.add(Task(chat_id=message.chat.id,ad_id=no))
            session.commit()
    except Exception:
        data=f"Sorry, there are no new ads available. 😟\n\nAlerts for new Channel tasks are __{k.channel}__.\nNSFW advertisements are __{k.nsfw}__.\n\nUse the ⚙️ *Settings* command to change your preferences"
        bot.send_message(message.chat.id,data,parse_mode='markdown')
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

@bot.message_handler(regexp='📊 Statastics')
def stats_handelr(message):
    a=session.query(User).count()
    c=session.query(Transaction).filter(Transaction.status=='Confirmed').count()
    d=session.query(Withdraw).filter(Withdraw.status=='Confirmed').count()
    data=f"Admin ID :*1247719165*\nDate : *11th August 2020* \nTotal Users : *{a}*\nPremium Users : *{b}*\nTotal Deposit : *{c}*\nTotal Withdraw : *{d}*"
    bot.send_message(message.chat.id,data,parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: True)
def handler_query(call):
    if call.data=='cancel_transc':
        try:
            bot.delete_message(call.message.chat.id,call.message.message_id)
            bot.send_message(call.message.chat.id,"⛔️ Transction Teraminated",reply_markup=start_markup())
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='deposit_history':
        try:
            m=session.query(Transaction).filter(Transaction.chat_id==call.message.chat.id,Transaction.status=='Confirmed').all()
            a=''
            for i in m:
                a+=f'\n\nTransaction ID :{i.txn}\nAmount : {str(i.amt)}\nStatus : {i.status}\n<a href="{i.status_url}"> More details </a>\n\n'
            try:
                bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='HTML',disable_web_page_preview=True)
            except Exception:
                bot.edit_message_text("*You Don't have any Deposit yet.*",chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown') 
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='withdraw_history':
        try:
            n=session.query(Withdraw).filter(Withdraw.chat_id==call.message.chat.id).all()
            a=''
            for i in n:
                a+=f'\n\nTransaction ID :{i.txn}\nAmount : {str(i.amt)}\nStatus : {i.status}\nTRX Address :{i.address}\n\n'
            try:
                bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='HTML',disable_web_page_preview=True)
            except Exception:
                bot.edit_message_text("*You Don't have any Withdrawal yet.*",chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown') 
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='porn':
        try:
            a=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            bot.edit_message_text(f"🔞 NSFW/pornographic ads are currently *{a.nsfw}* .",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=nsfw_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='set_back':
        try:
            bot.edit_message_text("Choose a setting to edit below",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=setting_markup())
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='nsfw_button_off':
        
        off=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
        session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.nsfw:'Disabled🔕'})
        session.commit()
        try:
            bot.edit_message_text(f"🔞 NSFW/pornographic ads are currently *{off.nsfw}* .",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=nsfw_markup(call.message.chat.id),parse_mode='markdown')
        except Exception as e:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
            #bot.send_message(call.message.chat.id,"Aww :( , Something went wrong .Please try again later.")
            
            
    if call.data=='nsfw_button_on':
        try:
            on=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.nsfw:'Enabled🔔'})
            session.commit()
            bot.edit_message_text(f"🔞 NSFW/pornographic ads are currently *{on.nsfw}* .",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=nsfw_markup(call.message.chat.id),parse_mode='markdown')
        except Exception as e:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
            #bot.send_message(call.message.chat.id,"Aww :( , Something went wrong .Please try again later.")
            
    if call.data=='task':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='sites_button_off':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.sites:'Disabled🔕'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='sites_button_on':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.sites:'Enabled🔔'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='channel_button_off':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.channel:'Disabled🔕'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='channel_button_on':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.channel:'Enabled🔔'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='bots_button_on':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.bots:'Enabled🔔'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='bots_button_off':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.bots:'Disabled🔕'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='post_button_off':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.post:'Disabled🔕'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='post_button_on':
        try:
            m=session.query(Alert).filter(Alert.chat_id==call.message.chat.id).one()
            session.query(Alert).filter(Alert.chat_id==call.message.chat.id).update({Alert.post:'Enabled🔔'})
            session.commit()
            data=f"Here are your settings for new task alerts.\n\nVisit sites : *{m.sites}*\nMessage bots : *{m.bots}*\nJoin chats :  *{m.channel}*\nView Posts : *{m.post}*\n\nUse the buttons below to turn on/off alerts for each task."
            bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=task_markup(call.message.chat.id),parse_mode='markdown')
        except Exception :
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='ad_delete':
        try:
            ad_id=call.message.text[19:29]
            session.query(Ads).filter(Ads.ad_id==ad_id).delete()
            session.commit()
            session.query(User).filter(User.chat_id==call.message.chat.id).update({User.ads_count:User.ads_count-1})
            session.commit()
            session.query(Task).filter(Task.ad_id==ad_id).delete()
            session.commit()
            bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,"🗑 Your Advertisement is Deleted")
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
        
    if call.data=="ad_dis":
        try:
                ad_id=call.message.text[19:29]
                z=session.query(Ads).filter(Ads.ad_id==ad_id).one()
                session.query(Ads).filter(Ads.ad_id==ad_id).update({Ads.status:'Disabled🔕'})
                session.commit()
                i=session.query(Ads).filter(Ads.ad_id==ad_id).one()
                if i.ad_type=='site':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id),disable_web_page_preview=True)
                if i.ad_type=='bot':
                    regex = re.compile(
                    r'^https?://'  # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                    r'localhost|'  # localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?'  # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    if bool(regex.search(i.link))==True:
                        result=re.search('https://t.me/(.*)?start=',i.link)
                        user=result.group(1).replace('?','')

                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{user}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    else:
                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='channel':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='post':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nPost Message ID : {i.post_message}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\n\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='group':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nUsername : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nVerification: {i.verify}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='youtube':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id),disable_web_page_preview=True)
            
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=="ad_en":
        try:
            ad_id=call.message.text[19:29]
            z=session.query(Ads).filter(Ads.ad_id==ad_id).one()
            user=session.query(User).filter(User.chat_id==z.chat_id).one()
            if z.r_balance < user.balance and z.r_balance > z.ppc:
                session.query(Ads).filter(Ads.ad_id==ad_id).update({Ads.status:'Enabled🔔'})
                session.commit()
                i=session.query(Ads).filter(Ads.ad_id==ad_id).one()
                if i.ad_type=='site':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='bot':
                    regex = re.compile(
                    r'^https?://'  # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                    r'localhost|'  # localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?'  # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    if bool(regex.search(i.link))==True:
                        result=re.search('https://t.me/(.*)?start=',i.link)
                        user=result.group(1).replace('?','')

                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{user}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    else:
                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='channel':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='post':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nPost Message ID :\{i.post_message}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='group':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nUsername : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nVerification: {i.verify}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='youtube':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id),disable_web_page_preview=True)
            else:
                session.query(Ads).filter(Ads.ad_id==z.ad_id).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
                session.commit()
                i=session.query(Ads).filter(Ads.ad_id==ad_id).one()
                if i.ad_type=='site':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='bot':
                    regex = re.compile(
                    r'^https?://'  # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                    r'localhost|'  # localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?'  # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    if bool(regex.search(i.link))==True:
                        result=re.search('https://t.me/(.*)?start=',i.link)
                        user=result.group(1).replace('?','')

                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{user}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    else:
                        a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nBot Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='channel':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='post':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nChannel Username : @{i.link}\nPost Message ID :\{i.post_message}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='group':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nUsername : @{i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nVerification: {i.verify}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
                if i.ad_type=='youtube':
                    a=f"Advertisement ID : {i.ad_id}\nType : {i.ad_type}\nURL : {i.link}\nTitle : {i.title}\nDescription  : {i.desc}\nNSFW Content : {i.porn}\nPPC : {i.ppc}\nBudget : {i.budget}\nStatus : {i.status}\nVisits : {i.visits}\nRemaining Budget : {i.r_balance}"
                    bot.edit_message_text(a,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id),disable_web_page_preview=True)
                bot.answer_callback_query(call.id,text="⏸ Your Advertisment is Paused due to Insufficient Fund/Budget Reached.",show_alert=True)  
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=="needed":
        try:
            ad_id=call.message.text[19:29]
            z=session.query(Ads).filter(Ads.ad_id==ad_id).one()
            session.query(Ads).filter(Ads.ad_id==ad_id).update({Ads.username_needed:'Yes'})
            session.commit()
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=="not_needed":
        try:
            ad_id=call.message.text[19:29]
            z=session.query(Ads).filter(Ads.ad_id==ad_id).one()
            session.query(Ads).filter(Ads.ad_id==ad_id).update({Ads.username_needed:'No'})
            session.commit()
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
    
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='ad_edit':
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=edit_ad_markup())
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='ad_title':
            ad_id=call.message.text[19:29]
            sent=bot.send_message(call.message.chat.id,"Enter the new title for your ad:",reply_markup=cancel_new_ad_markup())
            bot.register_next_step_handler(sent,edit_title,ad_id)
        
    
    if call.data=='ad_desc':
        msg=call.message.text
        ad_id=call.message.text[19:29]
        sent=bot.send_message(call.message.chat.id,"Enter the new description for your ad:",reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,edit_desc,ad_id)

    if call.data=='ad_cpc':
        ad_id=call.message.text[19:29]
        sent=bot.send_message(call.message.chat.id,"Enter the new Pay per click Rate for your ad:",reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,edit_cpc,ad_id)

    if call.data=='ad_budget':
        ad_id=call.message.text[19:29]
        sent=bot.send_message(call.message.chat.id,"Enter the new Budget for your ad:",reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,edit_budget,ad_id)
    
    if call.data=='ad_back':
        ad_id=call.message.text[19:29]
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=manage_adver_markup(ad_id))
    

    if call.data=='bot_skip':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
        bot_handle(call.message)

    if call.data=='bot_done':
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            z=session.query(Ads).filter(Ads.title==call.message.text.split("\n")[0]).one()
            sent=bot.send_message(call.message.chat.id,f"forward a message from the bot to this chat.")
            bot.register_next_step_handler(sent,bot_done,z.link,z.ad_id)
        except Exception:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            bot.answer_callback_query(call.id,text="Aww :( , To many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='channel_skip':
        
        channel_handle(call.message)

    if call.data=='channel_done':
        try:
           
            z=session.query(Ads).filter(Ads.title==call.message.text.split("\n")[0]).one()
            username='@'+z.link
            
            a=bot.get_chat_member(chat_id='@'+username,user_id=call.message.chat.id)
            
            if a.status=='member' or a.status=='administrator':
                bot.edit_message_text("Success! 👍\nYou must stay in the channel for at least 1 hours to earn your reward.",call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
                channel_done(call.message,username,z.ad_id)
            else:
                bot.send_message(call.message.chat.id,"You're not in channel")
            channel_handle(call.message)
            
        except Exception:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='post_skip':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
        post_handle(call.message)

    if call.data=='post_done':
        try:
            
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            z=session.query(Ads).filter(Ads.ad_id==call.message.text[9:19]).one()
            print(z.link)
            username='@'+z.link

            bot.forward_message(call.message.chat.id,from_chat_id=f"{username}",message_id=z.post_message)
            post_done(call.message,z.link,z.ad_id)
        except Exception : 
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')


    if call.data=='site_skip':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
        site_handle(call.message)

    if call.data=='site_done':
        try:
            
            sent=bot.edit_message_text(f"🔄 Processing...",chat_id=call.message.chat.id,message_id=call.message.message_id)
            site_handle(call.message)
        except Exception:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            bot.send_message(call.message.chat.id,"Please Try again..!!")
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')


    if call.data=='yt_done':
        try:
            
            sent=bot.edit_message_text(f"🔄 Processing...",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            yt_handle(call.message)
        except Exception:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            bot.send_message(call.message.chat.id,"Please Try again..!!")
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='group_skip':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
        group_handle_unverified(call.message)
    
    if call.data=='group_done':
            z=session.query(Ads).filter(Ads.title==call.message.text.split("\n")[0]).one()
            username='@'+z.link
            a=bot.get_chat_member(chat_id=username,user_id=call.message.chat.id)
            if a.status=='member' or a.status=='administrator':
                if z.verify==True:
                    bot.edit_message_text(f"Please Send `{z.comment}` in group to verify.",call.message.chat.id,message_id=call.message.message_id,reply_markup=contact_admin_markup(z.link),parse_mode='markdown')
                    group_verification(call.message,username,z.ad_id,z.comment)
                else:
                    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
                    group_done(call.message,username,z.ad_id)
                    group_handle_unverified(call.message)
            else:
                bot.answer_callback_query(call.id,text="Aww :( , You're not in channel .Please try again.",show_alert=True)


    if call.data=='back':
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            bot.send_message(call.message.chat.id,"✅ You're in Menu",reply_markup=start_markup())
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='trx':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Tron* address: \n `{address.trx}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='bch':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Bitcon Cash* address:\n `{address.bch}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='btc':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Bitcon* address:\n `{address.btc}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='eth':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Ethereum* address:\n `{address.eth}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='xrp':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Ripple* address:\n `{address.xrp}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='doge':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Doge* address:\n `{address.doge}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='bnb':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Binance Coin* address:\n `{address.bnb}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='ltc':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Litecoin* address:\n `{address.ltc}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='dash':
        address=session.query(Wallet).filter(Wallet.chat_id==call.message.chat.id).one()
        data=f'Your Personal *Dash* address:\n `{address.dash}` \n\n🕝 Transaction will be credited after 3 network confirmations. '
        bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown')
    if call.data=='top_ref':
        a=session.query(User).order_by(User.refferal.desc()).limit(20).all()
        data=""
        j=1
        for i in a:
            data+=f'{j}. {i.first_name.replace("None","")}\t{i.last_name.replace("None","")}\n'
            j=j+1

        bot.send_message(call.message.chat.id,data)

    if call.data=='view_message':
        
        try:
            msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            if msg.content_type=='text':
                bot.send_message(call.message.chat.id,msg.text)
            if msg.content_type=='photo':
                photo = open(msg.file_name, 'rb')
                bot.send_photo(call.message.chat.id,photo,caption=msg.text)
            if msg.content_type=='gif':
                photo = open(msg.file_name, 'rb')
                bot.send_animation(call.message.chat.id,photo,caption=msg.text)
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='100':
        try:
                msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
            #if msg1.total_users <=user:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users+100,BulkMessage.price:(msg1.total_users+100)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='500':
        try:
                msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
            #if msg1.total_users <=user:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users+500,BulkMessage.price:(msg1.total_users+500)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='1000':
        try:
                msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
            #if msg1.total_users <=user:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users+1000,BulkMessage.price:(msg1.total_users+1000)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    
    if call.data=='3000':
        try:
                msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
            #if msg1.total_users <=user:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users+3000,BulkMessage.price:(msg1.total_users+3000)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='100minus':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            if msg1.total_users>100:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users-100,BulkMessage.price:(msg1.total_users-100)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='500minus':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            if msg1.total_users >600:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users-500,BulkMessage.price:(msg1.total_users-500)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='1000minus':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            if msg1.total_users >1100:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users-1000,BulkMessage.price:(msg1.total_users-1000)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='3000minus':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            if msg1.total_users >3100:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:msg1.total_users-3000,BulkMessage.price:(msg1.total_users-3000)*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='reset_order':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            if msg1.total_users >100:
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.total_users:100,BulkMessage.price:100*minimum.bulk_message_price})
                session.commit()
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                data=f"*Order ID*: {msg.order_id}\n*Content Type*: {msg.content_type}\n*Total Message*: {msg.total_users} \n*Price*: {msg.price} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,parse_mode='markdown',reply_markup=members_markup())
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='cancel_order':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,"🚫 Order Cancelled",reply_markup=bulk_message_markup())
            session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).delete()
            session.commit()
            silent_remove(msg1.file_name)
        except TypeError:
            pass
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    
    if call.data=='delete_message':
        try:
            msg1=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            bot.edit_message_text("🗑 Your order Deleted",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
            session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).delete()
            session.commit()
            silent_remove(msg1.file_name)
        except TypeError:
            pass
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    
    if call.data=='confirm_order':
        try:
            msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
            info=session.query(User).filter(User.chat_id==msg.chat_id).one()
            if msg.price <=info.balance:
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=view2_message_markup())
                bot.send_message(call.message.chat.id,"✅ Your Order Placed Sucessfully.\n\n➖ <i>Waiting for admin to Approve.</i>",parse_mode='HTML',reply_markup=bulk_message_markup())
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                data=f"Order ID: {msg.order_id}\nContent Type: {msg.content_type}\nTotal Message: {msg.total_users} \nPrice: {msg.price} TRX\nEstimated Users(Approx): {user}\nAdvertiser: @{call.message.chat.username}\n\n"
                bot.send_message('-1001443308711',data,reply_markup=approve_order_markup())
            else:
                bot.edit_message_text("❌ Your Order is Unsucessful\n\n",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
                bot.send_message(call.message.chat.id,'⛔️ Insufficient Funds.Please Deposit',reply_markup=advertise_markup())
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).delete()
                session.commit()
                silent_remove(msg.file_name)
        except TypeError:
            pass
        except Exception:
            bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='decline_order':
        try:
            if call.from_user.id in admin:
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                info=session.query(User).filter(User.chat_id==msg.chat_id).one()
                data=f"Order ID: {msg.order_id}\nContent Type: {msg.content_type}\nTotal Message: {msg.total_users} \nPrice: {msg.price} TRX\nEstimated Users(Approx): {user}\nAdvertiser: @{info.username}\nOrder Status : Declined By Admin"
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=view2_message_markup())
                bot.send_message(msg.chat_id,data+"\n\n🚫 You're Bulk Message Order is Declined by admin\n\n",reply_markup=view2_message_markup())
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.status:'Declined'})
                session.commit()
            else:
                bot.answer_callback_query(call.id,text="🧑🏼‍💻 Your're Not Admin",show_alert=True)
        except Exception:
                bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
                bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='approve_order':
        try:
            if call.from_user.id in admin:
                msg=session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).one()
                user=session.query(User).count()
                info=session.query(User).filter(User.chat_id==msg.chat_id).one()
                data=f"Order ID: {msg.order_id}\nContent Type: {msg.content_type}\nTotal Message: {msg.total_users} \nPrice: {msg.price} TRX\nEstimated Users(Approx): {user}\nAdvertiser: @{info.username}\nOrder Status : Approved "
                bot.edit_message_text(data,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=view2_message_markup())
                bot.send_message(msg.chat_id,data+"\n\n✅ You're Bulk Message Order is Approved by admin\n\n",reply_markup=view2_message_markup())
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.status:'Approved'})
                session.commit()
                top_users=session.query(User).limit(msg.total_users).all()
                u=[]
                for i in top_users:
                    if msg.content_type=='text':
                        try:
                            bot.send_message(i.chat_id,msg.text,reply_markup=dicalimer_markup())
                            u.append(i.chat_id)
                        except Exception:
                            pass
                    if msg.content_type=='photo':
                        photo = open(msg.file_name, 'rb')
                        try:
                            bot.send_photo(i.chat_id,photo,caption=msg.text,reply_markup=dicalimer_markup())
                            u.append(i.chat_id)
                        except Exception:
                            pass
                    if msg.content_type=='gif':
                        photo = open(msg.file_name, 'rb')
                        try:
                            bot.send_animation(i.chat_id,photo,caption=msg.text,reply_markup=dicalimer_markup())
                            u.append(i.chat_id)
                        except Exception:
                            pass
                sucess=len(u)
                session.query(BulkMessage).filter(BulkMessage.order_id==call.message.text[10:15]).update({BulkMessage.status:'Completed',BulkMessage.remaining:sucess,BulkMessage.price:minimum.bulk_message_price*sucess})
                session.commit()
                if info.balance<=info.earning:
                    session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:info.balance-minimum.bulk_message_price*sucess,User.earning:info.earning-minimum.bulk_message_price*sucess})
                    session.commit()
                else:
                    session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:info.balance-minimum.bulk_message_price*sucess})
                    session.commit()
                bot.send_message(msg.chat_id,f"✅ Your above order sucessfully completed..\n\nSucessful sent message : {sucess}\nTotal Price : {minimum.bulk_message_price*sucess}")    
                #data1=f"Order ID: {msg.order_id}\nContent Type: {msg.content_type}\nTotal Message: {msg.total_users}\nSucessful sent message : {sucess}\nPrice: {minimum.bulk_message_price*sucess} TRX\nEstimated Users(Approx): {user}\nAdvertiser: @{info.username}\nOrder Status : Completed"
                #bot.edit_message_text(data1,chat_id=,message_id=call.message.message_id,reply_markup=view2_message_markup())
            else:
                bot.answer_callback_query(call.id,text="🧑🏼‍💻 Your're Not Admin",show_alert=True)

        except Exception:
                bot.answer_callback_query(call.id,text="Aww :( , Too many Requests .Please try again later.",show_alert=True)
                bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
    if call.data=='approve_withdraw':
        if call.from_user.id in admin:
            text=call.message.text[3:7]
            print(text)
            try:    
                a=session.query(Withdraw).filter(Withdraw.message_id==text).one() 
                user=session.query(User).filter(User.chat_id==a.chat_id).one()
                if a.status=='Unconfirmed':
                    print(a.amt)
                    priv_key = PrivateKey.fromhex(api_key.tron_key)
                    txn = (
                        tron_client.trx.transfer(from_=api_key.tron_address,to=a.address,amount=int(str(int(a.amt))+'000000'))
                        .memo("From RapidClick BOT")
                        .build()
                        .inspect()
                        .sign(priv_key)
                        .broadcast()
                        
                        
                    )
                    data=f'💰Your Withdrawal of <b>{a.amt} TRX</b> is Successful.\n\nTransaction ID : <a href="https://tronscan.org/#/transaction/{txn.txid}">{txn.txid}</a>'
                    bot.send_message(a.chat_id,data,parse_mode="HTML",disable_web_page_preview=True)
                    data_channel=f"ID:{a.message_id}\nChat ID :{a.chat_id}\nUsername : @{user.username}\nAmount : {a.amt}\nAddress :{a.address}\nStatus : Approved "
                    bot.edit_message_text(data_channel,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=empty_markup())
                    data=f'➕ New Withdraw:\n <b>{a.chat_id}</b> just withdrawal <b>{a.amt} TRX</b>\n\nTransaction ID : <a href="https://tronscan.org/#/transaction/{txn.txid}">{txn.txid}</a>'
                    bot.send_message('@Rapidclick_Transactions',data,parse_mode='HTML',disable_web_page_preview=True)
                    session.query(User).filter(User.chat_id==a.chat_id).update({User.balance:User.balance-(a.amt),User.earning:User.earning-(a.amt)})
                    session.commit()
                    session.query(Withdraw).filter(Withdraw.message_id==text).update({Withdraw.txn:txn.txid,Withdraw.status:'Confirmed'})
                    session.commit()
                else:
                    bot.answer_callback_query(call.id,text="🧑🏼‍💻 Your're Not Admin",show_alert=True)
            except Exception:
                bot.answer_callback_query(call.id,text="Aww :( , Something went wrong.Please try again later.",show_alert=True)
                bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

    if call.data=='stats':
        users=session.query(User).filter(User.ban==False).count()
        ban=session.query(User).filter(User.ban==True).count()
        link=session.query(Ads).filter(Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='site').count()
        yt=session.query(Ads).filter(Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='youtube').count()
        post=session.query(Ads).filter(Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='post').count()
        channel=session.query(Ads).filter(Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='channel').count()
        bot_=session.query(Ads).filter(Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='bot').count()
        group=session.query(Ads).filter(Ads.status=='Enabled🔔',Ads.complete=='Yes',Ads.ad_type=='group').count()
        deposit=session.query(Transaction).filter(Transaction.status=='Confirmed').count()
        withdraw=session.query(Withdraw).filter(Withdraw.status=='Confirmed').count()
        total_deposit=session.query(Transaction).filter(Transaction.status=='Confirmed').all()
        total_withdraw=session.query(Withdraw).filter(Withdraw.status=='Confirmed').all()
        t=0
        total=0
        for i in total_deposit:
            total+=i.amt
        
        for j in total_withdraw:
            t+=j.amt

        data=f" 👥 Users Info :\n\n👤 Active Users : {users}\n❌ Deleted Users: 0\n🚫 Banned Users : {ban}\n\n🖥 Advertising Info:\n\n🌐 Link Promotion : {link}\n🤖 Bot Promotion : {bot_}\n📄 Post Promotion: {post}\n📣 Channel Promotion : {channel}\n👥 Group Promotion : {group}\n▶️ YouTube Promotion : {yt}\n\n💰Transactions Info :\n\n{deposit} Deposit : {total} TRX\n{withdraw} Withdraw : {t} TRX\n💰Transactions : @Rapidclick_Transactions" 
        bot.send_message(call.message.chat.id,data)


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def group_verification(message,username,ad_id,comment): 
    msg.append(message.chat.id)
    usernam.append(username.replace('@',''))
    ad_i.append(ad_id)
    comme.append(comment)
    


@bot.message_handler(func=lambda m:m.from_user.id in msg and m.chat.username in usernam and m.text in comme)
def verified(message):
    group_done(message.from_user,usernam[0],ad_i[0]) 
    msg.remove(message.from_user.id)
    usernam.remove(usernam[0])
    ad_i.remove(ad_i[0])
    comme.remove(comme[0])
    group_handle(message.from_user)


def group_done(message,username,ad):
    try:
        a=session.query(Ads).filter(Ads.ad_id==ad).one()
        if a.verify==True:
            l=bot.get_chat_member(chat_id='@'+username,user_id=message.id)
            if l.status=='member' or l.status=='administrator':
                a=session.query(Ads).filter(Ads.ad_id==ad).one()
                bot.send_message(message.id,f"You earned {a.ppc*0.6} TRX for Joining group @{username} \n\n Note : You must stay atleast 20 days ")
                c=session.query(User).filter(User.chat_id==message.id).one()
                session.query(User).filter(User.chat_id==message.id).update({User.balance:User.balance+a.ppc*0.6,User.earning:User.earning+a.ppc*0.6})
                session.commit()
                if c.refferal_hash==None:
                    pass
                else:
                    session.query(User).filter(User.user_hash==c.refferal_hash).update({User.balance:User.balance+(a.ppc*0.06),User.earning:User.earning+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.06)})
                #if c.paid_ref_hash=='None':
                #     pass
                #else:
                #    session.query(User).filter(User.user_hash==c.paid_ref_hash).update({User.User:User.User+(a.ppc*0.1),User.refferal_earn:User.refferal_earn+(a.ppc*0.1)})
                session.query(Ads).filter(Ads.ad_id==ad).update({Ads.r_balance:Ads.r_balance-a.ppc,Ads.visits:Ads.visits+1})
                session.commit()
                msg=session.query(User).filter(User.chat_id==a.chat_id).one()
                if msg.balance<=msg.earning:
                    session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc,User.earning:msg.earning-a.ppc})
                    session.commit()
                else:
                    session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc})
                    session.commit()

                session.add(CheckUser(chat_id=message.id,date=date.today(),ad_id=ad,username='@'+username,ppc=a.ppc*0.6))
                session.commit()
                session.add(Task(chat_id=message.id,ad_id=a.ad_id))
                x=session.query(User).filter(User.chat_id==a.chat_id).one()
                f=session.query(Ads).filter(Ads.ad_id==ad).one()
                if f.r_balance<f.ppc or f.r_balance>x.balance:
                    session.query(Ads).filter(Ads.ad_id==ad).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
                    session.commit()
                else: 
                    pass
            else:
                    bot.send_message(message.id,"Task Incomplete\n\nYou leave the group "+username)
        else:
            l=bot.get_chat_member(chat_id='@'+username,user_id=message.chat.id)
            if l.status=='member' or l.status=='administrator':
                a=session.query(Ads).filter(Ads.ad_id==ad).one()
                bot.send_message(message.chat.id,f"You earned {a.ppc*0.6} TRX for Joining group @{username} \n\n Note : You must stay atleast 20 days ")
                c=session.query(User).filter(User.chat_id==message.chat.id).one()
                session.query(User).filter(User.chat_id==message.chat.id).update({User.balance:User.balance+a.ppc*0.6,User.earning:User.earning+a.ppc*0.6})
                session.commit()
                if c.refferal_hash==None:
                    pass
                else:
                    session.query(User).filter(User.user_hash==c.refferal_hash).update({User.balance:User.balance+(a.ppc*0.06),User.earning:User.earning+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.06)})
                #if c.paid_ref_hash=='None':
                #     pass
                #else:
                #    session.query(User).filter(User.user_hash==c.paid_ref_hash).update({User.User:User.User+(a.ppc*0.1),User.refferal_earn:User.refferal_earn+(a.ppc*0.1)})
                session.query(Ads).filter(Ads.ad_id==ad).update({Ads.r_balance:Ads.r_balance-a.ppc,Ads.visits:Ads.visits+1})
                session.commit()
                msg=session.query(User).filter(User.chat_id==a.chat_id).one()
                if msg.balance<=msg.earning:
                    session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc,User.earning:msg.earning-a.ppc})
                    session.commit()
                else:
                    session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc})
                    session.commit()
                session.add(CheckUser(chat_id=message.chat.id,date=datetime.now(),ad_id=ad,username='@'+username,ppc=a.ppc*0.6))
                session.commit()
                session.add(Task(chat_id=message.chat.id,ad_id=a.ad_id))
                x=session.query(User).filter(User.chat_id==a.chat_id).one()
                f=session.query(Ads).filter(Ads.ad_id==ad).one()
                if f.r_balance<f.ppc or f.r_balance>x.balance:
                    session.query(Ads).filter(Ads.ad_id==ad).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
                    session.commit()
                else: 
                    pass
            else:
                    bot.send_message(message.chat.id,"Task Incomplete\n\nYou leave the group "+username)

    except Exception:
        bot.send_message(message.id,"Aww :( , Something went worng.Please try again later.",reply_markup=start_markup())
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')



def post_done(message,username,ad): 
    try:
        time.sleep(10)
        a=session.query(Ads).filter(Ads.ad_id==ad).one()
        bot.send_message(message.chat.id,f"You earned {a.ppc*0.6} TRX for Reading post")
        c=session.query(User).filter(User.chat_id==message.chat.id).one()
        session.query(User).filter(User.chat_id==message.chat.id).update({User.balance:User.balance+a.ppc*0.6,User.earning:User.earning+a.ppc*0.6})
        session.commit()
        if c.refferal_hash==None:
            pass
        else:
            session.query(User).filter(User.user_hash==c.refferal_hash).update({User.balance:User.balance+(a.ppc*0.06),User.earning:User.earning+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.06)})
        #if c.paid_ref_hash=='None':
          #  pass
        #else:
            #session.query(User).filter(User.user_hash==c.paid_ref_hash).update({User.User:User.User+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.1)})
        session.query(Ads).filter(Ads.ad_id==ad).update({Ads.r_balance:Ads.r_balance-a.ppc,Ads.visits:Ads.visits+1})
        session.commit()
        msg=session.query(User).filter(User.chat_id==a.chat_id).one()
        if msg.balance<=msg.earning:
            session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc,User.earning:msg.earning-a.ppc})
            session.commit()
        else:
            session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc})
            session.commit()
        session.add(Task(chat_id=message.chat.id,ad_id=a.ad_id))
        x=session.query(User).filter(User.chat_id==a.chat_id).one()
        f=session.query(Ads).filter(Ads.ad_id==ad).one()
        if f.r_balance<f.ppc or f.r_balance>x.balance:
            session.query(Ads).filter(Ads.ad_id==ad).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
            session.commit()
        else: 
            pass
        post_handle(message)
    except Exception:
        bot.send_message(message.chat.id,"Aww :( , Something went worng.Please try again later.",reply_markup=start_markup())
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')






        
def channel_done(message,username,ad): 
    try:
        l=bot.get_chat_member(chat_id='@'+username,user_id=message.chat.id)
        if l.status=='member' or l.status=='administrator':
            a=session.query(Ads).filter(Ads.ad_id==ad).one()
            bot.send_message(message.chat.id,f"You earned {a.ppc*0.6} TRX for Joining Channel {username}")
            c=session.query(User).filter(User.chat_id==message.chat.id).one()
            session.query(User).filter(User.chat_id==message.chat.id).update({User.balance:User.balance+a.ppc*0.6,User.earning:User.earning+a.ppc*0.6})
            session.commit()
            if c.refferal_hash==None:
                pass
            else:
                session.query(User).filter(User.user_hash==c.refferal_hash).update({User.balance:User.balance+(a.ppc*0.06),User.earning:User.earning+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.06)})
            #if c.paid_ref_hash=='None':
            #     pass
            #else:
            #    session.query(User).filter(User.user_hash==c.paid_ref_hash).update({User.User:User.User+(a.ppc*0.1),User.refferal_earn:User.refferal_earn+(a.ppc*0.1)})
            session.query(Ads).filter(Ads.ad_id==ad).update({Ads.r_balance:Ads.r_balance-a.ppc,Ads.visits:Ads.visits+1})
            session.commit()
            msg=session.query(User).filter(User.chat_id==a.chat_id).one()
            if msg.balance<=msg.earning:
                session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc,User.earning:msg.earning-a.ppc})
                session.commit()
            else:
                session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc})
                session.commit()
            session.add(CheckUser(chat_id=message.chat.id,date=datetime.now(),ad_id=ad,username='@'+username,ppc=a.ppc*0.6))
            session.commit()
            session.add(Task(chat_id=message.chat.id,ad_id=a.ad_id))
            x=session.query(User).filter(User.chat_id==a.chat_id).one()
            f=session.query(Ads).filter(Ads.ad_id==ad).one()
            if f.r_balance<f.ppc or f.r_balance>x.balance:
                session.query(Ads).filter(Ads.ad_id==ad).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
                session.commit()
            else: 
                pass
        else:
                bot.send_message(message.chat.id,"Task Incomplete\n\nYou leave the  channel "+username)
    except Exception:
        bot.send_message(message.chat.id,"Aww :( , Something went worng.Please try again later.",reply_markup=start_markup())
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

def bot_done(message,username,ad):
    try:
        regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if bool(regex.search(username))==True:
                result=re.search('https://t.me/(.*)?start=',username)
                user=result.group(1).replace('?','')
                if message.forward_from.username==user and message.forward_from.is_bot==True:
                    today =datetime.today()
                    yesterday = today -timedelta(days=1)
                    unixtime = time.mktime(yesterday.timetuple())
                    if message.forward_date>=unixtime:
                        a=session.query(Ads).filter(Ads.ad_id==ad).one()
                        bot.send_message(message.chat.id,f"You earned {a.ppc*0.6} TRX for messaging a bot!")
                        c=session.query(User).filter(User.chat_id==message.chat.id).one()
                        session.query(User).filter(User.chat_id==message.chat.id).update({User.balance:User.balance+a.ppc*0.6,User.earning:User.earning+a.ppc*0.6})
                        session.commit()
                        if c.refferal_hash=="":
                            pass
                        else:
                            session.query(User).filter(User.user_hash==c.refferal_hash).update({User.balance:User.balance+(a.ppc*0.06),User.earning:User.earning+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.06)})
                        #if c.paid_ref_hash=='None':
                        #    pass
                        #else:
                        #    session.query(User).filter(User.user_hash==c.paid_ref_hash).update({User.User:User.User+(a.ppc*0.1),User.refferal_earn:User.refferal_earn+(a.ppc*0.1)})
                        session.query(Ads).filter(Ads.ad_id==ad).update({Ads.r_balance:Ads.r_balance-a.ppc,Ads.visits:Ads.visits+1})
                        session.commit()
                        msg=session.query(User).filter(User.chat_id==a.chat_id).one()
                        if msg.balance<=msg.earning:
                            session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc,User.earning:msg.earning-a.ppc})
                            session.commit()
                        else:
                            session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc})
                            session.commit()
                        session.add(Task(chat_id=message.chat.id,ad_id=a.ad_id))
                        x=session.query(User).filter(User.chat_id==a.chat_id).one()
                        f=session.query(Ads).filter(Ads.ad_id==ad).one()
                        if f.r_balance<f.ppc or f.r_balance>x.User:
                            session.query(Ads).filter(Ads.ad_id==ad).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
                            session.commit()
                        else: 
                            pass
        

                        bot_handle(message)
                    else:
                        sent=bot.send_message(message.chat.id,"The message you forwarded is too old. 🕰\n\nPlease send a newer message from bot.")
                        bot.register_next_step_handler(sent,bot_done,username,ad)
                else:
                    bot.send_message(message.chat.id,"Username Not Found")
        else:
            if message.forward_from.username==username and message.forward_from.is_bot==True:
                    today =datetime.today()
                    yesterday = today -timedelta(days=1)
                    unixtime = time.mktime(yesterday.timetuple())
                    if message.forward_date>=unixtime:
                        a=session.query(Ads).filter(Ads.ad_id==ad).one()
                        bot.send_message(message.chat.id,f"You earned {a.ppc*0.6} TRX for messaging a bot!")
                        c=session.query(User).filter(User.chat_id==message.chat.id).one()
                        session.query(User).filter(User.chat_id==message.chat.id).update({User.balance:User.balance+a.ppc*0.6})
                        session.commit()
                        if c.refferal_hash=="":
                            pass
                        else:
                            session.query(User).filter(User.user_hash==c.refferal_hash).update({User.balance:User.balance+(a.ppc*0.06),User.earning:User.earning+(a.ppc*0.06),User.refferal_earn:User.refferal_earn+(a.ppc*0.06)})
                       # if c.paid_ref_hash=='None':
                          #  pass
                        #else:
                           # session.query(User).filter(User.user_hash==c.paid_ref_hash).update({User.User:User.User+(a.ppc*0.1),User.refferal_earn:User.refferal_earn+(a.ppc*0.1)})
                        session.query(Ads).filter(Ads.ad_id==ad).update({Ads.r_balance:Ads.r_balance-a.ppc,Ads.visits:Ads.visits+1})
                        session.commit()
                        msg=session.query(User).filter(User.chat_id==a.chat_id).one()
                        if msg.balance<=msg.earning:
                            session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc,User.earning:msg.earning-a.ppc})
                            session.commit()
                        else:
                            session.query(User).filter(User.chat_id==msg.chat_id).update({User.balance:msg.balance-a.ppc})
                            session.commit()
                        session.add(Task(chat_id=message.chat.id,ad_id=a.ad_id))
                        x=session.query(User).filter(User.chat_id==a.chat_id).one()
                        f=session.query(Ads).filter(Ads.ad_id==ad).one()
                        if f.r_balance<f.ppc or f.r_balance>x.User:
                            session.query(Ads).filter(Ads.ad_id==ad).update({Ads.status:'⏸ Paused : Insufficient Fund/Budget Reached '})
                            session.commit()
                        else: 
                            pass
        

                        bot_handle(message)
                    else:
                        sent=bot.send_message(message.chat.id,"The message you forwarded is too old. 🕰\n\nPlease send a newer message from bot.")
                        bot.register_next_step_handler(sent,bot_done,username,ad)
            else:
                    bot.send_message(message.chat.id,"Username Not Found")
    except Exception:
        bot.send_message(message.chat.id,"Username Not Found",reply_markup=start_markup())
        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')



def edit_title(message,ad_id):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your operation canceled.",reply_markup=advertise_markup())
    else:
        session.query(Ads).filter(Ads.ad_id==ad_id).update({Ads.title:message.text})
        session.commit()
        bot.send_message(message.chat.id,"✅ Your Advertisment title has been updated",reply_markup=advertise_markup())

    
    

def edit_desc(message,ad_id):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your operation canceled.",reply_markup=advertise_markup())
    else:
        session.query(Ads).filter(Ads.ad_id==ad_id).update({Ads.desc:message.text})
        session.commit()
        bot.send_message(message.chat.id,"✅ Your Advertisment description has been updated",reply_markup=advertise_markup())

def edit_cpc(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your operation canceled.",reply_markup=advertise_markup())
    else:
        z=session.query(Ads).filter(Ads.ad_id==res).one()
        try:
            adg=float(message.text)
            if z.ad_type=='site':
                if adg>=minimum.min_cpc_site and adg<=1:
                        session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
                        session.commit()
                        bot.send_message(message.chat.id,"✅ Your Advertisment PPC has been updated",reply_markup=advertise_markup())
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_site}* and *1 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_cpc,res)
            if z.ad_type =='bot':
                if adg>=minimum.min_cpc_bot and adg<=1:
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
                    session.commit()
                    bot.send_message(message.chat.id,"✅ Your Advertisment PPC has been updated",reply_markup=advertise_markup())
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_bot}* and *1 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_cpc,res)
            if z.ad_type=='channel':
                if adg>=minimum.min_cpc_channel and adg<=1:
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
                    session.commit()
                    bot.send_message(message.chat.id,"✅ Your Advertisment PPC has been updated",reply_markup=advertise_markup())
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_channel}* and *1 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_cpc,res)
            if z.ad_type=='post':
                if adg>=minimum.min_cpc_post and adg<=1:
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
                    session.commit()
                    bot.send_message(message.chat.id,"✅ Your Advertisment PPC has been updated",reply_markup=advertise_markup())
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_post}* and *1 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_cpc,res)

            if z.ad_type=='group':
                if adg>=minimum.min_cpc_group and adg<=1:
                    session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
                    session.commit()
                    bot.send_message(message.chat.id,"✅ Your Advertisment PPC has been updated",reply_markup=advertise_markup())
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_group}* and *1 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_cpc,res)

            if z.ad_type=='youtube':
                if adg>=minimum.min_cpc_yt and adg<=1:
                        session.query(Ads).filter(Ads.ad_id==res).update({Ads.ppc:adg})
                        session.commit()
                        bot.send_message(message.chat.id,"✅ Your Advertisment PPC has been updated",reply_markup=advertise_markup())
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_cpc_yt}* and *1 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_cpc,res)
        except Exception: 
            sent=bot.send_message(message.chat.id,"Invalid TRX",parse_mode='markdown',reply_markup=advertise_markup())
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')




def edit_budget(message,res):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your operation canceled.",reply_markup=advertise_markup())
    
    else:
        z=session.query(Ads).filter(Ads.ad_id==res).one()
        try:
            msd=float(message.text)
            if z.ad_type=='site':
                if msd>=minimum.min_budget_site:
                    edit_budget_done(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_site}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_budget,res)
            if z.ad_type=='bot':
                if msd>=minimum.min_budget_bot:
                    edit_budget_done(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_bot}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_budget,res)
            if z.ad_type=='channel':
                if msd>=minimum.min_budget_channel:
                    edit_budget_done(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_channel}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_budget,res)
            if z.ad_type=='post':
                if msd>=minimum.min_budget_post:
                    edit_budget_done(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_post}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_budget,res)
            if z.ad_type=='group':
                if msd>=minimum.min_budget_group:
                    edit_budget_done(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_group}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_budget,res)
            if z.ad_type=='youtube':
                if msd>=minimum.min_budget_yt:
                    edit_budget_done(message,res,msd)
                else:
                    sent=bot.send_message(message.chat.id,f"You must enter a value between *{minimum.min_budget_yt}* and *50 TRX*",parse_mode='markdown',reply_markup=cancel_new_ad_markup())
                    bot.register_next_step_handler(sent,edit_budget,res)
        except Exception:
            sent=bot.send_message(message.chat.id,"Invalid TRX",parse_mode='markdown',reply_markup=advertise_markup())
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
        
def edit_budget_done(message,res,msd):
    a=session.query(User).filter(User.chat_id==message.chat.id).one()
    if msd <= a.balance:
        session.query(Ads).filter(Ads.ad_id==res).update({Ads.budget:msd,Ads.r_balance:(Ads.budget-Ads.r_balance)+msd})
        session.commit()
        bot.send_message(message.chat.id,"✅ Your Advertisment Budget has been updated",reply_markup=advertise_markup())
       

@bot.message_handler(regexp='📨 Bulk Message Service')
def bulk_message_handler(message):
    message_list=session.query(BulkMessage).filter(BulkMessage.chat_id==message.chat.id).all()
    users=session.query(User).count()
    message_count=session.query(BulkMessage).filter(BulkMessage.chat_id==message.chat.id).count()
    bot.send_message(message.chat.id,f"You have {message_count} orders",reply_markup=bulk_message_markup())
    for i in message_list:
        data=f"Order ID: {i.order_id}\nContent Type :{i.content_type}\nTotal Message :{i.total_users}\nTotal Sent Message: {i.remaining}\nOrder status :{i.status}\nTotal price: {i.price}\nUsers available (estimated): {users}"
        bot.send_message(message.chat.id,data,reply_markup=view_message_markup())
        

@bot.message_handler(regexp='⛔️ Cancel')
def cancel_ad__handler(message):
    bot.send_message(message.chat.id,"✅ You are in Advertisement.",reply_markup=advertise_markup())

@bot.message_handler(regexp='➕ Add Orders')
def add_orders(message):
    bal=session.query(User).filter(User.chat_id==message.chat.id).one()
    if bal.ban==False:
        res = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+
                                        string.digits, k = 5)) 
        sent=bot.send_message(message.chat.id,"❇️ Enter Advertisement Message to be sent.",reply_markup=cancel_new_ad_markup())
        session.add(BulkMessage(chat_id=message.chat.id,order_id=res))
        session.commit()
        
        bot.register_next_step_handler(sent,get_msg,res)

def get_msg(message,db):
    if message.text=='❌ Cancel':
        bot.send_message(message.chat.id,"🚫 Your order has been canceled.",reply_markup=advertise_markup())
        session.query(BulkMessage).filter(BulkMessage.order_id==db).delete()
        session.commit()
    else:
        user=session.query(User).count()
        if message.content_type=='text':
            session.query(BulkMessage).filter(BulkMessage.order_id==db).update({BulkMessage.content_type:'text',BulkMessage.text:message.text,BulkMessage.price:minimum.bulk_message_price*100,BulkMessage.total_users:100})
            session.commit()
            bot.send_message(message.chat.id,"🔞 *Pornographic/NSFW content strictly not allowed*",reply_markup=empty_key_markup(),parse_mode='markdown')
            data=f"*Order ID*: {db}\n*Content Type*: {message.content_type}\n*Total Message*: 100 \n*Price*: {minimum.bulk_message_price*100} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
            bot.send_message(message.chat.id,data,reply_markup=members_markup(),parse_mode='markdown')
        if message.content_type=='photo':
            path='bulk_message_file/'
            file = bot.get_file(message.photo[0].file_id)
            file1=bot.download_file(file.file_path)
            file_name=file.file_path.split("/")[-1]
            with open(path+file_name,"wb") as f:
                f.write(file1)
            FILES = ((file_name, False),(file_name, True),)   
            session.query(BulkMessage).filter(BulkMessage.order_id==db).update({BulkMessage.content_type:'photo',BulkMessage.text:message.caption,BulkMessage.file_name:path+file_name,BulkMessage.total_users:100})  
            session.commit()
            data=f"*Order ID*: {db}\n*Content Type*: {message.content_type}\n*Total Message*: 100 \n*Price*: {minimum.bulk_message_price*100} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
            bot.send_message(message.chat.id,data,reply_markup=members_markup(),parse_mode='markdown')
        if message.content_type=='document':
            path='bulk_message_file/'
            file = bot.get_file(message.animation.file_id)
            file1=bot.download_file(file.file_path)
            file_name=file.file_path.split("/")[-1]
            with open(path+file_name,"wb") as f:
                f.write(file1)
            FILES = ((file_name, False),(file_name, True),)   
            session.query(BulkMessage).filter(BulkMessage.order_id==db).update({BulkMessage.content_type:'gif',BulkMessage.text:message.caption,BulkMessage.file_name:path+file_name,BulkMessage.total_users:100})  
            session.commit()
            data=f"*Order ID*: {db}\n*Content Type*: {message.content_type}\n*Total Message*: 100 \n*Price*: {minimum.bulk_message_price*100} TRX\n*Estimated Users(Approx)*: {user}\n\nSelect the Below option to Increase No. of message.\n\nClick ✅ *Confirm* to confirm the order"
            bot.send_message(message.chat.id,data,reply_markup=members_markup(),parse_mode='markdown')
    

@bot.message_handler(commands=['admin_start'])
def admin_handler(message):
    if message.chat.id in admin:
        bot.send_message(message.chat.id,"✅ You logged in as Admin",reply_markup=admin_markup())
    else :
            bot.send_message(message.chat.id,'*This access only for admin*',parse_mode='markdown')

@bot.message_handler(regexp='📥 Mailing')
def mail_handler(message):
    if message.chat.id in admin:
        sent=bot.send_message(message.chat.id,'Enter the Message',reply_markup=cancel_new_ad_markup())
        bot.register_next_step_handler(sent,mail)
    

def mail(message):
    chat_id = message.chat.id
    if chat_id in admin:
        if message.text=='❌ Cancel':
            bot.send_message(message.chat.id,"🚫 canceled.",reply_markup=admin_markup())
        else:
            for user in session.query(User):
                try:
                    bot.send_message(user.chat_id,message.text)
                except Exception:
                    pass
            bot.send_message(message.chat.id,'☑️Mailing finished!',reply_markup=admin_markup())

    else :
            bot.send_message(message.chat.id,'*This access only for admin*',parse_mode='markdown')

def dicalimer_markup():
    markup=InlineKeyboardMarkup(row_width=6)
    h=InlineKeyboardButton('⚠️ Disclaimer',url='https://telegra.ph/MESSEAGE-DISCLAIMER---Rapidclickbot-09-28')
    markup.add(h)
    return markup


def members_markup():
    markup=InlineKeyboardMarkup(row_width=6)
    h=InlineKeyboardButton('+100',callback_data='100')
    url=InlineKeyboardButton('+500',callback_data='500')
    thousand=InlineKeyboardButton('+1000',callback_data='1000')
    three=InlineKeyboardButton('+3000',callback_data='3000')
    h_=InlineKeyboardButton('-100',callback_data='100minus')
    url_=InlineKeyboardButton('-500',callback_data='500minus')
    thousand_=InlineKeyboardButton('-1000',callback_data='1000minus')
    three_=InlineKeyboardButton('-3000',callback_data='3000minus')
    confirm=InlineKeyboardButton('✅ Confirm',callback_data='confirm_order')
    cancel=InlineKeyboardButton('🚫 Cancel',callback_data='cancel_order')
    reset=InlineKeyboardButton('🔄 Reset',callback_data='reset_order')
    markup.add(h,url,thousand,three)
    markup.add(reset)
    markup.add(h_,url_,thousand_,three_)
    markup.add(confirm,cancel)
    return markup


def view_message_markup():
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('✉️ View Message',callback_data='view_message')
    ul=InlineKeyboardButton('🗑 Delete Order',callback_data='delete_message')
    markup.add(url,ul)
    return markup

def view2_message_markup():
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('✉️ View Message',callback_data='view_message')
    markup.add(url)
    return markup

def approve_order_markup():
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('✉️ View Message',callback_data='view_message')
    ul=InlineKeyboardButton('✅ Approve',callback_data='approve_order')
    u=InlineKeyboardButton('🚫 Decline',callback_data='decline_order')
    markup.add(url)
    markup.add(ul,u)
    return markup

def bulk_message_markup():
    markup=ReplyKeyboardMarkup(row_width=7,resize_keyboard=True)
    visit_sites=KeyboardButton('➕ Add Orders')
    cancel=KeyboardButton('⛔️ Cancel')
    markup.row(visit_sites)
    markup.row(cancel)
    return markup

def start_markup():
    markup=ReplyKeyboardMarkup(row_width=7,resize_keyboard=True)
    visit_sites=InlineKeyboardButton('🌐')
    message_bot=KeyboardButton('🤖')
    joinchat=KeyboardButton('📣')
    view_post=KeyboardButton('📄')
    join_group=KeyboardButton('👥')
    yt=KeyboardButton("▶️")
    bala=KeyboardButton('💰 Balance')
    refferals=KeyboardButton('👫 Referral System')
    settings=KeyboardButton('⚙️ Settings')
    ad=KeyboardButton('🖥    My Promotions    🖥')
    info=KeyboardButton("ℹ️ Info")
    markup.row(joinchat,visit_sites,yt,message_bot,join_group,view_post)
    markup.row(bala)
    markup.row(refferals,info,settings)
    markup.row(ad)
    #markup.row(ssm)

    return markup

def advertise_markup():
    markup=ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
    add=KeyboardButton('➕ Add New Advertisement')
    bulk_message=KeyboardButton('📨 Bulk Message Service')
    back=KeyboardButton('🔙 Go to Menu')
    markup.row(add,bulk_message)
    markup.row(back)
    return markup

def new_ad_markup():
    markup=ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
    url=KeyboardButton('💻 Website/URL')
    bots=KeyboardButton('📲 Bot')
    channel=KeyboardButton('📢 Channel')
    post=KeyboardButton('👁 Post')
    group=KeyboardButton('👥 Group')
    yt=KeyboardButton('▶️ Youtube')
    
    back=KeyboardButton('❌ Cancel')
    markup.row(url,bots,yt)
    markup.row(channel,post,group)
    
    markup.row(back)
    return markup

def cancel_new_ad_markup():
    markup=ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
    url=KeyboardButton('❌ Cancel')
    markup.add(url)
    return markup
    
def nsfw_ad_markup():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    yes=KeyboardButton('✅ Yes')
    no=KeyboardButton("🚫 No")
    cancel=KeyboardButton('❌ Cancel')
    markup.row(yes,no)
    markup.row(cancel)
    return markup

def verify_ad_markup():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    yes=KeyboardButton('🔺 Yes')
    no=KeyboardButton("🔻 No")
    cancel=KeyboardButton('❌ Cancel')
    markup.row(yes,no)
    markup.row(cancel)
    return markup



def refferal_markup(message):
    markup=InlineKeyboardMarkup()
    user=session.query(User).filter(message.chat.id==User.chat_id).one()
    q=f'is No. 1 TRX coin earning bot in Telegram\nYou will get paid by Performing Easy task\n\nRefferal Link :https://t.me/Rapidclickbot?start={user.user_hash}'
    buy=InlineKeyboardButton('💳 Refer Now',switch_inline_query=q)
    contest=InlineKeyboardButton('👫 Top Referrals',callback_data='top_ref')
    markup.add(buy)
    markup.add(contest)
    return markup

def balance_markup():
    markup=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    deposit=KeyboardButton('➕ Deposit')
    withdraw=KeyboardButton('➖ Withdraw')
    back=KeyboardButton('🔙 Go to Menu')
    history=KeyboardButton('🕧 Transaction Histoy')
    email=KeyboardButton('📧 Update Email')
    markup.row(email)
    markup.row(deposit,withdraw)
    markup.row(history)
    markup.row(back)
    return markup

def transaction_link_markup(message):
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('➖ Deposit Now',url=message)
    cancel_trans=InlineKeyboardButton('🚫 Cancel Transction' , callback_data='cancel_transc')
    markup.add(url)
    markup.add(cancel_trans)
    return markup 

def deposit_approve_markup():
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('✅ Approve',callback_data='approve_withdraw')
    markup.add(url)
    return markup


def admin_markup():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    update_User=KeyboardButton("📥 Mailing")
    
    markup.row(update_User)
    return markup


def transaction_history_markup():
    markup=InlineKeyboardMarkup()
    deposit=InlineKeyboardButton('🏤 Deposit History',callback_data='deposit_history')
    withdraw=InlineKeyboardButton('🏛 Withdraw History',callback_data='withdraw_history')
    markup.add(deposit)
    markup.add(withdraw)
    return markup


def setting_markup():
    markup=InlineKeyboardMarkup()
    porn=InlineKeyboardButton('🔞 Allow NSFW?',callback_data='porn')
    task=InlineKeyboardButton('🚨 Task Alert',callback_data='task')
    markup.add(porn)
    markup.add(task)
    return markup

def nsfw_markup(message):
    a=session.query(Alert).filter(Alert.chat_id==message).one()
    markup=InlineKeyboardMarkup()
    if a.nsfw=='Enabled🔔':
        button=InlineKeyboardButton('❌ Trun Off NSFW Notification',callback_data='nsfw_button_off')
    else:
        button=InlineKeyboardButton('✅ Trun On NSFW Notification',callback_data='nsfw_button_on')
    back=InlineKeyboardButton('🔙 Back',callback_data='set_back')
    markup.add(button)
    markup.add(back)
    return markup

def task_markup(message):
    a=session.query(Alert).filter(Alert.chat_id==message).one()
    markup=InlineKeyboardMarkup()
    if a.sites=='Enabled🔔':
        sites_button=InlineKeyboardButton('❌ Trun Off Visiting Sites Task',callback_data='sites_button_off')
    else :
        sites_button=InlineKeyboardButton('✅ Trun On Visiting Sites Task',callback_data='sites_button_on')
        
    if a.bots=='Enabled🔔':
        bots_button=InlineKeyboardButton('❌ Trun Off Message Bot Task',callback_data='bots_button_off')
    else :
        bots_button=InlineKeyboardButton('✅ Trun On Message Bot Task',callback_data='bots_button_on')

    if a.channel=='Enabled🔔':
        channels_button=InlineKeyboardButton('❌ Trun Off Message Channel Task',callback_data='channel_button_off')
    else :
        channels_button=InlineKeyboardButton('✅ Trun On Message Channel Task',callback_data='channel_button_on')

    if a.post=='Enabled🔔':
        post_button=InlineKeyboardButton('❌ Trun Off Message Post Task',callback_data='post_button_off')
    else :
        post_button=InlineKeyboardButton('✅ Trun On Message Post Task',callback_data='post_button_on')
    
    back=InlineKeyboardButton('🔙 Back',callback_data='set_back')
    markup.add(sites_button)
    markup.add(bots_button) 
    markup.add(channels_button)
    markup.add(post_button)
    markup.add(back)

    return markup
    

def manage_ad_markup(message):
        i=session.query(Ads).filter(Ads.ad_id==message).one()
        markup=InlineKeyboardMarkup()
    
        if i.status=='Enabled🔔':
            button=InlineKeyboardButton('🔕 Disable',callback_data='ad_dis')
            if i.username_needed=='Yes':
                username_button=InlineKeyboardButton('✅ Username Needed',callback_data='not_needed')
            elif i.username_needed=='No':
                username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')
            else :
                username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')

        elif i.status=='Disabled🔕':
            button=InlineKeyboardButton('🔔 Enable',callback_data='ad_en')
            if i.username_needed=='Yes':
                username_button=InlineKeyboardButton('✅ Username Needed',callback_data='not_needed')
            elif i.username_needed=='No':
                username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')
            else :
                username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')
        else:
            button=InlineKeyboardButton('🔕 Disable',callback_data='ad_dis')
            if i.username_needed=='Yes':
                username_button=InlineKeyboardButton('✅ Username Needed',callback_data='not_needed')
            elif i.username_needed=='No':
                username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')
            else :
                username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')
            
        
        edit=InlineKeyboardButton('📝 Edit',callback_data='ad_edit')
        delete=InlineKeyboardButton('🗑 Delete',callback_data='ad_delete')
        markup.add(edit,button)
        markup.add(delete)
        markup.add(username_button)
        return markup

def manage_adver_markup(message):
    i=session.query(Ads).filter(Ads.ad_id==message).one()
    markup=InlineKeyboardMarkup()
    if i.status=='Enabled🔔':
        button=InlineKeyboardButton('🔕 Disable',callback_data='ad_dis')
    elif i.status=='Disabled🔕' or i.status=='⏸ Paused : Insufficient Fund/Budget Reached ':
        button=InlineKeyboardButton('🔔 Enable',callback_data='ad_en')
    #else:
        #button=InlineKeyboardButton('🔕 Disable',callback_data='ad_dis')
    if i.username_needed=='Yes':
            username_button=InlineKeyboardButton('✅ Username Needed',callback_data='not_needed')
    else:
            username_button=InlineKeyboardButton('❌ Username Needed',callback_data='needed')
    edit=InlineKeyboardButton('📝 Edit',callback_data='ad_edit')
    delete=InlineKeyboardButton('🗑 Delete',callback_data='ad_delete')
    markup.add(edit,button)
    markup.add(delete)
    markup.add(username_button)
    return markup

def edit_ad_markup():
    markup=InlineKeyboardMarkup()
    title=InlineKeyboardButton('☑️ Edit Title',callback_data='ad_title')
    desc=InlineKeyboardButton('❗️ Edit Description',callback_data='ad_desc')
    cpc=InlineKeyboardButton('💲 Edit PPC',callback_data='ad_cpc')
    bud=InlineKeyboardButton('💰 Edit Budget',callback_data='ad_budget')
    back=InlineKeyboardButton('🔙 Back',callback_data='ad_back')
    markup.add(title,desc)
    markup.add(bud,cpc)
    markup.add(back)
    return markup

def bot_task_markup(bot):
    markup=InlineKeyboardMarkup()
    regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if bool(regex.search(bot))==True:
        url=InlineKeyboardButton('✉️ Message Bot',url=bot)
    else:
        url=InlineKeyboardButton('✉️ Message Bot',url='https://t.me/'+bot)
    report=InlineKeyboardButton('✅ Done',callback_data='bot_done')
    skip=InlineKeyboardButton('⚠️ Skip',callback_data='bot_skip')
    markup.add(url)
    markup.add(skip,report)
    
    return markup


def channel_task_markup(bot):
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('🔈 Join Channel',url='https://t.me/'+bot)
    report=InlineKeyboardButton('✅ Joined',callback_data='channel_done')
    skip=InlineKeyboardButton('⚠️ Skip',callback_data='channel_skip')
    markup.add(url)
    markup.add(skip,report)
    return markup

def group_task_markup(bot):
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('🔈 Join group',url='https://t.me/'+bot)
    report=InlineKeyboardButton('✅ Joined',callback_data='group_done')
    skip=InlineKeyboardButton('⚠️ Skip',callback_data='group_skip')
    markup.add(url)
    markup.add(skip,report)
    return markup

def post_task_markup():
    markup=InlineKeyboardMarkup()
    report=InlineKeyboardButton('✅ Read Post',callback_data='post_done')
    skip=InlineKeyboardButton('⚠️ Skip',callback_data='post_skip')
    markup.add(skip,report)
    return markup

def site_task_markup(bot):
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('✉️ Visit Sites',url=bot)
    report=InlineKeyboardButton('✅ Next',callback_data='site_done')
    markup.add(url)
    markup.add(report)
    return markup

def yt_task_markup(bot):
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('✉️ Watch Video',url=bot)
    report=InlineKeyboardButton('✅ Next',callback_data='yt_done')
    markup.add(url)
    markup.add(report)
    return markup

def earn_more_markup():
    markup=InlineKeyboardMarkup()
    url=InlineKeyboardButton('⭐️ Upgrade Membership',callback_data='upgrade_member')
    report=InlineKeyboardButton('🦸‍♀🦸‍♂ Buy Referrals',callback_data='rent_ref')
    skip=InlineKeyboardButton('🔙 Back',callback_data='back')
    markup.add(url)
    markup.add(report)
    markup.add(skip)
    return markup


    

def empty_markup():
    markup=InlineKeyboardMarkup()
    return markup

def empty_key_markup():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    rr=KeyboardButton("🔞 18+ Content Not Allowed")
    markup.row(rr)
    return markup



def info_markup():
    markup=InlineKeyboardMarkup(row_width=5)
    stats=InlineKeyboardButton('📊 Bot Statastics',callback_data='stats')
    #skip=InlineKeyboardButton('🔴 Terms and Conditions',url='https://telegra.ph/TERMS-AND-CONDITIONS-07-31')
    markup.add(stats)
   # markup.add(skip)
    return markup


def dis_markup():
    markup=InlineKeyboardMarkup(row_width=5)
    ref1=InlineKeyboardButton('✅ I Agree',callback_data='agree')
    ref3=InlineKeyboardButton('🚫 I Disagree',callback_data='back')
    markup.add(ref1,ref3)

def contact_admin_markup(message):
    markup=InlineKeyboardMarkup(row_width=5)
    co=InlineKeyboardButton('✅ Go to Group',url='https://t.me/'+message)
    markup.add(co)
    return markup


def deposit_markup():
    markup=InlineKeyboardMarkup(row_width=3)
    btc=InlineKeyboardButton('BTC',callback_data='btc')
    trx=InlineKeyboardButton('TRX',callback_data='trx')
    eth=InlineKeyboardButton('ETH',callback_data='eth')
    ltc=InlineKeyboardButton('LTC',callback_data='ltc')
    bch=InlineKeyboardButton('BCH',callback_data='bch')
    doge=InlineKeyboardButton('DOGE',callback_data='doge')
    xrp=InlineKeyboardButton('XRP',callback_data='xrp')
    bnb=InlineKeyboardButton('BNB',callback_data='bnb')
    dash=InlineKeyboardButton('DASH',callback_data='dash')
    markup.add(trx,btc,eth)
    markup.add(ltc,bch,doge)
    markup.add(dash,xrp,bnb)
    return markup




@bot.message_handler(commands=['h'])
def pgo(message):
    sent=bot.send_message(message.chat.id,"hsj")
    bot.register_next_step_handler(sent,j)
    
def j(message):
    print(message.animation)
    #bot.get_file(message.document.file_id)

def check_user():
    try:
        check=session.query(CheckUser).all()
        bot.send_message(431108047,"check user working") 
        ten_days_ago = date.today() - timedelta(days=10)
        bot.send_message(431108047,ten_days_ago)
        for i in check:
            if i.date >= ten_days_ago:
                a=bot.get_chat_member(chat_id=i.username,user_id=i.chat_id)
                bot.send_message(431108047,a.status)
                advertiser=session.query(Ads).filter(Ads.ad_id==i.ad_id).one()
                if a.status=='left':
                    session.query(User).filter(User.chat_id==i.chat_id).update({User.balance:User.balance-i.ppc,User.earning:User.earning-i.ppc})
                    session.commit()
                    session.query(User).filter(User.chat_id==advertiser.chat_id).update({User.balance:User.balance+i.ppc})
                    session.commit()
                    try:
                        bot.send_message(i.chat_id,f"❌ <b>You Left.</b> {i.username}\n\n You lost <b>{i.ppc}</b> because you left this channel/group " ,parse_mode='HTML')
                    except Exception:
                        bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
                    session.query(CheckUser).filter(CheckUser.chat_id==i.chat_id,CheckUser.ad_id==i.ad_id).delete()
                    session.commit()
            else:
                session.query(CheckUser).filter(CheckUser.chat_id==i.chat_id,CheckUser.ad_id==i.ad_id).delete()
                session.commit()
            time.sleep(5)
    except Exception:
            bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')

def send_alert():
    try:
        users=session.query(User).all()
        bot.send_message(431108047,"Send alert working") 
        
        for i in users:
            f=[]
            n=session.query(Task).filter(Task.chat_id==i.chat_id).all()
            for j in n:
                f.append(j.ad_id)
            a=session.query(Ads).filter(Ads.ad_id.notin_(f),Ads.status=='Enabled🔔',Ads.complete=='Yes').count()
            if a>0:
                data=f"<b>New Promotions Available</b>\n\nWe found {a} new promotions available for you today"
                try:
                    bot.send_message(i.chat_id,data,parse_mode='HTML')
                except Exception:
                    bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')
                except telebot.apihelper.ApiTelegramException:
                    continue
            time.sleep(5)
    except Exception:
                    bot.send_message('-1001372007234',f'<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()}',parse_mode='HTML')



"""x=datetime.today()
y = x.replace(day=x.day, hour=18, minute=30, second=0, microsecond=0) + timedelta(days=1)
delta_t=y-x
secs=delta_t.total_seconds()
x1=datetime.today()
y1 = x1.replace(day=x1.day, hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t1=y1-x1
secs1=delta_t1.total_seconds()

t = threading.Timer(secs, send_alert)

t1 = threading.Timer(secs, check_user)
t.start()
t1.start()
t.join()
t1.join()"""
sched.add_job(send_alert,'cron',hour=00,minute=00)
sched.add_job(check_user,'cron',hour=17,minute=30)
#sched.add_job(send_alert,'cron',hour=00)
sched.start()
atexit.register(lambda: sched.shutdown())

bot.polling()


        
    





