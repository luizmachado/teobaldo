from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.security import security
from app.tools import user_service
from app.schemas.user import Token

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Retorna um token de acesso se as credenciais forem válidas. """
    user = user_service.get_user_by_document(documento=form_data.username)

    # A regra de negócio é que a senha é o próprio documento.
    if not user or not security.verify_password(form_data.password, user.documento):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect document or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": user.documento}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
