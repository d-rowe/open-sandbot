def get_endpoint(path: str, resource: str):
    return "/{}/{}".format(path, resource)


def get_api_endpoint(path: str, resource: str):
    return get_endpoint("api/{}".format(path), resource)
