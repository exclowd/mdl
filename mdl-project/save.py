import datetime
import os

import numpy as np
from sqlalchemy import Column, Float, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

sql_file = os.path.join(os.path.dirname(__file__), 'data0.db')
engine = create_engine(f"sqlite:///{sql_file}")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    vector_0 = Column(Float)
    vector_1 = Column(Float)
    vector_2 = Column(Float)
    vector_3 = Column(Float)
    vector_4 = Column(Float)
    vector_5 = Column(Float)
    vector_6 = Column(Float)
    vector_7 = Column(Float)
    vector_8 = Column(Float)
    vector_9 = Column(Float)
    vector_10 = Column(Float)
    mse_train = Column(Float)
    mse_test = Column(Float)


Base.metadata.create_all(engine)


def exists(vector: np.array):
    return session.query(Data).filter(
        Data.vector_0 == vector[0],
        Data.vector_1 == vector[1],
        Data.vector_2 == vector[2],
        Data.vector_3 == vector[3],
        Data.vector_4 == vector[4],
        Data.vector_5 == vector[5],
        Data.vector_6 == vector[6],
        Data.vector_7 == vector[7],
        Data.vector_8 == vector[8],
        Data.vector_9 == vector[9],
        Data.vector_10 == vector[10]
    ).count() > 0


def score(vector: np.array):
    for vec in session.query(Data).filter(
            Data.vector_0 == vector[0],
            Data.vector_1 == vector[1],
            Data.vector_2 == vector[2],
            Data.vector_3 == vector[3],
            Data.vector_4 == vector[4],
            Data.vector_5 == vector[5],
            Data.vector_6 == vector[6],
            Data.vector_7 == vector[7],
            Data.vector_8 == vector[8],
            Data.vector_9 == vector[9],
            Data.vector_10 == vector[10]
    ):
        return np.array([vec.mse_train, vec.mse_test])


def get_id(vector: np.array):
    for vec in session.query(Data).filter(
            Data.vector_0 == vector[0],
            Data.vector_1 == vector[1],
            Data.vector_2 == vector[2],
            Data.vector_3 == vector[3],
            Data.vector_4 == vector[4],
            Data.vector_5 == vector[5],
            Data.vector_6 == vector[6],
            Data.vector_7 == vector[7],
            Data.vector_8 == vector[8],
            Data.vector_9 == vector[9],
            Data.vector_10 == vector[10]
    ):
        return vec.id


def get_from_id(id: int):
    vec = session.query(Data).filter(Data.id == id).first()
    if vec is not None:
        return np.array(
            [vec.vector_0, vec.vector_1, vec.vector_2, vec.vector_3, vec.vector_4, vec.vector_5, vec.vector_6,
             vec.vector_7, vec.vector_8, vec.vector_9, vec.vector_10, ]), np.array([vec.mse_train, vec.mse_test])


def get_all():
    expr = '[' + ', '.join([f'vec.vector_{it}' for it in range(11)]) + ']'
    for vec in session.query(Data):
        yield np.array(eval(expr))


def add(vector: np.array, mse: np.array):
    if exists(vector):
        return
    data = Data(
        vector_0=vector[0],
        vector_1=vector[1],
        vector_2=vector[2],
        vector_3=vector[3],
        vector_4=vector[4],
        vector_5=vector[5],
        vector_6=vector[6],
        vector_7=vector[7],
        vector_8=vector[8],
        vector_9=vector[9],
        vector_10=vector[10],
        mse_train=mse[0],
        mse_test=mse[1]
    )
    session.add(data)
    session.commit()


if __name__ == '__main__':
    vv = [0.7380669852589472, 0.08711817134358402, 0.6854319818859647, 0.7361535029129077, 0.04557160491584822,
          0.5792219272811107, 0.8776476150614081, 0.5264880634321608, 0.04007212170185781, 0.542912651380285,
          0.004214886703377996]
    print(score(vv))

# df = pd.read_csv('data.csv')
# data_dict = {
#     'timestamp': datetime.now(),
#     'vector': arr,
#     'mse': mse
# }
# df2 = pd.DataFrame.from_dict(data_dict, orient='index')
# df2.transpose()
# df2.to_csv('data.csv', mode='a', header=False)
