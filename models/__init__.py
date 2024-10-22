#!/usr/bin/python3
"""
initialize the models package
"""

# storage_t = getenv("MATHS_TYPE_STORAGE")
storage_t = "db"
print("The file storage type is: %s" % storage_t)
if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
db = storage
storage.reload()
