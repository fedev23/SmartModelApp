def validate_params(required_params, provided_params):
    """Valida que todos los parámetros requeridos estén presentes."""
    missing_params = [param for param in required_params if not provided_params.get(param)]
    if missing_params:
        return {"error": f"Missing required parameters: {', '.join(missing_params)}"}
    return None
