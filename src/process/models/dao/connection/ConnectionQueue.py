from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.connection.ConnectionQueueBase import ConnectionQueueBase
from models.dao.Entity import Entity


class ConnectionQueue(ConnectionQueueBase,Entity, IocManager.Base):
    __tablename__ = "ConnectionQueue"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    Protocol = Column(String(100), index=False, unique=False, nullable=True)
    Mechanism = Column(String(100), index=False, unique=False, nullable=True)
    ConnectorType = relationship("ConnectorType", back_populates="Queues")
