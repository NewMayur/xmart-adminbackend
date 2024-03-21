def response_base(
    message: str = "Success",
    status: int = 200,
    data: list = None,
):
    resp = {
        "message": message,
        "status": status,
        "data": data,
    }

    return resp, status
