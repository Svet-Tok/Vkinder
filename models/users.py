from sqlalchemy.exc import SQLAlchemyError

from models.base import Base

import sqlalchemy as sq
from sqlalchemy.orm import relationship, Session


class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String, nullable=False, unique=True)
    sex = sq.Column(sq.Integer)
    age = sq.Column(sq.Integer)
    city = sq.Column(sq.String(50))
    candidates = relationship('Candidates', secondary='users_candidates', back_populates='users', cascade='all,delete')


class Photos(Base):
    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    owner_id = sq.Column(sq.String, nullable=False, unique=True)
    like_count = sq.Column(sq.Integer, nullable=False)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.candidate_id'))


class Candidates(Base):
    __tablename__ = 'candidates'

    candidate_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    vk_id = sq.Column(sq.String, nullable=False, unique=True)
    users = relationship('Users', secondary='users_candidates', back_populates='candidates', cascade='all,delete')

    def add_user(self):
        """Метод добавления пользователя в бд."""

        user = Users(
            vk_id=self.user_id,
            sex=self.sex,
            age=self.age,
            city=self.city
        )
        try:
            self.session.add(user)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            return 'DB ERROR'

    def add_photo(self):
        """Метод добавления фотографии в бд."""

        photo = Photos(
            owner_id=self.owner_id,
            like_count=self.like_count,
            candidate_id=self.candidate_id

        )

        try:
            self.session.add(photo)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            return 'DB ERROR'

    def add_candidate(self):
        """Метод добавления кандидата в бд."""

        candidate = Candidates(
            first_name=self.first_name,
            last_name=self.last_name,
            vk_id=self.vk_id
        )

        self.session.add(candidate)

        return candidate


def check_user(engine, user_id, vk_id ):
    with Session(engine) as session:
        from_bd = session.query(Users).filter(
            Users.user_id == user_id,
            Users.worksheet_id == vk_id
        ).first()
        return True if from_bd else False
