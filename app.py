#!venv/bin/python
import os
from flask import Flask, url_for, redirect, render_template, request, abort,flash,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
import flask_admin
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose,helpers
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import UserMixin,login_required,LoginManager,current_user,login_user,current_user,logout_user
from flask_bcrypt import Bcrypt
from wtforms import form, fields, validators
from urllib.parse import unquote_plus
import json
import re
from flask_restful import Api,Resource
import sys
import hashlib
import datetime
import string
from random import choices
#from models import User,engine,User,Transaction,Deposit,Withdraw,Alert,Ads,Task,API_KEY,Wallet,Testgroup,CheckUser


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')    
db = SQLAlchemy(app)
Base=automap_base()
Base.prepare(db.engine,reflect=True)
api=Api(app)
bcrypt=Bcrypt(app)
login=LoginManager(app)
login.login_view='admin.login'
login.login_message_category='info'







class Role(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    password=db.Column(db.String)

Users=Base.classes.user
Ads=Base.classes.ads
Deposit=Base.classes.trans
Withdraw=Base.classes.withdraw
Min=Base.classes.min
Api=Base.classes.api
ShortURL=Base.classes.short_url
Task=Base.classes.task
IP=Base.classes.whitelist

@login.user_loader
def user_loader(admin_id):
    return Role.query.get(admin_id)



class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])
    submit=fields.SubmitField('Login')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if  user.password!=self.password.data:
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(Role).filter_by(name=self.username.data).first()
# Setup Flask-Security
#user_datastore = SQLAlchemyUserDatastore(db, Users,Balance)
#security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):
    
    
    def is_accessible(self):

        if not current_user.is_active or not current_user.is_authenticated:
            return False

        else:
            return True
            

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('login_view', next=request.url))


    can_edit = False
    edit_modal = False
    create_modal = True   
    can_export = True
    can_view_details = True
    details_modal = True


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        total_users=db.session.query(Users).count()
        total_ads=db.session.query(Ads).count()
        total_deposit=db.session.query(Deposit).count()
        total_withdraw=db.session.query(Withdraw).filter_by(status='Confirmed').count()
        top_users=db.session.query(Users).order_by(Users.balance.desc()).limit(20).all()
        top_ref=db.session.query(Users).order_by(Users.refferal.desc()).limit(20).all()
        top_earning=db.session.query(Users).order_by(Users.earning.desc()).limit(20).all()
        context={'total_users':total_users,'total_ads':total_ads,'total_deposit':total_deposit,'total_withdraw':total_withdraw,'top_ref':top_ref,'top_users':top_users,'top_earn':top_earning}
        if not current_user.is_authenticated:
            return redirect(url_for('role.index_view'))
        return self.render('admin/custom_index.html',context=context)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user is not None:
                login_user(user)
                if current_user.is_authenticated:
                    return redirect(url_for('admin.index'))
            else:
                    flash(f'Login Unsucessful','danger')


        self._template_args['form'] = form
        return self.render('admin/login.html',form=form)

#a=session.query(User).order_by(User.refferal_earn.desc()).limit(20).all()
        

class UserView(MyModelView):
    can_create = False
    can_delete=False
    can_edit = False
    
    column_editable_list = ['balance','ban','earning']
    column_searchable_list = ['chat_id','first_name','username','ip']
    column_exclude_list = ['user_hash','refferal_hash','last_name']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list


class IPView(MyModelView):
    can_create = True
    can_delete=True
    can_edit = False
    
    column_editable_list = []
    column_searchable_list = ['address']
    column_exclude_list = []
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class AdsView(MyModelView):
    can_create = False
    can_delete=True
    can_edit = True
    column_editable_list = []
    column_searchable_list = ['chat_id','ad_type','porn','ppc','budget']
    column_exclude_list = []
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class MinView(MyModelView):
    can_create = False
    can_delete=False
    can_edit = True
    column_editable_list = []
    column_searchable_list = []
    column_exclude_list = []
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class DepositView(MyModelView):
    can_create = False
    can_delete=False
    can_edit = False
    column_editable_list = []
    column_searchable_list = ['chat_id','amt','txn','status']
    column_exclude_list = []
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class WithdrawView(MyModelView):
    can_create = False
    can_delete=False
    can_edit = False
    column_editable_list = []
    column_searchable_list = ['chat_id','amt','status','username']
    column_exclude_list = ['message_id']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class TaskView(MyModelView):
    can_create = False
    can_delete=False
    can_edit = False
    column_editable_list = []
    column_searchable_list = ['chat_id']
    column_exclude_list = []
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class APIView(MyModelView):
    can_create = False
    can_delete=False
    can_edit = True
    column_editable_list = []
    column_searchable_list = []
    column_exclude_list = []
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class CustomView(BaseView):
    @expose('/')
    def index(self):
        total_users=db.session.query(Users).count()
        total_ads=db.session.query(Ads).count()
        total_deposit=db.session.query(Deposit).count()
        total_withdraw=db.session.query(Withdraw).filter_by(status='Confirmed').count()
        
        #a=db.session.query(Balance).order_by(Balance.refferal.desc()).limit(20).all()
        context={'total_users':total_users,'total_ads':total_ads,'total_deposit':total_deposit,'total_withdraw':total_withdraw}
        return self.render('admin/custom_index.html',context=context)

    
# Flask views
@app.route('/')
def index():

    return render_template('index.html')


# Create admin
admin = flask_admin.Admin(
    app,
    'My Dashboard',
    index_view=MyAdminIndexView(),
    base_template='my_master.html',
    template_mode='bootstrap3',
)


@app.route('/login/',methods=['GET','POST'])
def login_view():
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        
        return redirect(url_for('admin.login_view',form=form))
    


@app.route('/process/')
def process():
        ipn_version = request.form.get(["ipn_version"])
        ipn_id = request.form.get["ipn_id"]
        ipn_mode = request.form.get["ipn_mode"]
        merchant = request.form.get["merchant"]
        txn_id = request.form.get["txn_id"]
        status =request.form.get["status"]


        print(ipn_id)
        
    
        return status

class short_url(Resource):
    def get(self):
        self.original_url = request.args.get('longurl')
        self.chat_id=request.args.get('chat_id')
        self.ad=request.args.get('ad')
        print(self.ad)
        link = ShortURL(long_url=self.original_url,chat_id=self.chat_id,short_url=generate_short_link(),ad_id=self.ad)
        db.session.add(link)
        db.session.commit()
        return jsonify(short_url="http://162.0.230.68:5000/redirect/"+link.short_url)

def generate_short_link():
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=6))
        link = db.session.query(ShortURL).filter_by(short_url=short_url).first()
        
        if link:
            return generate_short_link()
        
        return short_url

class yt_short_url(Resource):
    def get(self):
        self.original_url = request.args.get('longurl')
        self.chat_id=request.args.get('chat_id')
        self.ad=request.args.get('ad')
        print(self.ad)
        link = ShortURL(long_url=self.original_url,chat_id=self.chat_id,short_url=generate_yt_short_link(),ad_id=self.ad)
        db.session.add(link)
        db.session.commit()
        return jsonify(short_url="http://162.0.230.68:5000/watch/"+link.short_url)

def generate_yt_short_link():
        characters = string.digits + string.ascii_letters
        short_url = 'yt_'+''.join(choices(characters, k=6))
        link = db.session.query(ShortURL).filter_by(short_url=short_url).first()
        
        if link:
            return generate_short_link()
        
        return short_url

@app.route('/redirect/<link>')
def redirect_long(link):
    long=db.session.query(ShortURL).filter_by(short_url=link).first()
    if long.long_url==None or long.status=="Complete":
        return render_template('task_done.html')
    
    ad=db.session.query(Ads).filter_by(ad_id=long.ad_id).one() 
    user_data=db.session.query(Users).filter_by(chat_id=long.chat_id).one()
    if user_data.ip==None:
        db.session.query(Users).filter_by(chat_id=long.chat_id).update(dict(ip=request.remote_addr))
        db.session.commit()
    db.session.query(Users).filter_by(chat_id=long.chat_id).update(dict(balance=user_data.balance+ad.ppc*0.6,earning=user_data.earning+ad.ppc*0.6))
    db.session.commit()
    print(user_data.refferal_hash)
    if user_data.refferal_hash=='':
        pass
    else:
        ref=db.session.query(Users).filter_by(user_hash=user_data.refferal_hash).one()
        db.session.query(Users).filter_by(user_hash=user_data.refferal_hash).update(dict(balance=ref.balance+(ad.ppc*0.06),earning=ref.earning+(ad.ppc*0.06),refferal_earn=ref.refferal_earn+(ad.ppc*0.06)))
        db.session.commit()
    db.session.query(Ads).filter_by(ad_id=long.ad_id).update(dict(r_balance=ad.r_balance-ad.ppc,visits=ad.visits+1))
    db.session.commit()
    advertise=db.session.query(Users).filter_by(chat_id=ad.chat_id).one()
    if advertise.balance<=advertise.earning:
        db.session.query(Users).filter_by(chat_id=advertise.chat_id).update(dict(balance=advertise.balance-ad.ppc,earning=advertise.earning-ad.ppc))
        db.session.commit()
    else:
        db.session.query(Users).filter_by(chat_id=advertise.chat_id).update(dict(balance=advertise.balance-ad.ppc))
        db.session.commit()
    if ad.r_balance<ad.ppc or ad.r_balance>advertise.balance:
        db.session.query(Ads).filter_by(ad_id=long.ad_id).update(dict(status='⏸ Paused : Insufficient Fund/Budget Reached '))
        db.session.commit()
    db.session.query(ShortURL).filter_by(short_url=link).update(dict(status="Complete"))
    db.session.commit()

    return render_template('redirect.html',long_url=long.long_url,ppc=ad.ppc*0.6)

@app.route('/watch/<link>')
def yt_redirect_long(link):
    long=db.session.query(ShortURL).filter_by(short_url=link).first()
    if long.long_url==None or long.status=="Complete":
        return render_template('task_done.html')
    
    ad=db.session.query(Ads).filter_by(ad_id=long.ad_id).one() 
    user_data=db.session.query(Users).filter_by(chat_id=long.chat_id).one()
    if user_data.ip==None:
        db.session.query(Users).filter_by(chat_id=long.chat_id).update(dict(ip=request.remote_addr))
        db.session.commit()
    db.session.query(Users).filter_by(chat_id=long.chat_id).update(dict(balance=user_data.balance+ad.ppc*0.6,earning=user_data.earning+ad.ppc*0.6))
    db.session.commit()
    print(user_data.refferal_hash)
    if user_data.refferal_hash=='':
        pass
    else:
        ref=db.session.query(Users).filter_by(user_hash=user_data.refferal_hash).one()
        db.session.query(Users).filter_by(user_hash=user_data.refferal_hash).update(dict(balance=ref.balance+(ad.ppc*0.06),earning=ref.earning+(ad.ppc*0.06),refferal_earn=ref.refferal_earn+(ad.ppc*0.06)))
        db.session.commit()
    db.session.query(Ads).filter_by(ad_id=long.ad_id).update(dict(r_balance=ad.r_balance-ad.ppc,visits=ad.visits+1))
    db.session.commit()
    advertise=db.session.query(Users).filter_by(chat_id=ad.chat_id).one()
    if advertise.balance<=advertise.earning:
        db.session.query(Users).filter_by(chat_id=advertise.chat_id).update(dict(balance=advertise.balance-ad.ppc,earning=advertise.earning-ad.ppc))
        db.session.commit()
    else:
        db.session.query(Users).filter_by(chat_id=advertise.chat_id).update(dict(balance=advertise.balance-ad.ppc))
        db.session.commit()
    if ad.r_balance<ad.ppc or ad.r_balance>advertise.balance:
        db.session.query(Ads).filter_by(ad_id=long.ad_id).update(dict(status='⏸ Paused : Insufficient Fund/Budget Reached '))
        db.session.commit()
    db.session.query(ShortURL).filter_by(short_url=link).update(dict(status="Complete"))
    db.session.commit()
    print(long.long_url)
    return render_template('yt_redirect.html',long_url=long.long_url,ppc=ad.ppc*0.6)


@app.route('/task_done/<ppc>')
def task_done(ppc):
    return render_template('earn.html',ppc=ppc)

api.add_resource(short_url,'/short')
api.add_resource(yt_short_url,'/yt')

# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Admin"))
admin.add_view(UserView(Users, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(AdsView(Ads, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Advertisiments"))
admin.add_view(DepositView(Deposit, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Deposit"))
admin.add_view(WithdrawView(Withdraw, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Withdraw"))
admin.add_view(MinView(Min, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Edit Price"))
admin.add_view(APIView(Api, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="API KEY"))
admin.add_view(IPView(IP, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="IP Whitelist"))
admin.add_view(TaskView(Task, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="User Task"))
admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
   # if not os.path.exists(database_path):
       # build_sample_db()
    # Start app
    app.run(host='0.0.0.0')