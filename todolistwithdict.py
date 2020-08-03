from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

Base = declarative_base()
global today


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())


class Tasky:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.s = sessionmaker(bind=self.engine)()
        self.menu = "1) Today's tasks\n" \
                    "2) Week's tasks\n" \
                    "3) All tasks\n" \
                    "4) Past tasks\n" \
                    "5) Add task\n" \
                    "6) Delete past tasks\n" \
                    "7) Delete future tasks\n" \
                    "0) Exit"
        self.choices = {'1': self.today, '2': self.weeky, '3': self.all,
                        '4': self.missed, '5': self.add, '6': self.to_delete_past,
                        '7': self.to_delete_future, '0': self.exit}
        self.running = True
        self.user_interface()


    def exit(self):
        print("\nBye!")
        self.running = False

    def today(self):
        global today
        today = datetime.today()
        rows = self.s.query(Table).filter(Table.deadline == today.date()).order_by(Table.deadline).all()
        print(f"\nToday {today.strftime('%d')} {today.strftime('%b')}")
        if not rows:
            print(f"Nothing to do!")
        else:
            for ind, tsk in enumerate(rows, start=1):
                print(f"{ind}. {tsk}")

    def weeky(self):
        global today
        day_plus = timedelta(days=1)
        current_week = today.date() + timedelta(days=7)
        week_count = today.date()
        while week_count <= current_week:
            rows = self.s.query(Table).filter(Table.deadline == week_count).order_by(Table.deadline).all()
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

    def all(self):
        rows = self.s.query(Table).all()
        if not rows:
            print(f"\nNothing to do!\n")
        else:
            rows = self.s.query(Table).order_by(Table.deadline).all()
            count = 1
            print("\nAll Tasks:")
            for row in rows:
                print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                count += 1

    def add(self):
        enter_task = input("Enter Task\n")
        enter_deadline = input("Enter deadline\n")
        y, m, d = enter_deadline.split(sep="-")
        new_row = Table(task=enter_task, deadline=datetime(int(y), int(m), int(d)))
        self.s.add(new_row)
        self.s.commit()
        print("The task has been added!\n")

    def missed(self):
        rows = self.s.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if not rows:
            print(f"\nNothing is missed!\n")
        else:
            count = 1
            print("\nMissed Tasks:")
            for row in rows:
                print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                count += 1

    def to_delete_past(self):
        rows = self.s.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
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
            self.s.delete(deleting)
            self.s.commit()

    def to_delete_future(self):
        global today
        rows = self.s.query(Table).filter(Table.deadline > today).order_by(Table.deadline).all()
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
            self.s.delete(deleting)
            self.s.commit()

    def user_interface(self):
        while self.running:
            print(self.menu)
            choice = input("> ")
            self.choices.get(choice, lambda: None)()
            print() if choice not in {'0', '2'} else None

Tasky('R')
