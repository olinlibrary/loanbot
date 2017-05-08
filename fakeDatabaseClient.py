# the class structure used for the User in the Mongo database
tools_list = [{
    "_id": {
        "$oid": "58e5528dbf24551abe30660f"
    },
    "current_user": {
        "$oid": "58ebabe3638acc000b2e2429"
    },
    "name": "screwdriver",
    "alternate_names": [],
    "current_due_date": 1492100080
}, {
    "_id": {
        "$oid": "58e5528dbf24551abe306610"
    },
    "current_due_date": 1491424505,
    "name": "drill",
    "alternate_names": [],
    "current_user": {
        "$oid": "58dfe761db78bb000bf7c88b"
    }
}, {
    "_id": {
        "$oid": "58e5528dbf24551abe306611"
    },
    "name": "arduino",
    "alternate_names": [],
    "current_due_date": None,
    "current_user": None
}]

users_list = [{
    "_id": {
        "$oid": "58ebabe3638acc000b2e2429"
    },
    "sender_id": "1346430625424620",
    "tools": [{
        "$oid": "58e5528dbf24551abe30660f"
    }],
    "stage": 0,
    "temp_tools": []
}]


class User(object):
    def __init__(self, sender_id):
        self.sender_id = sender_id
        self.tools = []
        self.temp_tools = []
        self.stage = 0


class FakeDatabaseClient(object):
    """A client which connects to Mongo and deals with Mongo database operations."""

    def get_all_users(self):
        """Fake version of get_all_users."""
        return users_list

    def get_all_tools(self):
        """Fake version of get_all_tools."""
        return tools_list

    def find_user(self, field_name, field_value):
        """Fake version of find_user."""
        return None

    def find_user_by_sender_id(self, sender_id):
        """Fake version of find_user_by_sender_id."""
        return None

    def find_or_create_user(self, sender_id, name):
        """Fake version of find_or_create_user."""
        return users_list[0]

    def update_user(self, updated_user):
        """Update a user in the database.

        Given an updated user dictionary with the same sender_id,
        replaces the old database entry with the new one
        """
        sender_id = updated_user['sender_id']
        self.users.find_one_and_replace({"sender_id": sender_id}, updated_user)

    def find_tool_by_name(self, name):
        """Find a tool by searching on the name field."""
        return None
        # return self.tools.find_one({'name':name})

    def find_tool_by_id(self, tool_id):
        """Find a tool by searching on the id field."""
        return None
        # return self.tools.find_one({'_id':tool_id})

    def update_tool(self, updated_tool):
        """Update a tool in the database.

        Given an updated tool dictionary with the same _id,
        replaces the old database entry with the new one
        """
        return None
        # self.tools.find_one_and_replace({"_id":updated_tool['_id']}, updated_tool)
