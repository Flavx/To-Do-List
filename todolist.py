from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

today = datetime.today()


class Tasky:
    def __init__(self):
        self.menu = "1) Today's tasks\n" \
                    "2) Week's tasks\n" \
                    "3) All tasks\n" \
                    "4) Past tasks\n" \
                    "5) Add task\n" \
                    "6) Delete past tasks\n" \
                    "7) Delete future tasks\n" \
                    "0) Exit"

    def today(self):
        rows = session.query(Table).filter(Table.deadline == today.date()).order_by(Table.deadline).all()
        if not rows:
            print(f"\nToday {today.strftime('%d')} {today.strftime('%b')}\n"
                  f"Nothing to do!\n")
        else:
            print(f"\nToday {today.strftime('%d')} {today.strftime('%b')}")
            for item, lst in enumerate(rows, start=1):
                print(f"{item}. {lst}")
        print()

    def weeky(self):
        day_plus = timedelta(days=1)
        current_week = today.date() + timedelta(days=7)
        week_count = today.date()
        while week_count <= current_week:
            rows = session.query(Table).filter(Table.deadline == week_count).order_by(Table.deadline).all()
            print(f"\n{week_count.strftime('%A')} {week_count.day} {week_count.strftime('%b')}")
            if not rows:
                print("Nothing to do!")
                week_count += day_plus
            else:
                count = 1
                for row in rows:
                    print(f"{count}. {row.task}.")
                    count += 1
                week_count += day_plus
        print()

    def all(self):
        rows = session.query(Table).all()
        if not rows:
            print(f"\nNothing to do!\n")
        else:
            rows = session.query(Table).order_by(Table.deadline).all()
            count = 1
            print("\nAll Tasks:")
            for row in rows:
                print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                count += 1
            print()

    def add(self):
        enter_task = input("Enter Task\n")
        enter_deadline = input("Enter deadline\n")
        y, m, d = enter_deadline.split(sep="-")
        new_row = Table(task=enter_task, deadline=datetime(int(y), int(m), int(d)))
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")

    def past(self):
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if not rows:
            print(f"\nNothing is missed!\n")
        else:
            count = 1
            print("\nPast Tasks:")
            for row in rows:
                print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                count += 1
            print()

    def to_delete_past(self):
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if not rows:
            print(f"\nNothing to delete!\n")
        else:
            count = 1
            print("\nChoose the number of the task you want to delete:")
            for row in rows:
                print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                count += 1
            print()
            selected = int(input()) - 1
            deleting = rows[selected]
            session.delete(deleting)
            session.commit()

    def to_delete_future(self):
        rows = session.query(Table).filter(Table.deadline > today).order_by(Table.deadline).all()
        if not rows:
            print(f"\nNothing to delete!\n")
        else:
            count = 1
            print("\nChoose the number of the task you want to delete:")
            for row in rows:
                print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                count += 1
            print()
            selected = int(input()) - 1
            deleting = rows[selected]
            session.delete(deleting)
            session.commit()


tasky = Tasky()

while True:
    Session = sessionmaker(bind=engine)
    session = Session()
    print(tasky.menu)
    choice = int(input(">"))
    if choice == 1:
        tasky.today()
    elif choice == 2:
        tasky.weeky()
    elif choice == 3:
        tasky.all()
    elif choice == 4:
        tasky.past()
    elif choice == 5:
        tasky.add()
    elif choice == 6:
        tasky.to_delete_past()
    elif choice == 7:
        tasky.to_delete_future()
    elif choice == 0:
        print("\nBye!")
        break
