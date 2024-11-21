#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Save the user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # session = self._session
        try:
            self._session.add(new_user)
            self._session.commit()
            self._session.refresh(new_user)
            return new_user
        except Exception:
            pass

    def find_user_by(self, **kwargs) -> User:
        """Returns first row found in the users table
        that matches the kwargs filter
        """
        from sqlalchemy.orm.exc import NoResultFound
        from sqlalchemy.exc import InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user:
                return user
            raise NoResultFound
        except InvalidRequestError as exception:
            raise exception

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Use self.find_user_by to locate and update a user
        """
        user = self.find_user_by(id=user_id)
        if user:
            for attribute, value in kwargs.items():
                if user.__dict__.get(attribute):
                    user.__dict__[attribute] = value
                else:
                    raise ValueError
