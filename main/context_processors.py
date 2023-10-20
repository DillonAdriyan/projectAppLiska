def greeting(request):
    username = request.session.get('username', None)
    print("Username:", username)
    data = {
        'username': username,
    }
    return data
