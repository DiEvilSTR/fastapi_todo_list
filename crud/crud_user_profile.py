from sqlalchemy.orm import selectinload, Session


from models.user import UserProfile
from schemas.user_profile import UserProfileUpdate


def user_profile_get(db: Session, username: str):
    return db.query(UserProfile).filter(UserProfile.username == username).first()


def user_profile_create(db: Session, username: str):
    db_user_profile = UserProfile(username=username)
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)
    return db_user_profile


def user_profile_update(db: Session, user_profile: UserProfileUpdate, username: str):
    db_user_profile = user_profile_get(db=db, username=username)
    updated_user_profile = user_profile.dict(exclude_unset=True)
    for key, value in updated_user_profile.items():
        setattr(db_user_profile, key, value)
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)
    return db_user_profile