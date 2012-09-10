import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from pyramid.security import (
    Allow,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
            (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)
    content = Column(Text)
    status = Column(Integer)
    tags = Column(Text)

    def __init__(self, title, content, status, tags):
        self.title = title
        self.content = content
        self.status = status
        self.tags = tags


"""class Photo(Base):
    __tablename__ = 'photo'
    upload = Column(Text)
    date_created = Column(DateTime, default=datetime.datetime.now())
    is_image = Column(Boolean, default=True)

    def __init__(self, upload, date_created, is_image):
        self.upload = upload
        self.date_created = date_created
        self.is_image
"""
