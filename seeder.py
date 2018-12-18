from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatItem, User

engine = create_engine('sqlite:///catalog.db')
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
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category for SOCCER
cat = Category(user_id=1, name="Soccer")

session.add(cat)
session.commit()
catItem = CatItem(user_id=1, name="Ball", description="""The Fair Trade Certified, Valor Match Soccer Ball made with a durable textured cover,
 similar to those used in top-level match soccer balls. Patented ‘DuoTech’ construction combines increased performance and durability.
  It features a reinforced bladder for extended air retention and complies with FIFA Quality Pro Match Standards. 
  All Senda balls are Fair Trade Certified, ensuring ball producers meet social, economic and environmental criteria. 
  This includes guaranteeing all workers in the supply chain receive at least the national minimum wage, that there is no child labor
   involved in production and that the health and safety of workers is safeguarded. Senda's mission is to make high-quality.""", category=cat)

session.add(catItem)
session.commit()

catItem2 = CatItem(user_id=1, name="Soccer Goal", description="""The SKLZ Quickster Goal is perfect for pick up games. The ultra-portable quick and easy set up frame allows you the freedom to train daily, without the hassle. """, category=cat)

session.add(catItem2)
session.commit()


# Category for basket baal
cat2 = Category(user_id=1, name="BasketBall")

session.add(cat2)
session.commit()
catItem = CatItem(user_id=1, name="Basketball Hoop", description=""" 44" Impact backboard is virtually unbreakable.
Telescoping mechanism adjusts from 7.5 to 10-Feet 6-Inch increments
27-Gallon base fills with water or sand and rolls to your desired location
All-weather resistant, deigned to withstand the harshest elements.""", category=cat2)

session.add(catItem)
session.commit()

catItem2 = CatItem(user_id=1, name="Scoreboard", description=""" Recommended for indoor use
Wireless remote for scoring and clock adjustments
Scores basketball, wrestling, volleyball, boxing and more
Use as a metronome, stopwatch, clock with alarm and program timer
Counts up or down from 99:99 and keeps score to 199 """, category=cat2)

session.add(catItem2)
session.commit()

# Category for Gymnastices 
cat3 = Category(user_id=1, name="Gymnastices")

session.add(cat3)
session.commit()
catItem = CatItem(user_id=1, name="Exercise Mat", description=""" EASY TO CARRY - Tri-fold design is compact for storage, and two carrying handles makes fitness on-the-go convenient
THICK CUSHION - Provides a cushioned, supportive surface for workouts, stretch-ing, martial Arts, or outdoor fitness routines
JOINT PROTECTION - Resilient foam interior keeps its shape for long-term usability, and protects knees, wrists, elbows & back
DURABLE - Vinyl surface resists tearing or stretching and is easy to wipe clean; great for stretching & floor exercises.""", category=cat3)

session.add(catItem)
session.commit()

catItem2 = CatItem(user_id=1, name="Kip Bar", description=""" STRONG: Safe sturdy pro level design, can accommodate up to 140lbs, no extension pieces or stabilizers necessary.
ADJUSTABLE: The gymnastics bar can go as low as 35” (3ft) and as high as 57” (4.75ft) with 10 intervals in between.
EASY: Assembly is simple with clear instructions and tools included.
BONUS: Comes with cool sticker pack that can be used to decorate and personalize the bar.""", category=cat3)

session.add(catItem2)
session.commit()
print ("added category items!")