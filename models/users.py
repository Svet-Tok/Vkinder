from models.base import Base

import sqlalchemy as sq
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String, nullable=False, unique=True)
    sex = sq.Column(sq.Integer)
    age = sq.Column(sq.Integer)
    city = sq.Column(sq.String(50))
    candidates = relationship('Candidates', secondary='users_candidates', back_populates='users', cascade='all,delete')


class UserCandidate(Base):
    __tablename__ = 'users_candidates'

    __table_args__ = (sq.PrimaryKeyConstraint('user_id', 'candidate_id'),)

    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'))
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.candidate_id'))


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
