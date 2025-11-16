import pydantic


class StoryModel(pydantic.BaseModel):
    """A story model that contains the basic story and the target grade."""

    title: str
    basic_story: str
    target_grade: int


class LeveledStoryModel(StoryModel):
    """A leveled story model that contains different versions of the story."""

    target_grade: int
    # lix_score: float
    percentage_of_basic_vocabulary: float
    observed_grade: int
    # text_is_covered_by_basic_vocab: bool

    easy_story: str
    medium_story: str
    challenging_story: str


class LeveledStoryCollectionModel(pydantic.BaseModel):
    """A leveled story collection model that contains different leveled stories."""

    target_grade: int
    easy_story: LeveledStoryModel
    medium_story: LeveledStoryModel
    challenging_story: LeveledStoryModel


class StorySpecificationModel(pydantic.BaseModel):
    """A story specification model that contains the content, style and level."""

    content: str
    style: str
    level: int


class JudgeOutputModel(LeveledStoryModel):
    """A judge output model that contains feedback and refinement decision."""

    lix_score: float
    text_is_covered_by_basic_vocab: bool
    feedback: str
    needs_refinement: bool
