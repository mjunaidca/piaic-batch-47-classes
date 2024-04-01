# poetry install --no-root  
# poetry run python hello.py

from sqlmodel import SQLModel, Field, create_engine, Session, select

# Add your neon.tech Database URL
DATABASE_URL: str = "postgresql://todo_owner:ipgcEC0fJd4s@ep-old-block-a5y75062.us-east-2.aws.neon.tech/sql?sslmode=require"

class Students(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str


engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

def create_students():
    student1 = Students(name="Ahmed")
    student2 = Students(name="Ali")

    print("Student1:", student1)
    print("Student2:", student2)

    # Add the students to the database
    session : Session = Session(engine)
    session.add(student1)
    session.add(student2)

    session.commit()

    session.refresh(student1)
    session.refresh(student2)

    print("Student1:", student1)
    print("Student2:", student2)


create_students()

def get_all_students():
    session = Session(engine)

    query = select(Students)
    all_students = session.exec(query).all()

    print("all_students", all_students)

get_all_students()
