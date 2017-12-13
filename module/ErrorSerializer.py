def Response(req, resp, exception):
    resp.body = exception.to_json()
    resp.content_type = 'application/json'
    resp.append_header('Vary', 'Accept')
