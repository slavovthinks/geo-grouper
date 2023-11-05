import io
from csv import DictReader

from fastapi import UploadFile, HTTPException

from geo_grouper.models import User


async def load_users_from_csv(file: UploadFile) -> list[User]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    content = await file.read()
    content = io.StringIO(content.decode('utf-8-sig'))

    dict_reader = DictReader(content)
    dict_reader.fieldnames = [fieldname.lower() for fieldname in dict_reader.fieldnames]
    return [User(**user) for user in list(dict_reader)]

