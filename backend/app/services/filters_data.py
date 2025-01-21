from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.datagastos import ControlGastos

def apply_filters(query, filters):
    """
    Aplica filtros dinámicos a la consulta SQLAlchemy.

    Args:
        query: La consulta SQLAlchemy base.
        filters: Diccionario con los filtros aplicados.

    Returns:
        query: La consulta con los filtros aplicados.
    """
    try:
        # Filtros de igualdad exacta
        if "usuario" in filters and filters["usuario"]:
            query = query.filter(ControlGastos.usuario == filters["usuario"])
        if "clase" in filters and filters["clase"]:
            query = query.filter(ControlGastos.clase == filters["clase"])

        # Filtros de inclusión (IN)
        if "clase_in" in filters and filters["clase_in"]:
            query = query.filter(ControlGastos.clase.in_(filters["clase_in"]))

        # Filtros de rango (Fechas y Cantidad)
        if "rango_fecha_inicio" in filters and "rango_fecha_fin" in filters:
            if filters["rango_fecha_inicio"] and filters["rango_fecha_fin"]:
                query = query.filter(
                    ControlGastos.fecha.between(filters["rango_fecha_inicio"], filters["rango_fecha_fin"])
                )
        if "rango_cantidad_min" in filters and filters["rango_cantidad_min"] is not None:
            query = query.filter(ControlGastos.cantidad >= float(filters["rango_cantidad_min"]))
        if "rango_cantidad_max" in filters and filters["rango_cantidad_max"] is not None:
            query = query.filter(ControlGastos.cantidad <= filters["rango_cantidad_max"])

        # Filtro parcial (LIKE)
        if "usuario_like" in filters and filters["usuario_like"]:
            query = query.filter(ControlGastos.usuario.ilike(f"%{filters['usuario_like']}%"))

        # Ordenamiento
        if "ordenar_por" in filters and "orden" in filters:
            ordenar_campo = getattr(ControlGastos, filters["ordenar_por"], None)
            if ordenar_campo:
                query = query.order_by(
                    ordenar_campo.desc() if filters["orden"] == "desc" else ordenar_campo.asc()
                )

        return query
    except Exception as e:
        print("Error en apply_filters:", str(e))
        raise