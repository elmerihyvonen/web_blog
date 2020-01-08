import uuid
import datetime

from src.common.database import Database
from src.models.post import Post


class Blog(object):

    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        # uuid4() for random value and .hex gives hexdecimal
        self._id = uuid.uuid4().hex if _id is None else _id


    def new_post(self, title, content, date=datetime.datetime.utcnow()):

        post = Post(blog_id=self._id, # self._id is now the blog_id for the Post
                    author=self.author, # author is the same for blog and Post
                    title=title,
                    content=content,
                    created_date=date)

        post.save_to_mongo()


    def get_posts(self):
        return Post.from_blog(self._id)


    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())


    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }


    # used to return the blog instance for menu program
    @classmethod
    def from_mongo(cls, id):

        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})

        #creates a Blog object with found data and returns it
        #cls refers to current class which is Blog

        return cls(**blog_data)


    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})

        # creates a blog object for each blog found in blogs and returning
        # them as a list of blog objects
        return [cls(**blog) for blog in blogs]

