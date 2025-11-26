from pydantic import BaseModel, ConfigDict, Field


class SkillBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(min_length=1, max_length=25)


class Skill(SkillBase):
    pass


class PostSkill(SkillBase):
    pass


class GetSkill(SkillBase):
    pass
