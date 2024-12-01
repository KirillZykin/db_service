from fastapi import FastAPI, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text


import database, schemas, crud
from database import engine, SessionLocal

# Создание таблиц
database.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Пароли
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Проверка авторизации
def require_auth(request: Request) -> bool:
    user = request.session.get("user")
    if user is None:
        return False
    return True

# --- Пользовательские маршруты ---
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = schemas.UserCreate(username=username, hashed_password=hashed_password, role=role)
    if crud.get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db, user)
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
def login_user(
        request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # Сохраняем пользователя в сессии
    request.session["user"] = {"id": user.id, "username": user.username, "role": user.role}
    return RedirectResponse(url="/", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def home(request: Request, is_auth: bool = Depends(require_auth)):
    if is_auth:
        user = request.session.get("user")
        if user.get("role") == "Клиент":
            views = ["Client_Race_Info", "Client_Booking_History"]
        elif user.get("role") == "Организатор":
            views = ["Organizer_Race_Schedule_Results", "Organizer_Race_Booking_Overview"]
        elif user.get("role") == "Технический персонал":
            views = ["Technical_Kart_Status_Maintenance", "Technical_Kart_Last_Race"]
        return templates.TemplateResponse("index.html", {"request": request, "user": user, "views": views})
    else:
        return RedirectResponse(url="/login", status_code=303)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/view/{view}")
def print_data(
        request: Request,
        view: str,
        db: Session = Depends(get_db),
        is_auth: bool = Depends(require_auth),
):
    if is_auth:
        # Проверяем доступность представления
        client_views = ["Client_Race_Info", "Client_Booking_History"]
        organizer_views = ["Organizer_Race_Schedule_Results", "Organizer_Race_Booking_Overview"]
        tech_views = ["Technical_Kart_Status_Maintenance", "Technical_Kart_Last_Race"]

        # Получаем текущего пользователя из сессии
        user = request.session.get("user")

        if (view not in client_views) and (user.get("role") == "Клиент"):
            raise HTTPException(status_code=404, detail="Представление не найдено или вы не имеете право")
        elif (view not in organizer_views) and (user.get("role") == "Организатор"):
            raise HTTPException(status_code=404, detail="Представление не найдено или вы не имеете право")
        elif (view not in tech_views) and (user.get("role") == "Технический персонал"):
            raise HTTPException(status_code=404, detail="Представление не найдено или вы не имеете право")

        # Выполняем запрос к представлению
        query = text(f"""SELECT * FROM {view}""")

        result = db.execute(query)

        # Динамически извлекаем названия колонок
        columns = result.keys()

        # Преобразуем результат в список словарей
        data = [dict(zip(columns, row)) for row in result.fetchall()]

        # Возвращаем данные в шаблон
        return templates.TemplateResponse(
            "data.html", {"request": request, "user": user, "data": data, "view": view, "columns": columns}
        )
    else:
        return RedirectResponse(url="/login", status_code=303)
