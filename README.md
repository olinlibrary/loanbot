# Loan Wrangler Chatbot

[![Build Status](https://travis-ci.org/olinlibrary/loanbot.svg?branch=master)](https://travis-ci.org/olinlibrary/loanbot)
[![Documentation Status](https://readthedocs.org/projects/olin-loan-wrangler/badge/?version=latest)](http://olin-loan-wrangler.readthedocs.io/en/latest/?badge=latest)

Loan Wrangler is a friendly chatbot, ready to help you with (almost) anything involving borrowing and using the library’s awesome tools and media equipment.

## Why a Loan Chatbot?

Libraries are awesome because they want you to have what you want, when you want it, for free. This started with books, then digital resources, and now the possibilities are endless! For example, the Olin College library wants users to be able to borrow tools and media equipment. Since the current loan system wasn’t made for tools (which are different than books in a few key ways), we created a chatbot that can help library patrons check out, use, and return tools in a much more flexible, friendly, and fun way.

![A list of reasons that loans of books, tools, and media equipment must be handled differently: 1 Different loan time. 2 Different loan frequency. 3 Different kind of help needed to use the item.](./docs/images/LoanWranglerDemo.png "Why a loan chatbot?")

## Conversing With Loan Wrangler

Since the bot is still under development and not yet public, you will need to chat with it from the Library’s facebook account.  To be able to message it yourself, you will need to be added to the page’s admins by the Library.

When you message Loan Wrangler, it will do its best to meet all your tool and media equipment loan needs. Since it is still a young bot, you will notice it doesn't have answers for everything! Here is an example conversation you might have:

![Screenshot from a demo conversation with the chatbot. The user and bot exchange a greeting, then the user asks if the drill is available. The bot replies that the drill is not available, and offers to ask the person who borrowed it to bring it back. The user confirms that they wan this, and the bot says it has let the drill borrower know.](./docs/images/greetingAndAvailability.png "Demo Conversation")

At this point the bot would send a message to the user with the drill checked out, like "someone's looking for the drill, could you return it if you're done using it?" Once the drill is returned, the next user can check it out:

![Screenshot from a demo conversation with the chatbot. The user says they want the drill, and the bot confirms the item, then asks whether a loan time of 1 day is okay or whether 12 hours or 3 days would be better. The user chooses 1 day, and the bot says they're all set, it will remind them to return the drill before it is due.](./docs/images/checkOutDrill.png "Demo Conversation")

Shortly before the drill is due, the bot will send a reminder, and keep sending periodic reminders until the drill is returned.

![Screenshot from a demo conversation with the chatbot. The bot lets the user know that the drill is due soon, and asks them to bring it back to the library.](./docs/images/returnPlease.png "Demo Conversation")

When the user returns the drill, they can let the bot know it's back:

![Screenshot from a demo conversation with the chatbot. The user says they returned the drill, and the bot confirms the tool, then thanks the user and says it will let The Library know the drill has returned.](./docs/images/returnDrill.png "Demo Conversation")

A user can also check out more than one tool at a time, and ask for help with tools:

![Screenshot from a demo conversation with the chatbot. In one message the user asks for three different tools. As before, teh bot confirms the three tools, offers loan times, and lets the user know that it will remind them to return the tools. The user then asks how to use a soldering iron. The bot offers a link to a youtube video.](./docs/images/checkOutMultipleTools.png "Demo Conversation")

Likewise, a user can return more than one tool at a time:

![Screenshot from a demo conversation with the chatbot. In one message the user says they have returned two tools, the sewing machine and the gimbal. The bot confirms the tools and thanks the user.](./docs/images/returnTwoTools.png "Demo Conversation")

If a user asks for help that Loan Wrangler isn't equipped to give, it redirects their question to the librarians (note that this feature is only partially complete).

![Screenshot from a demo conversation with the chatbot. The user asks what they should do with their life. The bot says it doesn't know how to help them and that it has passed their question on to the librarians, who will hopefully know what to do and will contact the user soon.](./docs/images/helpwithmylife.png "Demo Conversation")

## Product Manager

### Project Status

Currently, the bot can:

- Check out an item to a user
- Accept a returned item
- List some tools available
- Send reminders to a user when a tool is nearly due
- Indicate whether a desired item is available
- Ask a user to return an item at the request of another user
- Give resources to help a user with an item, or send an email to the librarians when it doesn’t know how to help

We’ve been tracking bugs and new feature ideas on the GitHub issues page.

#### Known bugs

The return reminders are currently done using a threaded interval timer.  There’s a current bug where the messages are sent twice instead of once, usually one second apart.  We spent a lot of time looking at it and have been unable to figure out why.

## Developer

### Installation instructions

1\. Either install a local MongoDB instance, or provision a hosted instance and set `mongo_uri` to its URL.

macOS running [Homebrew](https://brew.sh): run `brew install mongodb`, and then following the instructions to start the instance.

Ubuntu: follow [these instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition) to install and run a local instance.

Hosted instance (for example, mLab): Set the `mongo_uri` envirnonment variable to a [MongoDB connection string URI](https://docs.mongodb.com/manual/reference/connection-string/) to the instance.

2\. Install Python package dependencies: `pip install -r requirements.txt`.  If you want to update the documentation, you will also need to run `pip install -r requirements-dev.txt`. Also, this project is written in Python 3, so if you’re not using a virtual environment, you should run those commands instead with `sudo pip3`.

3\. Run `python3 create_tools_from_tind.py`.

4\. Set the following environment variables:

Our code has the following app secrets:

- `validationToken` is a Facebook variable that confirms for Facebook that you own the app that you say you own. You can set this to anything for local development.
- `pageAccessToken` is generated by Facebook for your page. You can set this to anything for local development.

### The Bot Files

Our code contains four primary files:

- `server.py` is the main application with the Flask routing structure.  It creates instances of the next three objects.
- `messenger_client.py` defines a class for interfacing with the sending and receiving of Facebook messages.
- `database_client.py` defines a class for interacting with the Mongo database, and includes functions that get and set the various information we care about.
- `conversation_handler.py` is the primary program for parsing received message text and determining the appropriate response.  It takes a database client in its constructor since it needs to get tool and user information.

We also have some additional files:

- `create_dummy_tools.py` populates the database with a dummy set tools of tools, for testing.  This is currently obsolete.
- `create_tools_from_tind.py` populates the tools database by pulling an XML from Tind and parsing it.  This is a separate script from our app, so it only executes when it is explicitly run.  Future work could including making this update live.
- `send_email_to_librarian.py` is imported and used to send an email when needed.
- `tests.py` contains our tests.  The test coverage is low and non-ideal.
- `fake_database_client.py` creates a fake database client that returns fake data, to be used in the tests.

### Understanding Conversation Handling

We use user stages to keep track of where a user is in their conversation, and use that information to decide what they mean when we receive a message that just says “yes”, for example.  The stages are:

```python
self.NO_CONTACT = 0
self.SENT_GREETING = 1
self.WANT_CHECKOUT = 2
self.CONFIRM_TOOL = 4
self.HOW_LONG = 5
self.CLOSING = 6
self.WANT_RETURN = 7
self.CONFIRM_TOOL_RETURN = 8
self.AVAILABILITY_QUESTION = 9
self.SEND_LIST = 10
```

Additionally, our conversation handling works through “dumb” searching for keywords in user messages.  It does not (yet) use machine learning.  That’d be a pretty good idea though.  Currently, when parsing for words, we look for: checkout words, return words, closing words, availability words (asking if a tool is available), and help words.

When adding to these word lists, keep in mind that the bot looks for that word anywhere in the user message, so choose them with care.  For example, at an earlier point in the project, we included the word “in” as an availability word, for the case of a user asking “is the camera in?”  The problem this presents is that it would see “in” in other words as well (for example, “I am checking out a camera”), which would be misinterpreted because the word “checking” also contains the word “in”.

The `determine_response_for_user` function is the main part of this, and follows a mostly predictable structure.  It’s pretty much a list of if statements that determine a response based on user stage.  There are a couple important exceptions.
The end of that function should never be reached, and if it is, it’s a bug.  It should be structured in a way that it returns before ever getting to the end of the function.

The first chunk of the function is structured differently.  It looks like this (pseudo-code):

```
if the message is a closing:
    Return a farewell

if the message is asking for help:
    Return a help resource

if the user stage is SEND_LIST
    If the message is “view more” then return a response
    Otherwise, don’t return because it needs to be treated like NO_CONTACT

if the user stage is NO_CONTACT
    Check for return words and set user stage
    Check for availability words and return response
    Check for checkout words and set user stage
    Else, return that we don’t understand

// other if-checks for user stages begin here
```

The reason for this is that people should always be able to exit the conversation (closing words) or ask for help, no matter their stage.  Thus, these checks come before anything else.

The `SEND_LIST` check needs to be above `NO_CONTACT`.  The user is in this stage if they just got sent the list of available tools with the “view more” button.  If they click that button, we handle that here.  But if they send a different message instead, we need to be able to handle that like a new conversation.  Hence setting the user stage to `NO_CONTACT` so that the message gets handled by the appropriate block.

In `NO_CONTACT`, some parts of it set the user stage, such as identifying that the user wants to return or check out, so that it can be handled by the appropriate code block.  Other parts of it send a return message, if the message doesn’t require a stage change for the user.

Basically, the ordering of these is very intentional so that a user can flow through if-blocks as appropriate, and checks come in the proper order.

### Making Additions

Making additions to Loan Wrangler's conversational abilities mostly happens in the above `determine_response_for_user` function.  For example, let’s say we want to make a message path where if a user sends the word “olin” then Loan Wranger will only respond to further messages with the word “olin”.  It stops when a user says one of the default stop commands, of course.
First, we would add a check to the `NO_CONTACT` if-block that changes the user stage if we see the start word “olin”:

```
# checking out
elif any(word in message for word in self.checkout_words):
    user['stage'] = self.WANT_CHECKOUT
    print(user['stage'])

# NEW CODE HERE:
elif “olin” in message:
    user[‘stage’] = self.OLIN
# END NEW CODE

else:
    # send greeting and ask what tool
    response = "😄 Hi there! I'm Loan Wrangler, what can I help you with?"
    return user, response, None
```

This also requires us to define the new user stage in the constructor:

```python
self.CONFIRM_TOOL_RETURN = 8
self.AVAILABILITY_QUESTION = 9
self.SEND_LIST = 10
self.OLIN = 11 # NEW CODE
```

Finally, we make an if-statement in the rest of the function call, for handling messages when the user is in the new stage:

```python
if user['stage'] == self.OLIN:
    return user, "olin", None
```

Now Loan Wrangler would return the response "olin" to anything it was sent (except a stop word to end the conversation).

If we wanted to make a better addition, this function might actually do some handling of the message received.
The structure of the return block is very specific; it returns a 3-part tuple:

1. The user variable, which was passed into this function.  It may have been updated over the course of running (such as updating its stage) so it needs to be passed back so it can be saved.
2. The response string that should be send to the user in the chat window.
3. The quickreply options.  This should either be `None` if no quickreply options are available, or a list of strings that represents the list of quickreply options.

### Future Work

- Expand tests.  Right now, testing coverage is low, and the most important functionalities to test (the `if` structure flow of the `conversationHandler`) are not being tested at all.  A good test suite might be some kind of matrix of responses and user stages, and testing that a given message begets a given response, depending on the user’s stage.  Part of this would also include getting our Travis CI up again, and actually using it as an evaluator of our app.
- Refactor.  It’s not a great structure to rely so heavily on placement of code, the way that having some `if` statements before others is crucial or it breaks the code.  This could probably be done better.
- Integrate with TIND.  Right now we’re pulling a tools list from TIND to populate our database, but that just parses XML, and only gets run when we execute it manually.  All the transactions occur solely in our database.  We should integrate with TIND’s self-check API so that the transactions are part of the library system.
- Security.  There are no checks as to whether a user is a member of the Olin community.  This should happen, through TIND users or another method.

## Operator

If you are an Olin user working on the project for Olin, you can contact Anne LoVerso or Mimi Kome to get the app secrets, which are required for changing the Heroku deployment.

If you are outside Olin looking to adapt the project, you will need to create your own Facebook app and secrets.
[Creating a Facebook app is well documented](https://developers.facebook.com/docs/messenger-platform/guides/quick-start)

The deployment workflow uses Heroku. The Heroku account is dependent on our Mongo database. To replace this or use your own, initialize a new database via `python3 create_tools_from_tind.py`.

The app needs access to the following environment variables:

- `validationToken` is a Facebook variable that confirms for Facebook that you own the app that you say you own.  You can set this to anything
- `serverURL` is the link to your hosted webapp; for us, heroku
- `pageAccessToken` is generated by Facebook for your page
- `mongo_uri` is a [MongoDB connection string URI](https://docs.mongodb.com/manual/reference/connection-string/).
- `tind_access_token` will be needed to make Tind API requests.  This is not currently used.

Loan Wrangler also relies on our Facebook page and its Messenger integration, which can be managed from the Facebook developers dashboard.  Both the Library Facebook account Lib Guru and Anne are admins of this page and can make changes.
The Facebook page is not yet approved for public messaging, which means that in order for the bot to respond to a given user, they need to be listed as a Developer, Tester, or Administrator role on the Facebook developer app site.  When the app is public, this won’t be necessary.  To make it public just submit an application for review on the Developer dashboard after making sure you’ve followed Facebook’s checkboxes, such as uploading a photo.

# Attribution

Code written by [Anne LoVerso](http://anneloverso.com) and Mimi Kome.  Help from Oliver Steele, Jeff Goldenson, and Emily Ferrier.  Thanks to the rest of the Hacking the Library class.

# License

MIT License
