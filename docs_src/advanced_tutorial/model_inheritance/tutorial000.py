import os

from mongodb_odm import (
    ASCENDING,
    Document,
    Field,
    IndexModel,
    ODMObjectId,
    apply_indexes,
    connect,
)


class Course(Document):
    title: str


class Content(Document):
    course_id: ODMObjectId
    title: str = Field(max_length=255)

    class Config(Document.Config):
        allow_inheritance = True
        indexes = [
            IndexModel([("course_id", ASCENDING)]),
        ]


class Text(Content):
    text: str

    class Config(Document.Config):
        allow_inheritance = False


class Video(Content):
    video_path: str = Field(max_length=512)

    class Config(Document.Config):
        allow_inheritance = False


def configuration():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()


def create_data():
    course = Course(title="MongoDB-ODM Tutorial").create()

    Text(course_id=course.id, title="Introduction", text="Introduction Text").create()
    Video(
        course_id=course.id,
        title="Environment Setup",
        video_path="/media/video_path.mp4",
    ).create()


def retrieve_content():
    for content in Content.find():
        print(content)
    print()


def retrieve_text():
    for text in Text.find():
        print(text)
    print()


def retrieve_video():
    for video in Video.find():
        print(video)
    print()


def main():
    configuration()

    create_data()

    retrieve_content()
    retrieve_text()
    retrieve_video()


if __name__ == "__main__":
    main()
