from fastapi import status, HTTPException
from src.utils import Hash, get_field_or_404
from src.schemas.users import UserSchema
from src.server.database import db
from email_validator import validate_email, EmailNotValidError


async def create_user(user: UserSchema):

#Verifica se email é válido
    try:
        new_account = True
        validation = validate_email(user.email, check_deliverability=new_account)
        user.email = validation.email
        print("3")

    except EmailNotValidError as e:
        print(str(e)) 

#Verifica se email já existe
    user_db = await get_user_by_email(user.email)
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="message': 'Email already registered")

#Verifica se senha é válida
    print("4")
    len_password = 3
    if len_password > len(user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="message': 'Password not valid")

    user = await db.users_db.insert_one(user.dict()) # insere no db

#Verifica ObjectId
    if user.inserted_id:
        user = await get_field_or_404(user.inserted_id, db.users_db, 'user')
        return user
        

async def get_user_by_email(user_email):
    try:
        user = await db.users_db.find_one({'email': user_email})
        if user:
            print('iogiu')
            return user

    except Exception as e:
         print(f"get_user.error: {e}")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

