import os

from pymongo import MongoClient


class User(object):
    """The class sructure used for the User in the Mongo database."""

    def __init__(self, sender_id, name):
        self.sender_id = sender_id
        self.tools = []
        self.temp_tools = []
        self.stage = 0
        self.name = name


class DatabaseClient(object):
    """A client which connects to Mongo and deals with Mongo database operations."""

    def __init__(self):
        MONGO_URI = os.environ['mongo_uri']
        client = MongoClient(MONGO_URI)
        db = client.olinloanbot
        self.users = db.users
        self.tools = db.tindtools

    def get_all_users(self):
        """Return all users in the Users database."""
        return self.users.find({})

    def get_all_tools(self):
        """Return all tools in the Tools database."""
        return self.tools.find({})

    def get_all_available_tools(self):
        """Return all non checked out tools in the Tools database."""
        return self.tools.find({'current_user': None})

    def find_user(self, field_name, field_value):
        """Find a user from a given field, allowing to search by any field."""
        return self.users.find_one({field_name: field_value})

    def find_user_by_sender_id(self, sender_id):
        """Find one user by using the sender_id as the search field."""
        return self.users.find_one({'sender_id': sender_id})

    def find_or_create_user(self, sender_id, name):
        """Find or crate a user in the database.

        Either finds a user by sender_id, or creates that user in the database.
        Returns the user.
        """
        user = self.users.find_one({'sender_id': sender_id})
        if user is None:
            user = User(sender_id, name)
            self.users.insert_one(user.__dict__)
        user = self.users.find_one({'sender_id': sender_id})
        return user

    def update_user(self, updated_user):
        """Update a user in the database.

        Given an updated user dictionary with the same sender_id,
        replaces the old database entry with the new one
        """
        sender_id = updated_user['sender_id']
        self.users.find_one_and_replace({"sender_id": sender_id}, updated_user)

    def find_tool_by_name(self, name):
        """Find a tool by searching on the name field."""
        return self.tools.find_one({'name': name})

    def find_tool_by_id(self, tool_id):
        """Find a tool by searching on the id field."""
        return self.tools.find_one({'_id': tool_id})

    def update_tool(self, updated_tool):
        """Update a tool in the database.

        Given an updated tool dictionary with the same _id,
        replace the old database entry with the new one
        """
        self.tools.find_one_and_replace({"_id": updated_tool['_id']}, updated_tool)
