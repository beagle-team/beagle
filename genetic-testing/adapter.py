import string
import random


class UserAction(object):

    def __init__(self, action_type, values):
        self.action_type = action_type
        self.values = values

    def __repr__(self):
        return "<{}: {}>".format(self.action_type, self.values)

    @staticmethod
    def random_action():
        actions = [
            UserClick.random_action,
            # UserScroll.random_action,
            UserType.random_action,
            # UserWait.random_action,
        ]

        action = actions[random.randint(0, len(actions)-1)]()

        return action


class UserClick(UserAction):

    def __init__(self, values):
        self.action_type = 'click'
        self.values = values

    def append_to_action_chain(self, action_chain):
        action_chain.move_by_offset(self.values[0], self.values[1])
        action_chain.click()
        action_chain.move_by_offset(-self.values[0], -self.values[1])

    @staticmethod
    def random_action():
        x = random.randint(0, 100) * 2
        y = random.randint(0, 100) * 2
        return UserClick([x, y])


class UserScroll(UserAction):

    def __init__(self, values):
        self.action_type = 'scroll'
        self.values = values

    def append_to_action_chain(self, action_chain):
        return
        # TODO: implement
        # action_chain.scroll(self.values[0], self.values[1])

    @staticmethod
    def random_action():
        x = random.randint(0, 100) * 10
        y = random.randint(0, 100) * 10
        return UserScroll([x, y])


class UserType(UserAction):

    def __init__(self, values):
        self.action_type = 'type'
        self.values = values

    def append_to_action_chain(self, action_chain):
        action_chain.send_keys(self.values)

    @staticmethod
    def random_action():
        min_char = 1
        max_char = 100
        all_char = string.ascii_letters + string.punctuation + string.digits
        value = "".join(random.choice(all_char) for x in range(random.randint(min_char, max_char)))
        return UserType(value)


class UserWait(UserAction):

    def __init__(self, values):
        self.action_type = 'wait'
        self.values = values

    def append_to_action_chain(self, action_chain):
        action_chain.pause(self.values)

    @staticmethod
    def random_action():
        amount = random.random() * 2  # TODO: Da dimensionare
        return UserWait(amount)
