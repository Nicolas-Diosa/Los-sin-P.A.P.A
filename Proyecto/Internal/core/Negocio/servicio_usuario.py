from core.Persistencia.DB_manager import DB_Manager

class ServicioUsuario:
    """
    Servicio de negocio que usa DB_Manager para obtener datos y
    devolver estructuras listas para la presentación.
    """
    def init(self):
        self.db = DB_Manager()

    def obtener_primer_usuario_dict(self):
        """Obtiene el primer usuario y lo convierte a dict (solo campos necesarios)."""
        usuario = self.db.read_primer_usuario()
        if not usuario:
            return None
        # Mapear sólo los campos que quieras mostrar
        return {
            "id": str(usuario.id) if hasattr(usuario, "id") else None,
            "nombre_usuario": usuario.nombre_usuario,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "bio": usuario.bio,
            "foto_perfil": usuario.foto_perfil,
        }

    def obtener_usuario_por_nombre(self, nombre_usuario):
        usuario = self.db.get_usuario_por_nombre(nombre_usuario)
        if not usuario:
            return None
        return {
            "id": str(usuario.id),
            "nombre_usuario": usuario.nombre_usuario,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "bio": usuario.bio,
            "foto_perfil": usuario.foto_perfil,
        }