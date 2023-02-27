from sqlalchemy import Column, Integer, String, DateTime, func, create_engine, ForeignKey
from sqlalchemy.orm import validates, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import re

Base = declarative_base()

engine = create_engine('sqlite:///authors.db')
Session = sessionmaker(bind=engine)
session = Session()


class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    phone_number = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    posts = relationship("Post", back_populates="author")

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    summary = Column(String)
    category = Column(String)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="posts")

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be less than 250 characters")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']
        if category not in valid_categories:
            raise ValueError("Category invalid")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        is_clickbait = True
        title = title.strip()
        click_bait = ["Won't Believe", "Secret", "Guess"]
        for pattern in click_bait:
            if pattern.lower() not in title.lower():
                is_clickbait = False
        if not re.search("^&v=[0-9]*$", title):
            is_clickbait = False
        if not is_clickbait:
            raise ValueError("Must be click bait")
        else:
            return title


Base.metadata.create_all(engine)
