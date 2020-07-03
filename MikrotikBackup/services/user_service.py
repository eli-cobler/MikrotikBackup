from typing import Optional, List

from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import MikrotikBackup.data.db_session as db_session
from MikrotikBackup.data.users import User

def get_users_list() -> List[User]:
    session = db_session.create_session()
    routers = session.query(User). \
        order_by(User.name.asc()). \
        all()

    session.close()

    return routers

def get_is_admin(user_id):
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()

def get_user_count() -> int:
    session = db_session.create_session()
    try:
        return session.query(User).count()
    finally:
        session.close()

def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.email == email).first()
    finally:
        session.close()

def create_user(name: str, email: str, password: str, is_admin) -> Optional[User]:
    if find_user_by_email(email):
        return None

    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_text(password)
    user.is_admin = is_admin

    session = db_session.create_session()
    try:
        session.add(user)
        session.commit()
    finally:
        session.close()

    return user

def delete_user_by_id(user_id: int):
    if not find_user_by_id(user_id):
        return None

    session = db_session.create_session()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()
    finally:
        session.close()

def delete_user_by_email(email: str):
    if not find_user_by_email(email):
        print('no user found')
        return None

    session = db_session.create_session()

    try:
        user = session.query(User).filter(User.email == email).first()
        session.delete(user)
        session.commit()
        print('user deleted')
    finally:
        session.close()

def hash_text(text: str) -> str:
    return crypto.encrypt(text, rounds=171204)

def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)

def login_user(email: str, password: str) -> Optional[User]:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return None

        if not verify_hash(user.hashed_password, password):
            return None

        return user
    finally:
        session.close()

def find_user_by_id(user_id: int) -> Optional[User]:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()
