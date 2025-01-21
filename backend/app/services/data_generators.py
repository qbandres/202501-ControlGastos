from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.datagastos import ControlGastos

def generate_xy_data(db: Session, x_column: str, y_column: str):
    """
    Genera datos para gráficos x-y basados en las columnas especificadas.

    Args:
        db (Session): Sesión de la base de datos.
        x_column (str): Nombre de la columna para el eje x.
        y_column (str): Nombre de la columna para el eje y.

    Returns:
        list: Lista de diccionarios con los valores x-y.
    """
    query = db.query(
        getattr(ControlGastos, x_column).label("x"),
        func.sum(getattr(ControlGastos, y_column)).label("y")
    ).group_by(getattr(ControlGastos, x_column)).order_by(getattr(ControlGastos, x_column))

    results = query.all()
    return [{"x": row.x, "y": row.y} for row in results]

def generate_xyy_data(db: Session, x_column: str, y1_column: str, y2_column: str):
    """
    Genera datos para gráficos x-y1-y2 basados en las columnas especificadas.

    Args:
        db (Session): Sesión de la base de datos.
        x_column (str): Nombre de la columna para el eje x.
        y1_column (str): Nombre de la primera columna para el eje y1.
        y2_column (str): Nombre de la segunda columna para el eje y2.

    Returns:
        list: Lista de diccionarios con los valores x-y1-y2.
    """
    query = db.query(
        getattr(ControlGastos, x_column).label("x"),
        func.sum(getattr(ControlGastos, y1_column)).label("y1"),
        func.sum(getattr(ControlGastos, y2_column)).label("y2")
    ).group_by(getattr(ControlGastos, x_column)).order_by(getattr(ControlGastos, x_column))

    results = query.all()
    return [{"x": row.x, "y1": row.y1, "y2": row.y2} for row in results]