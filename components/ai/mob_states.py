from enum import Enum, auto


class MobState(Enum):

    # The mob will walk around the room
    LOITERING = auto()

    # The mob is currently transfering to another room
    TRANSFERRING = auto()

    # TODO add more
