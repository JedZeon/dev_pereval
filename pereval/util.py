def get_path_upload_photo(instance, file):
    return f'photos/passes_{instance.pereval.id}/{file}'
