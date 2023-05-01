from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from ...models.authentication import users as model_users
from ...models.authentication import passwords as model_password


def there_is_active_password_for_user(db: Session, user_id: int) -> bool:
    """check if the user has an active password

    Parameters
    ----------
    db : Session
        Current SqlAlchemy database session
    user_id : int
        User's id that is wanted to get the current password


    Returns
    -------
    bool
        True if the user has an active password, False other way
    """

    password = db.query(model_password.Passwords).filter(model_password.Passwords.user_id == user_id, 
                                                         model_password.Passwords.is_active == True).first()

    return password is not None


def get_active_password(db: Session, user_id: int) -> str:
    """Get the current active password. 

    Parameters
    ----------
    db : Session
        Current SqlAlchemy database session
    id_user : int
        User's id that is wanted to get the current password

    Returns
    -------
    str
        Current active password
    """

    password = db.query(model_password.Passwords).filter(model_password.Passwords.user_id == user_id, 
                                                         model_password.Passwords.is_active == True).first()
    
    return password.hashed_password


def check_password(db: Session, user_id: int, password_to_check: str) -> bool:
    """Check if the passed password is equal to the active password registered in database

    Parameters
    ----------
    db : Session
        Current SqlAlchemy database session
    id_user : int
        User's id that is gonna be checked
    password_to_check : str
        password to be checked against the database

    Returns
    -------
    bool
        True if the password is correct, False if not
    """

    current_active_password = get_active_password(db, user_id)
    hashed_password_to_check = model_password.Passwords.set_password(password_to_check)

    return current_active_password == hashed_password_to_check
    
 
def create_password(db: Session, user_id: int, password: str, expiration_date: date = None) -> model_password.Passwords:
    """Create a password only if there is no active password for the current user

    Parameters
    ----------
    db : Session
        Current SqlAlchemy database session
    user_id : int
        User that is gonna be created the password
    password : str
        password to be setted
    expiration_date : date, optional
        The espiration date for the password, by default None

    Returns
    -------
    model_password.Passwords
        Model Password object
    """

    if there_is_active_password_for_user(db, user_id):
        raise HTTPException(status_code=400, detail="there is already an active password. Use update_password method instead of create_password method")
    
    hashed_password = model_password.Passwords.set_password(password)

    db_password = model_password.Passwords(user_id=user_id,
                                           hashed_password=hashed_password,
                                           expiration_date=expiration_date)
    
    db.add(db_password)
    db.commit()
    db.refresh(db_password)

    return db_password  


def disable_passwords(db: Session, user_id: int) -> int:
    """Disables all password for an user

    Parameters
    ----------
    db : Session
        Current SqlAlchemy database session
    user_id : int
        User that is gonna be disabled

    Returns
    -------
    int
        User's id that is disabled
    """

    db.query(model_password.Passwords).filter(model_password.Passwords.user_id == user_id).update({'is_active': False})
    db.commit()

    return user_id


def update_password(db: Session, user_id: int, current_password: str, new_password: str, expiration_date: date = None) -> model_password.Passwords:
    """ Upadate the current password for the user

    Parameters
    ----------
    db : Session
        Current SqlAlchemy database session
    user_id : int
        User that is gonna get a new password
    current_password : str
        password to be checked
    new_password : str
        new password for the user
    expiration_date : date, optional
        The espiration date for the password, by default None

    Returns
    -------
    model_password.Passwords
        Model Password object
    """

    if not there_is_active_password_for_user(db, user_id):
        raise HTTPException(status_code=400, detail="there is no an active password. Use create_password method instead of update_password method")
    
    if check_password(db, user_id, current_password):
        # this make this function a non pure function
        disable_passwords(db, user_id)
        return create_password(db, user_id, new_password, expiration_date)
    
    else:
        raise HTTPException(status_code=400, detail="Password can not be changed. Current active password does not match with the 'Current password given'")


