from datetime import datetime, timedelta
import streamlit as st
import extra_streamlit_components as stx
import jwt
import yaml


# load cookie manager
cookie_manager = stx.CookieManager()


# extract cookie settings
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)
cookie_name = config['cookie']['name']
cookie_key = config['cookie']['key']
cookie_expiry_days = config['cookie']['expiry_days']


def login(username, password):
    # TODO: perform authentication with backend
    # store username
    st.session_state.username = username
    return True


def register(username, email, password):
    # TODO: perform authentication with backend
    # store username
    st.session_state.username = username
    return True


def encode_cookie():
    # encode cookie JSON
    exp_date = (datetime.now() + timedelta(days=cookie_expiry_days)).timestamp()
    cookie_dict = {
        'username': st.session_state.username,
        'exp_date': exp_date}
    token = jwt.encode(
        cookie_dict, 
        cookie_key, 
        algorithm='HS256')
    return token


def decode_cookie(token):
    # decode cookie JSON
    cookie_dict = jwt.decode(token, cookie_key, algorithms=['HS256'])
    return cookie_dict


def get_cookie():
    # get authentication cookie 
    token = cookie_manager.get(cookie_name)
    if token is not None:
        cookie_dict = decode_cookie(token)
        if (cookie_dict is not False and 'username' in cookie_dict and
            cookie_dict['exp_date'] > datetime.now().timestamp()):
            return cookie_dict
    return None


def set_cookie():
    # set authentication cookie
    # cookie_manager = get_cookie_manager()
    token = encode_cookie()
    exp_date = datetime.now() + timedelta(days=cookie_expiry_days)
    cookie_manager.set(cookie_name, token, expires_at=exp_date)


def delete_cookie():
    cookie_manager.delete(cookie_name)


def authenticate_user():
    # widget for user authentication
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        st.header("Login")
        # login form
        login_form = st.form(key='login')
        username = login_form.text_input('Username')
        password = login_form.text_input('Password', type='password')
        # on submit button click, process user details
        if login_form.form_submit_button('Login'):
            if login(username, password):
                set_cookie()
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error('Invalid login credentials')
    with register_tab:
        st.header("Register")
        # register form
        register_form = st.form(key='register')
        username = register_form.text_input('Username')
        email = register_form.text_input('Email')
        password = register_form.text_input('Password', type='password')
        confirm_password = register_form.text_input('Confirm Password', type='password')
        # on submit button click, process user details
        if register_form.form_submit_button('Register'):
            if password != confirm_password:
                st.error('Passwords must match')
            elif register(username, email, password):
                set_cookie()
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error('Registration failed')


def logout_user():
    if not st.session_state.authenticated:
        return 
    delete_cookie()
    st.session_state.authenticated = False
    st.rerun()


def check_cookie():
    token = get_cookie()
    if token:
        # TODO: authenticate token
        st.session_state.username = token['username']
        st.session_state.authenticated = True