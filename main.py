'''
Beschreibung:
1. Starte Server im Terminal: uvicorn main:app --reload
2. Öffne im Browser:   http://127.0.0.1:8000/docs
3. Klicke rechts neben GET auf den Schlüssel und gebe die Zugangsdaten für Login und Passwort ( bosch, bosch )
4. Suchbegriff unter GET eingeben und mit Execute ausführen
'''


from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import FastAPI, Depends, HTTPException, status
from googlesearch import search
from jose import jwt

app = FastAPI()

# Authorisierung mit OAuth2
@app.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    if data.username == "bosch" and data.password == "bosch":
        access_token = jwt.encode({"user": data.username}, key="secret")
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Die Zugangsdaten sind nicht korrekt!",
        headers={"WWW-Authenticate": "Bearer"},
    )

# Abfrage von Suchbegriffen mit der Bedingung, dass Authorisierung erfolgreich war.
@app.get("/{keyword}", dependencies=[Depends(OAuth2PasswordBearer(tokenUrl="login"))])
async def searchThis(keyword):
    urlList = []
    for foundThisURL in search(keyword,
                    tld='com',
                    lang='en',
                    num=10,
                    stop=10,
                    pause=2.0):
        urlList.append({"URL": foundThisURL})
    return urlList


