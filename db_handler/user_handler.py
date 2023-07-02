from models.users import Users, Candidates, UserCandidate

from sqlalchemy.exc import SQLAlchemyError


class UserDb:
    def __init__(self, session, user_id, age, sex, city):

        self.session = session
        self.user_id = user_id
        self.age = age
        self.sex = sex
        self.city = city

    @property
    def exists(self):
        """Метод проверки наличия пользователя в бд. Если пользователь есть в бд,
        проверяются данные на актуальность. Если возраст или город устарели,
        происходит обновление данных."""

        if self.session.query(Users).filter(Users.vk_id == self.user_id).first():
            if self.session.query(Users.age).filter(
                    Users.vk_id == self.user_id).first() == self.age and self.session.query(Users.city).filter(
                    Users.vk_id == self.user_id).first() == self.city:
                return True
            else:
                self.update_user()
                return True
        else:
            return False

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

    def update_user(self):
        """Метод обновления возраста и города в бд."""

        user = self.session.query(Users).filter(Users.vk_id == self.user_id).first()

        user.age = self.age
        user.city = self.city

        try:
            self.session.add(user)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            return 'DB ERROR'

        self.session.add(user)
        self.session.commit()

    def relation(self, candidate):
        """Медот добавления связей между пользователем и кандидатом."""

        user = self.session.query(Users).filter(Users.vk_id == self.user_id).first()

        try:
            user.candidates.append(candidate)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            return 'DB ERROR'

    def candidates_list(self, user):
        return self.session.query(Candidates.first_name, Candidates.last_name, Candidates.vk_id).join(
            UserCandidate).join(
            Users).filter(
            Users.vk_id == user.user_id).all()
