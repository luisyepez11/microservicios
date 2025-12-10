from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, ForeignKey, DateTime, desc, asc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import List, Optional
import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

# cargar variables de entorno
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()

# obtener configuracion de la base de datos
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
JWT_SECRET = os.getenv("JWT_SECRET")
SAL_ENCRYPT = os.getenv("SAL_ENCRYPT")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin123!")

# obtener configuracion de Resend
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@db:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#configuracion de seguridad
security = HTTPBearer()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# configuracion JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# token contenedor de todos los datos del usuario
def create_access_token(user_data: dict):
    to_encode = user_data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# extraer los datos del token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    user_data = {
        "id_usuario": payload.get("id_usuario"),
        "correo_usuario": payload.get("correo_usuario"),
        "fecha_creacion": payload.get("fecha_creacion"),
        "ultima_conexion": payload.get("ultima_conexion"),
        "permisos": payload.get("permisos", [])
    }
    
    if not user_data["id_usuario"]:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return user_data

#modelos
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    correo_usuario = Column(String, unique=True, nullable=False)
    contraseña_usuario = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultima_conexion = Column(DateTime, nullable=True)  

class Permiso(Base):
    __tablename__ = "permisos"
    
    id_permiso = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_permiso = Column(String, unique=True, nullable=False)

class PermisoUsuario(Base):
    __tablename__ = "permisos_usuario"
    
    id_permiso_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    id_permiso = Column(UUID(as_uuid=True), ForeignKey("permisos.id_permiso"))

class HistorialUsuario(Base):
    __tablename__ = "historial_usuario"
    
    id_historial_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False)
    descripcion_operacion = Column(String, nullable=False) 
    fecha_operacion = Column(DateTime, default=datetime.utcnow, nullable=False)


def crear_permisos_por_defecto(db: Session):
    """Crea los permisos por defecto con UUIDs fijos y válidos"""
    try:
        permisos_por_defecto = [
            {
                "id": uuid.UUID("11111111-1111-1111-1111-111111111111"),
                "nombre": "vista_productos"
            },
            {
                "id": uuid.UUID("22222222-2222-2222-2222-222222222222"), 
                "nombre": "modificacion_productos"
            },
            {
                "id": uuid.UUID("33333333-3333-3333-3333-333333333333"),
                "nombre": "vista_stock"
            },
            {
                "id": uuid.UUID("44444444-4444-4444-4444-444444444444"),
                "nombre": "modificacion_stock"
            },
            {
                "id": uuid.UUID("55555555-5555-5555-5555-555555555555"),
                "nombre": "manejo_usuarios"
            }
        ]
        
        permisos_creados = 0
        
        for permiso_data in permisos_por_defecto:
            permiso_existente = db.query(Permiso).filter(
                Permiso.nombre_permiso == permiso_data["nombre"]
            ).first()
            
            if not permiso_existente:
                nuevo_permiso = Permiso(
                    id_permiso=permiso_data["id"],
                    nombre_permiso=permiso_data["nombre"]
                )
                db.add(nuevo_permiso)
                permisos_creados += 1
        
        db.commit()
            
    except Exception as e:
        db.rollback()
        raise
    
def crear_usuario_admin_por_defecto(db: Session):
    """Crea un usuario administrador con todos los permisos si no existe"""
    try:
        usuario_admin = db.query(Usuario).filter(
            Usuario.correo_usuario == ADMIN_EMAIL
        ).first()
        
        if usuario_admin:
            print(f"Usuario administrador ya existe: {ADMIN_EMAIL}")
            return
        
        print(f"Creando usuario administrador por defecto: {ADMIN_EMAIL}")
        
        # Crear el usuario administrador
        usuario_admin = Usuario(
            correo_usuario=ADMIN_EMAIL,
            contraseña_usuario=get_password_hash(ADMIN_PASSWORD),
            fecha_creacion=datetime.utcnow()
        )
        
        db.add(usuario_admin)
        db.commit()
        db.refresh(usuario_admin)
        
        # Obtener todos los permisos existentes
        permisos = db.query(Permiso).all()
        
        # Asignar todos los permisos al administrador
        for permiso in permisos:
            permiso_usuario = PermisoUsuario(
                id_usuario=usuario_admin.id_usuario,
                id_permiso=permiso.id_permiso
            )
            db.add(permiso_usuario)
            print(f"   + Permiso asignado: {permiso.nombre_permiso}")
        
        db.commit()
        
        print(f"Usuario administrador creado exitosamente")
        print(f"Email: {ADMIN_EMAIL}")
        print(f"Contraseña: {ADMIN_PASSWORD}")
        
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario administrador: {str(e)}")
        raise

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    try:
        crear_permisos_por_defecto(db)
        crear_usuario_admin_por_defecto(db) 
    except Exception as e:
        print(f"Error durante la inicialización: {str(e)}")

#esquemas

class UsuarioCreate(BaseModel):
    correo_usuario: str = Field(..., min_length=5, max_length=100)
    contraseña_usuario: str = Field(..., min_length=6) 

    @field_validator('correo_usuario')
    @classmethod
    def validar_email_basico(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('El correo debe contener @')
        return v

    @field_validator('contraseña_usuario')
    @classmethod
    def validar_contraseña_fuerte(cls, v: str) -> str:
        if v.isnumeric():
            raise ValueError('La contraseña no puede ser solo números')
        if v.isalpha():
            raise ValueError('La contraseña debe contener números y letras')
        return v

class UsuarioResponse(BaseModel):
    id_usuario: uuid.UUID
    correo_usuario: str
    fecha_creacion: datetime
    ultima_conexion: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }

class PermisoCreate(BaseModel):
    nombre_permiso: str = Field(..., min_length=2, max_length=50)

class PermisoResponse(BaseModel):
    id_permiso: uuid.UUID
    nombre_permiso: str
    
    model_config = {
        "from_attributes": True
    }

class PermisoUsuarioCreate(BaseModel):
    id_usuario: uuid.UUID
    id_permiso: uuid.UUID

class PermisoUsuarioDelete(BaseModel):
    id_usuario: uuid.UUID
    id_permiso: uuid.UUID

class PermisoUsuarioResponse(BaseModel):
    id_permiso_usuario: uuid.UUID
    id_usuario: uuid.UUID
    id_permiso: uuid.UUID
    
    model_config = {
        "from_attributes": True
    }

class LoginData(BaseModel):
    correo_usuario: str
    contraseña_usuario: str

class PermisoEnPerfil(BaseModel):
    id_permiso: uuid.UUID
    nombre_permiso: str
    
    model_config = {
        "from_attributes": True
    }

class PerfilResponse(BaseModel):
    id_usuario: uuid.UUID
    correo_usuario: str
    fecha_creacion: datetime
    ultima_conexion: Optional[datetime] = None 
    permisos: List[PermisoEnPerfil] = []
    
    model_config = {
        "from_attributes": True
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: PerfilResponse

class EmailVerificacionRequest(BaseModel):
    correo_usuario: EmailStr
    codigo_verificacion: str

class EmailVerificacionResponse(BaseModel):
    mensaje: str
    correo_enviado: bool
    correo_destino: str

class HistorialUsuarioCreate(BaseModel):
    id_usuario: uuid.UUID
    descripcion_operacion: str = Field(..., min_length=2, max_length=500)

class HistorialUsuarioUpdate(BaseModel):
    descripcion_operacion: str = Field(..., min_length=2, max_length=500)

class HistorialUsuarioResponse(BaseModel):
    id_historial_usuario: uuid.UUID
    id_usuario: uuid.UUID
    descripcion_operacion: str
    fecha_operacion: datetime
    
    model_config = {
        "from_attributes": True
    }


def obtener_permisos_usuario(db: Session, usuario_id: uuid.UUID) -> List[PermisoEnPerfil]:
    """
    Obtener todos los permisos de un usuario específico
    """
    permisos = db.query(Permiso).join(
        PermisoUsuario, Permiso.id_permiso == PermisoUsuario.id_permiso
    ).filter(
        PermisoUsuario.id_usuario == usuario_id
    ).all()
    
    permisos_response = []
    for permiso in permisos:
        permisos_response.append(PermisoEnPerfil(
            id_permiso=permiso.id_permiso,
            nombre_permiso=permiso.nombre_permiso
        ))
    
    return permisos_response

def preparar_datos_usuario_para_token(usuario: Usuario, permisos: List[PermisoEnPerfil]) -> dict:
    """
    Prepara todos los datos del usuario para incluirlos en el token JWT
    """
    permisos_serializables = []
    for permiso in permisos:
        permisos_serializables.append({
            "id_permiso": str(permiso.id_permiso),
            "nombre_permiso": permiso.nombre_permiso
        })
    
    datos_usuario = {
        "id_usuario": str(usuario.id_usuario),
        "correo_usuario": usuario.correo_usuario,
        "fecha_creacion": usuario.fecha_creacion.isoformat(),
        "ultima_conexion": usuario.ultima_conexion.isoformat() if usuario.ultima_conexion else None,
        "permisos": permisos_serializables
    }
    
    return datos_usuario

def verificar_permiso(current_user: dict, permiso_requerido: str) -> bool:
    """Verifica si el usuario tiene un permiso específico"""
    return any(
        permiso.get("nombre_permiso") == permiso_requerido 
        for permiso in current_user["permisos"]
    )

def registrar_operacion_historial(
    db: Session, 
    usuario_id: uuid.UUID, 
    descripcion: str
) -> bool:
    """
    Función auxiliar para registrar una operación en el historial
    """
    try:
        nueva_entrada = HistorialUsuario(
            id_usuario=usuario_id,
            descripcion_operacion=descripcion
        )
        db.add(nueva_entrada)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al registrar operación en historial: {str(e)}")
        return False

def actualizar_ultima_conexion_usuario(db: Session, usuario_id: uuid.UUID, razon: str = "Actividad en el sistema"):
    """
    Función auxiliar para actualizar la última conexión de un usuario
    """
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        if usuario:
            usuario.ultima_conexion = datetime.utcnow()
            db.commit()
            
            registrar_operacion_historial(
                db, 
                usuario_id, 
                f"Última conexión actualizada: {razon}"
            )
            
            return True
        return False
    except Exception as e:
        print(f"Error al actualizar última conexión: {str(e)}")
        return False

# funcion para enviar correo con el codigo por n8n
async def enviar_codigo_verificacion_resend(destinatario: str, codigo_verificacion: str) -> bool:
    try:
        html_content = f"""
        <html>
        <body>
            <h1>Código de Verificación</h1>
            <p>Tu código de verificación es: <strong>{codigo_verificacion}</strong></p>
            <p>Ingresa este código en la página de verificación para continuar.</p>
            <p>Si no solicitaste este código, ignora este mensaje.</p>
        </body>
        </html>
        """
        
        data = {
            "correo": destinatario,
            "codigo": codigo_verificacion
        }
        
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://lyepez23.app.n8n.cloud/webhook/affb8262-d277-4e32-95b2-79ed4dc24e63",
                json=data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                print(f"Email con código de verificación enviado exitosamente a {destinatario}")
                return True
            else:
                print(f"Error enviando email: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        print(f"Excepción enviando email: {str(e)}")
        return False
    
# crear tablas
Base.metadata.create_all(bind=engine)

# ENDPOINTS
@app.get("/", tags=["Lógica de Usuarios"])
def root():
    return {"mensaje": "API de Gestión de Usuarios y Permisos", "estado": "activo"}
    
# LOGIN 
@app.post("/login", response_model=TokenResponse, tags=["Lógica de Usuarios"])
def login(login_data: LoginData, db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener token JWT con TODOS los datos del usuario
    """
    try:
        # buscar usuario por correo
        usuario = db.query(Usuario).filter(
            Usuario.correo_usuario == login_data.correo_usuario
        ).first()
        
        if not usuario:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        # verificar contraseña
        if not verify_password(login_data.contraseña_usuario, usuario.contraseña_usuario):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        # actualizar última conexión
        usuario.ultima_conexion = datetime.utcnow()
        db.commit()
        db.refresh(usuario)
        
        # registrar en el historial
        registrar_operacion_historial(
            db, 
            usuario.id_usuario, 
            "Inició sesión en el sistema"
        )
        
        # obtener permisos del usuario
        permisos = obtener_permisos_usuario(db, usuario.id_usuario)
        datos_usuario_token = preparar_datos_usuario_para_token(usuario, permisos)
        
        # crear token con los datos del usuario
        access_token = create_access_token(datos_usuario_token)
        
        perfil_completo = PerfilResponse(
            id_usuario=usuario.id_usuario,
            correo_usuario=usuario.correo_usuario,
            fecha_creacion=usuario.fecha_creacion,
            ultima_conexion=usuario.ultima_conexion,
            permisos=permisos
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": perfil_completo
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el login: {str(e)}")
    
# ENDPOINTS DE ÚLTIMA CONEXIÓN
@app.put("/actualizar-ultima-conexion", response_model=UsuarioResponse, tags=["Lógica de Usuarios"])
def actualizar_ultima_conexion(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza la última conexión del usuario autenticado
    """
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == current_user["id_usuario"]).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        usuario.ultima_conexion = datetime.utcnow()
        db.commit()
        db.refresh(usuario)
        
        registrar_operacion_historial(
            db, 
            usuario.id_usuario, 
            "Actualizó su última conexión manualmente"
        )
        
        return usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al actualizar última conexión: {str(e)}"
        )

@app.put("/usuarios/{usuario_id}/actualizar-conexion", response_model=UsuarioResponse, tags=["Lógica de Usuarios"])
def actualizar_conexion_usuario(
    usuario_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar la última conexión de cualquier usuario (solo administradores)
    """
    try:
        if not verificar_permiso(current_user, "manejo_usuarios"):
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para actualizar conexiones de otros usuarios"
            )
        
        # Buscar el usuario
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        usuario.ultima_conexion = datetime.utcnow()
        db.commit()
        db.refresh(usuario)
        
        registrar_operacion_historial(
            db, 
            usuario.id_usuario, 
            f"Última conexión actualizada por administrador ({current_user['correo_usuario']})"
        )
        
        return usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al actualizar conexión del usuario: {str(e)}"
        )

# LOGOUT
@app.post("/logout", tags=["Lógica de Usuarios"])
def logout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cerrar sesión y actualizar última conexión
    """
    try:
        # Actualizar última conexión
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == current_user["id_usuario"]
        ).first()
        
        if usuario:
            usuario.ultima_conexion = datetime.utcnow()
            db.commit()
            
            registrar_operacion_historial(
                db, 
                usuario.id_usuario, 
                "Cerró sesión en el sistema"
            )
        
        return {
            "mensaje": "Sesión cerrada correctamente",
            "ultima_conexion": usuario.ultima_conexion if usuario else None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al cerrar sesión: {str(e)}"
        )

@app.get("/mi-perfil", response_model=PerfilResponse, tags=["Lógica de Usuarios"])
def obtener_mi_perfil(current_user: dict = Depends(get_current_user)):
    """
    Obtener el perfil del usuario actual con todos sus permisos DIRECTAMENTE DEL TOKEN
    """
    try:
        permisos_obj = []
        for permiso_dict in current_user["permisos"]:
            permisos_obj.append(PermisoEnPerfil(
                id_permiso=uuid.UUID(permiso_dict["id_permiso"]),
                nombre_permiso=permiso_dict["nombre_permiso"]
            ))
        
        perfil_response = PerfilResponse(
            id_usuario=uuid.UUID(current_user["id_usuario"]),
            correo_usuario=current_user["correo_usuario"],
            fecha_creacion=datetime.fromisoformat(current_user["fecha_creacion"]),
            ultima_conexion=datetime.fromisoformat(current_user.get("ultima_conexion")) 
                if current_user.get("ultima_conexion") else None,
            permisos=permisos_obj
        )
        
        return perfil_response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener el perfil: {str(e)}"
        )

#CRUD USUARIOS
@app.post("/usuarios", response_model=UsuarioResponse, tags=["Usuarios"])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario
    """
    try:
        # verificar si existe ya el correo
        usuario_existente = db.query(Usuario).filter(
            Usuario.correo_usuario == usuario.correo_usuario
        ).first()
        
        if usuario_existente:
            raise HTTPException(
                status_code=400, 
                detail="El correo ya está registrado"
            )
        
        # crear usuario con contraseña encriptada
        db_usuario = Usuario(
            correo_usuario=usuario.correo_usuario,
            contraseña_usuario=get_password_hash(usuario.contraseña_usuario)
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        registrar_operacion_historial(
            db, 
            db_usuario.id_usuario, 
            "Usuario creado en el sistema"
        )
        
        return db_usuario
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@app.get("/usuarios", response_model=list[UsuarioResponse], tags=["Usuarios"])
def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios registrados
    """
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por su ID
    """
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        if not usuario:
            raise HTTPException(
                status_code=404, 
                detail="Usuario no encontrado"
            )
            
        return usuario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(
    usuario_id: uuid.UUID, 
    usuario_actualizado: UsuarioCreate, 
    db: Session = Depends(get_db)
):
    """
    Actualizar un usuario existente
    """
    try:
        #buscar el usuario
        db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        if not db_usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # verificar si el nuevo correo ya existe en otro usuario
        if usuario_actualizado.correo_usuario != db_usuario.correo_usuario:
            correo_existente = db.query(Usuario).filter(
                Usuario.correo_usuario == usuario_actualizado.correo_usuario
            ).first()
            
            if correo_existente:
                raise HTTPException(
                    status_code=400, 
                    detail="El correo ya está en uso por otro usuario"
                )
        
        # actualizar los campos
        db_usuario.correo_usuario = usuario_actualizado.correo_usuario
        db_usuario.contraseña_usuario = get_password_hash(usuario_actualizado.contraseña_usuario)
        
        db.commit()
        db.refresh(db_usuario)
        
        registrar_operacion_historial(
            db, 
            db_usuario.id_usuario, 
            "Actualizó su información de usuario"
        )
        
        return db_usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")
    
@app.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Eliminar un usuario
    """
    try:
        # buscar el usuario
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # eliminar todas las relaciones con permisos
        relaciones_permisos = db.query(PermisoUsuario).filter(
            PermisoUsuario.id_usuario == usuario_id
        ).all()
        
        for relacion in relaciones_permisos:
            db.delete(relacion)
        
        # eliminar el usuario
        db.delete(usuario)
        db.commit()
        
        return {
            "mensaje": "Usuario eliminado correctamente",
            "usuario_id": usuario_id,
            "relaciones_eliminadas": len(relaciones_permisos)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

# ENDPOINTS DE PERMISOS
@app.post("/permisos", response_model=PermisoResponse, tags=["Permisos"])
def crear_permiso(permiso: PermisoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo permiso
    """
    try:
        permiso_existente = db.query(Permiso).filter(
            Permiso.nombre_permiso == permiso.nombre_permiso
        ).first()
        
        if permiso_existente:
            raise HTTPException(
                status_code=400, 
                detail="El permiso ya existe"
            )
        
        db_permiso = Permiso(nombre_permiso=permiso.nombre_permiso)
        db.add(db_permiso)
        db.commit()
        db.refresh(db_permiso)
        
        return db_permiso
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear permiso: {str(e)}")

@app.get("/permisos", response_model=list[PermisoResponse], tags=["Permisos"])
def obtener_permisos(db: Session = Depends(get_db)):
    """
    Obtener todos los permisos
    """
    try:
        permisos = db.query(Permiso).all()
        return permisos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener permisos: {str(e)}")

@app.get("/permisos/{permiso_id}", response_model=PermisoResponse, tags=["Permisos"])
def obtener_permiso(permiso_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Obtener un permiso específico por su ID
    """
    try:
        permiso = db.query(Permiso).filter(Permiso.id_permiso == permiso_id).first()
        
        if not permiso:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
            
        return permiso
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener permiso: {str(e)}")

@app.put("/permisos/{permiso_id}", response_model=PermisoResponse, tags=["Permisos"])
def actualizar_permiso(
    permiso_id: uuid.UUID, 
    permiso_actualizado: PermisoCreate, 
    db: Session = Depends(get_db)
):
    """
    Actualizar un permiso existente
    """
    try:
        db_permiso = db.query(Permiso).filter(Permiso.id_permiso == permiso_id).first()
        
        if not db_permiso:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
        
        if permiso_actualizado.nombre_permiso != db_permiso.nombre_permiso:
            permiso_existente = db.query(Permiso).filter(
                Permiso.nombre_permiso == permiso_actualizado.nombre_permiso
            ).first()
            
            if permiso_existente:
                raise HTTPException(
                    status_code=400, 
                    detail="El nombre del permiso ya está en uso"
                )
        
        db_permiso.nombre_permiso = permiso_actualizado.nombre_permiso
        
        db.commit()
        db.refresh(db_permiso)
        
        return db_permiso
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar permiso: {str(e)}")

@app.delete("/permisos/{permiso_id}", tags=["Permisos"])
def eliminar_permiso(permiso_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Eliminar un permiso
    """
    try:
        permiso = db.query(Permiso).filter(Permiso.id_permiso == permiso_id).first()
        
        if not permiso:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
        
        db.delete(permiso)
        db.commit()
        
        return {"mensaje": "Permiso eliminado correctamente"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar permiso: {str(e)}")

# ENDPOINTS PARA RELACIONES USUARIOS-PERMISOS
@app.post("/permisos-usuario", response_model=PermisoUsuarioResponse, tags=["Permisos-Usuarios"])
def asignar_permiso_a_usuario(permiso_usuario: PermisoUsuarioCreate, db: Session = Depends(get_db)):
    """
    Asignar un permiso a un usuario 
    """
    try:
        # verificar si el usuario existe
        usuario = db.query(Usuario).filter(Usuario.id_usuario == permiso_usuario.id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # verificar si el permiso existe
        permiso = db.query(Permiso).filter(Permiso.id_permiso == permiso_usuario.id_permiso).first()
        if not permiso:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
        
        # verificar si la relación ya existe
        relacion_existente = db.query(PermisoUsuario).filter(
            PermisoUsuario.id_usuario == permiso_usuario.id_usuario,
            PermisoUsuario.id_permiso == permiso_usuario.id_permiso
        ).first()
        
        if relacion_existente:
            raise HTTPException(status_code=400, detail="El usuario ya tiene este permiso")
        
        # crear la relación
        db_permiso_usuario = PermisoUsuario(
            id_usuario=permiso_usuario.id_usuario,
            id_permiso=permiso_usuario.id_permiso
        )
        
        db.add(db_permiso_usuario)
        db.commit()
        db.refresh(db_permiso_usuario)
        
        registrar_operacion_historial(
            db, 
            usuario.id_usuario, 
            f"Se asignó el permiso '{permiso.nombre_permiso}' al usuario"
        )
        
        return db_permiso_usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al asignar permiso: {str(e)}")

@app.delete("/permisos-usuario/", tags=["Permisos-Usuarios"])
def desvincular_permiso_de_usuario(
    id_usuario: uuid.UUID,
    id_permiso: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Desvincular un permiso de un usuario (eliminar relación) por ID de usuario y ID de permiso
    """
    try:
        # relacion entre permiso y usuario
        permiso_usuario = db.query(PermisoUsuario).filter(
            PermisoUsuario.id_usuario == id_usuario,
            PermisoUsuario.id_permiso == id_permiso
        ).first()
        
        if not permiso_usuario:
            raise HTTPException(
                status_code=404, 
                detail="No se encontró la relación entre el usuario y el permiso especificado"
            )
        
        db.delete(permiso_usuario)
        db.commit()
        
        permiso = db.query(Permiso).filter(Permiso.id_permiso == id_permiso).first()
        permiso_nombre = permiso.nombre_permiso if permiso else "permiso desconocido"
        
        registrar_operacion_historial(
            db, 
            id_usuario, 
            f"Se desvinculó el permiso '{permiso_nombre}' del usuario"
        )
        
        return {
            "mensaje": "Permiso desvinculado correctamente del usuario",
            "id_usuario": id_usuario,
            "id_permiso": id_permiso
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al desvincular permiso: {str(e)}"
        )

@app.get("/usuarios/{usuario_id}/permisos", tags=["Permisos-Usuarios"])
def obtener_permisos_de_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Obtener todos los permisos de un usuario específico
    Retorna el id de los permisos y el nombre del permiso
    """
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # obtener los permisos del usuario
        permisos = db.query(Permiso).join(
            PermisoUsuario, Permiso.id_permiso == PermisoUsuario.id_permiso
        ).filter(
            PermisoUsuario.id_usuario == usuario_id
        ).all()
        
        permisos_response = []
        for permiso in permisos:
            permisos_response.append({
                "id_permiso": permiso.id_permiso,
                "nombre_permiso": permiso.nombre_permiso
            })
        
        return {
            "usuario_id": usuario_id,
            "permisos": permisos_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener permisos del usuario: {str(e)}")
    
# EMAIL VERIFICATION
@app.post("/enviar-codigo-verificacion", response_model=EmailVerificacionResponse, tags=["Lógica de Usuarios"])
async def enviar_codigo_verificacion(
    datos: EmailVerificacionRequest,
    background_tasks: BackgroundTasks
):
    """
    Enviar codigo de verificación al usuario
    Comprobar que realmente sea su correo
    """
    try:
        # enviar el correo
        background_tasks.add_task(
            enviar_codigo_verificacion_resend, 
            datos.correo_usuario, 
            datos.codigo_verificacion
        )
        
        return {
            "mensaje": "Código de verificación enviado exitosamente",
            "correo_enviado": True,
            "correo_destino": datos.correo_usuario
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al enviar código de verificación: {str(e)}"
        )

@app.get("/historial-usuarios", response_model=list[HistorialUsuarioResponse], tags=["Historial de Usuarios"])
def obtener_todo_el_historial(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener todo el historial de todos los usuarios
    """
    try:
        # Verificar permisos
        if not verificar_permiso(current_user, "manejo_usuarios"):
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para ver el historial de usuarios"
            )
        
        historial = db.query(HistorialUsuario).all()
        return historial
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener el historial: {str(e)}"
        )

@app.get("/usuarios/{usuario_id}/historial", response_model=list[HistorialUsuarioResponse], tags=["Historial de Usuarios"])
def obtener_historial_usuario(
    usuario_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener el historial de un usuario específico por su ID
    """
    try:
        # verificar que el usuario existe
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        es_mismo_usuario = str(current_user["id_usuario"]) == str(usuario_id)
        tiene_permiso = verificar_permiso(current_user, "manejo_usuarios")
        
        if not (es_mismo_usuario or tiene_permiso):
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para ver el historial de este usuario"
            )
        
        historial = db.query(HistorialUsuario)\
            .filter(HistorialUsuario.id_usuario == usuario_id)\
            .order_by(HistorialUsuario.fecha_operacion.desc())\
            .all()
        
        return historial
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener el historial del usuario: {str(e)}"
        )

@app.post("/historial-usuarios", response_model=HistorialUsuarioResponse, tags=["Historial de Usuarios"])
def crear_entrada_historial(
    historial_data: HistorialUsuarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crear una nueva entrada en el historial de un usuario
    """
    try:
        # Verificar que el usuario existe
        usuario = db.query(Usuario).filter(Usuario.id_usuario == historial_data.id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar permisos
        es_mismo_usuario = str(current_user["id_usuario"]) == str(historial_data.id_usuario)
        tiene_permiso = verificar_permiso(current_user, "manejo_usuarios")
        
        if not (es_mismo_usuario or tiene_permiso):
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para crear entradas en el historial"
            )
        
        # Crear la entrada en el historial
        nueva_entrada = HistorialUsuario(
            id_usuario=historial_data.id_usuario,
            descripcion_operacion=historial_data.descripcion_operacion
        )
        
        db.add(nueva_entrada)
        db.commit()
        db.refresh(nueva_entrada)
        
        return nueva_entrada
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al crear la entrada en el historial: {str(e)}"
        )

@app.put("/historial-usuarios/{historial_id}", response_model=HistorialUsuarioResponse, tags=["Historial de Usuarios"])
def actualizar_entrada_historial(
    historial_id: uuid.UUID,
    historial_data: HistorialUsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar una entrada del historial por su ID
    """
    try:
        entrada_historial = db.query(HistorialUsuario)\
            .filter(HistorialUsuario.id_historial_usuario == historial_id)\
            .first()
        
        if not entrada_historial:
            raise HTTPException(status_code=404, detail="Entrada del historial no encontrada")
        
        if not verificar_permiso(current_user, "manejo_usuarios"):
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para editar el historial"
            )
        
        # Actualizar la descripción
        entrada_historial.descripcion_operacion = historial_data.descripcion_operacion
        
        db.commit()
        db.refresh(entrada_historial)
        
        # Registrar en el historial (como edición)
        registrar_operacion_historial(
            db, 
            entrada_historial.id_usuario, 
            f"Se editó una entrada del historial (ID: {historial_id})"
        )
        
        return entrada_historial
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al actualizar la entrada del historial: {str(e)}"
        )

@app.delete("/historial-usuarios/{historial_id}", tags=["Historial de Usuarios"])
def eliminar_entrada_historial(
    historial_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar una entrada del historial por su ID
    """
    try:
        entrada_historial = db.query(HistorialUsuario)\
            .filter(HistorialUsuario.id_historial_usuario == historial_id)\
            .first()
        
        if not entrada_historial:
            raise HTTPException(status_code=404, detail="Entrada del historial no encontrada")
        
        usuario_id = entrada_historial.id_usuario
        
        if not verificar_permiso(current_user, "manejo_usuarios"):
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para eliminar del historial"
            )
        
        # Eliminar la entrada
        db.delete(entrada_historial)
        db.commit()
        
        # Registrar en el historial
        registrar_operacion_historial(
            db, 
            usuario_id, 
            f"Se eliminó una entrada del historial (ID: {historial_id})"
        )
        
        return {
            "mensaje": "Entrada del historial eliminada correctamente",
            "id_historial_usuario": historial_id,
            "id_usuario": usuario_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al eliminar la entrada del historial: {str(e)}"
        )
    
