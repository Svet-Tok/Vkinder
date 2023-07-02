from models.users import Candidates


class CandidateDB:
    def __init__(self, session, first_name, last_name, vk_id):
        self.session = session
        self.first_name = first_name
        self.last_name = last_name
        # self.vk_id = vk_id

    def exists(self):
        """Метод проверки наличия кандидата в бд."""

        return self.session.query(Candidates).filter(Candidates.vk_id == self.vk_id).first()

    def add_candidate(self):
        """Метод добавления кандидата в бд."""

        candidate = Candidates(
            first_name=self.first_name,
            last_name=self.last_name
            # vk_id=self.vk_id
        )

        self.session.add(candidate)

        return candidate

    def get_id(self):
        """Метод возвращает id кандидата"""

        return self.session.query(Candidates.candidate_id).filter(Candidates.vk_id == self.vk_id).first()
