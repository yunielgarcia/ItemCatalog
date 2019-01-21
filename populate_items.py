from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Item, User, Base

# engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com")
session.add(User1)
session.commit()

# Working Categories
Soccer = Category(name="Soccer")
Basketball = Category(name="Basketball")
Baseball = Category(name="Baseball")
Frisbee = Category(name="Frisbee")
Snowboarding = Category(name="Snowboarding")
RockClimbing = Category(name="Rock Climbing")
Skating = Category(name="Skating")
Hockey = Category(name="Hockey")

session.add(Soccer)
session.commit()
session.add(Basketball)
session.commit()
session.add(Baseball)
session.commit()
session.add(Frisbee)
session.commit()
session.add(Snowboarding)
session.commit()
session.add(RockClimbing)
session.commit()
session.add(Skating)
session.commit()
session.add(Hockey)
session.commit()


# Items

catalog_item1 = Item(user_id=1, category_id=1,
                     name="Shinguards",
                     description=(
                         "Protect your lower legs with soccer shin guards"
                         " and sleeves from Academy Sports + Outdoors when"
                         " you're playing on the pitch."))
catalog_item2 = Item(user_id=1, category_id=3,
                     name="Bate",
                     description=("So, using a heavier bat should result"
                                  " in faster hit balls, which means the"
                                  " hit ball will travel farther"))

# Adding items
session.add(catalog_item1)
session.commit()
session.add(catalog_item2)
session.commit()


print "added items!"
