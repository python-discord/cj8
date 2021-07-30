from .DBWorker import DatabaseWorker
from .models import Base

Base.metadata.create_all(DatabaseWorker.engine)
