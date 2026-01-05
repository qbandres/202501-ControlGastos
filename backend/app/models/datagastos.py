from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.connection import Base

class MetodoPago(enum.Enum):
    EFECTIVO = "Efectivo"
    TARJETA_CREDITO = "Tarjeta de Crédito"
    TARJETA_DEBITO = "Tarjeta de Débito"
    TRANSFERENCIA = "Transferencia"
    OTROS = "Otros"

class TipoGasto(enum.Enum):
    FIJO = "Fijo"
    VARIABLE = "Variable"
    HORMIGA = "Hormiga"
    IMPREVISTO = "Imprevisto"

class ControlGastos(Base):
    __tablename__ = 'control_gastos'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relación con Usuario
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref="gastos")
    
    clase = Column(String(30), nullable=False)
    asignacion = Column(String(30), nullable=False)
    
    # Cambio de Float a Numeric para precisión financiera
    cantidad = Column(Numeric(10, 2), nullable=False)
    
    # Uso de Enums para evitar texto libre
    tipo = Column(Enum(TipoGasto), nullable=False)
    metodo = Column(Enum(MetodoPago), nullable=False, default=MetodoPago.EFECTIVO)
    
    locacion = Column(String(30), nullable=False)
    fecha = Column(Date, nullable=False)
    observaciones = Column(Text, nullable=True)
    
    # Timestamps
    f_ingreso = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())