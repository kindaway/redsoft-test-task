from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import registry

from src.domain.exclusion_poll.entity import ExclusionPoll
from src.domain.friend.entity import Friend
from src.domain.house.entity import House
from src.domain.message.entity import Message
from src.domain.user.entity import User

metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

mapper_registry = registry()

houses = Table(
    "houses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("apartments_count", Integer),
    Column("apartments_per_floor", Integer),
    Column("entrances_count", Integer),
    Column("floors_count", Integer),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(63)),
    Column("last_name", String(63)),
    Column("patronymic", String(63)),
    Column("house_number", ForeignKey("houses.id")),
    Column("apartment_number", Integer),
)

messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("from_id", ForeignKey("users.id")),
    Column("to_id", ForeignKey("users.id")),
    Column("text", Text),
)

friend_pairs = Table(
    "friend_pairs",
    metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("friend_id", ForeignKey("users.id"), primary_key=True)
)

exclusion_polls = Table(
    "exclusion_polls",
    metadata,
    Column("exclusion_candidate_id", ForeignKey("users.id"), primary_key=True),
    Column("votes", Integer),
    Column("votes_required", Integer),
    Column("reason", Text)
)


def map_domain():
    mapper_registry.map_imperatively(House, houses)
    mapper_registry.map_imperatively(User, users)
    mapper_registry.map_imperatively(Friend, friend_pairs)
    mapper_registry.map_imperatively(Message, messages)
    mapper_registry.map_imperatively(ExclusionPoll, exclusion_polls)
