from core.Persistencia.DB_manager import DB_Manager
from core.models import Usuario


def validar_nombre_usuario(nombre: str) -> bool:
    """Nombre no vacío, mínimo 3 caracteres y debe contener al menos una letra."""
    if not nombre or len(nombre.strip()) < 3:
        return False
    if not any(c.isalpha() for c in nombre):
        return False
    return True


def validar_bio(bio: str) -> bool:
    """Bio <= 280 caracteres."""
    if bio is None:
        return True
    return len(bio) <= 280


class PerfilService:
    """Capa de negocio para editar el perfil de usuario."""

    def __init__(self):
        self.db = DB_Manager()

    def obtener_usuario(self, username: str):
        """Obtiene usuario por nombre_usuario."""
        try:
            return self.db.get_usuario_by_nombre_usuario(username)
        except Usuario.DoesNotExist:
            return None

    def editar_perfil(self, username: str, datos: dict):
        """
        datos esperados:
        {
            'nombre_usuario': 'nuevoNombre',
            'bio': 'texto aquí'
        }
        """

        usuario = self.obtener_usuario(username)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        nuevo_nombre = datos.get("nombre_usuario", "").strip()
        nueva_bio = datos.get("bio", "")

        # ---------- Validaciones ----------
        if not validar_nombre_usuario(nuevo_nombre):
            raise ValueError("El nombre de usuario no es válido.")

        if not validar_bio(nueva_bio):
            raise ValueError("La biografía supera los 280 caracteres.")

        # Validación de nombre único si cambia
        if nuevo_nombre != usuario.nombre_usuario:
            try:
                existe = self.db.get_usuario_by_nombre_usuario(nuevo_nombre)
                if existe:
                    raise ValueError("Ese nombre de usuario ya está en uso.")
            except Usuario.DoesNotExist:
                pass  # No existe → válido

        # ---------- Actualizar usando DB_Manager.update ----------
        self.db.update(
            Usuario,
            campo="id",
            valor=usuario.id,
            nombre_usuario=nuevo_nombre,
            bio=nueva_bio
        )

        return True
