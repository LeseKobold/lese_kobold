import pydantic


class StoryModel(pydantic.BaseModel):
    """A story model that contains the basic story and the target grade."""

    title: str
    basic_story: str
    target_grade: int


class LeveledStoryModel(StoryModel):
    """A leveled story model that contains different versions of the story."""

    percentage_of_basic_vocabulary: float
    observed_grade: int

    easy_story: str
    medium_story: str
    challenging_story: str


class StorySpecificationModel(pydantic.BaseModel):
    """A story specification model that contains the content, style and level."""

    content: str
    style: str
    level: int
