from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime
from app.database.connection import Base
from datetime import datetime

class ControlGastos(Base):
    __tablename__ = 'control_gastos'
    
    id = Column(Integer, primary_key=True)
    usuario = Column(String(20), nullable=False)
    clase = Column(String(30), nullable=False)
    asignacion = Column(String(30), nullable=False)
    cantidad = Column(Float, nullable=False)
    tipo = Column(String(15), nullable=False)
    locacion = Column(String(30), nullable=False)
    fecha = Column(Date, nullable=False)
    observaciones = Column(Text, nullable=True)
    metodo = Column(String(10), nullable=False, default="Efectivo")  # Método de pago
    f_ingreso = Column(DateTime, default=datetime.utcnow)  # Fecha de ingreso