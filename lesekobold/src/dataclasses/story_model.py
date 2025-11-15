import typing

import pydantic


class CharacterModel(pydantic.BaseModel):
    name: str
    description: str


class SettingModel(pydantic.BaseModel):
    place: str
    time: str


class SceneModel(pydantic.BaseModel):
    scene_number: int
    scene_outline: str
    characters: list[str]
    setting: SettingModel


class StoryContentModel(pydantic.BaseModel):
    storyline: list[SceneModel]
    characters: list[CharacterModel]
    themes: list[str]
    genre: str


class StyleInputModel(pydantic.BaseModel):
    storyline: StoryContentModel
    target_grade: str
    difficulty_level: typing.Literal["easy", "medium", "hard"]


class StyleOutputModel(pydantic.BaseModel):
    story: str
    target_grade: str
    difficulty_level: typing.Literal["easy", "medium", "hard"]
    percentage_of_basic_vocabulary: float


class StorySpecificationModel(pydantic.BaseModel):
    content: str
    style: str
    level: int
