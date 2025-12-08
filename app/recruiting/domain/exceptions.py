class SkillAlreadyExists(Exception):
    pass


class SkillNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
