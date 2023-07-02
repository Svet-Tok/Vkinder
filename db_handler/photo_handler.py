from sqlalchemy.exc import SQLAlchemyError

from models.users import Photos


class PhotoDB:
    def __init__(self, session, candidate_id, owner_id, like_count):
        self.session = session
        self.owner_id = owner_id
        self.like_count = like_count
        self.candidate_id = candidate_id

    def exists(self):
        """Метод проверки наличия фотографии в бд."""

        return self.session.query(Photos).filter(Photos.owner_id == self.owner_id).first()

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
