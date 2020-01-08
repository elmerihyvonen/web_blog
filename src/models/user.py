import uuid
from datetime import datetime

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    # get from mongo by email identifier
    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(collection="users", query={"email": email})
        if data is not None:
            return cls(**data)
        return None # return None is the data was None


    # get from mongo by id
    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection="users", query={"_id": _id})
        if data is not None:
            return cls(**data)
        return None # return None is the data was None



    # checks if the user email matches the password they sent
    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)

        if user is not None:
            # check the password
            return user.password == password

        return False # User does not exist so login is invalid


    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)

        if user is None:
            # user doesn't exist so we can create a user
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # user already exists
            return False


    @staticmethod
    def login(user_email):

        # login_valid has already been called
        # so we are storing their email in the session
        session['email'] = user_email


    @staticmethod
    def logout():
        session['email'] = None

    #listing all the blogs for the specific author_id
    def get_blogs(self):
        return Blog.find_by_author_id(self._id)


    # creating a new blog
    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    # writing new post
    @staticmethod
    def new_post(blog_id, title, content, date=datetime.utcnow()):

        blog = Blog.from_mongo(blog_id)

        blog.new_post(title=title,
                      content=content,
                      date=date)

    # this is only for internal use because it contains the password
    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }


    def save_to_mongo(self):
        Database.insert(collection="users", data=self.json())