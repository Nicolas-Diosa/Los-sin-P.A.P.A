Table usuarios {
  id               uuid [pk, default: `gen_random_uuid()`]
  nombre_usuario         varchar(30) [unique, not null]
  email            varchar(255) [unique, not null]
  contrasena    varchar(255) [not null]
  nombre             varchar(100)
  bio              varchar(280)
  foto_perfil       text
}


Table actividades {
  id               uuid [pk, default: `gen_random_uuid()`]
  id_creador       uuid [not null, ref: > usuarios.id]
  nombre_actividad            varchar(120) [not null]
  descripcion      text
  categoria         varchar(40) // fútbol, estudio, hiking, etc.
  ubicacion          varchar(200)
  lat              decimal(9,6)
  lng              decimal(9,6)
  fecha_hora_inicio      timestamptz [not null]
  fecha_hora_fin         timestamptz
  cupos         int
  foto_actividad        text
  estado           varchar(20) // 'Planteada' | 'Publicada' | 'Cancelada'
  fecha_hora_creacion       timestamptz [not null, default: `now()`]
  fecha_hora_actualizacion       timestamptz [not null, default: `now()`]
}


Table participantes_actividad {
  id_actividad      uuid [not null, ref: > actividades.id]
  id_usuario          uuid [not null, ref: > usuarios.id]
  hora_llegada     timestamptz
  hora_salida   timestamptz
  estado_participante     varchar(20) // 'Participante' | 'Abandonó' | 'Expulsado'
  indexes {
    (id_actividad, id_usuario) [unique]
  }
}


Table materias {
  id               uuid [pk, default: `gen_random_uuid()`]
  id_usuario        uuid [not null, ref: > usuarios.id]
  nombre_materia    varchar(80) [not null]
  semestre          int
  horario_materia   text //icalendar
  prioridad         int //Definir prioridades
  estado_materia    varchar(12) //Aprobada | Cursando | Reprobada
}




Table eventos_calendario {
  id               uuid [pk, default: `gen_random_uuid()`]
  id_usuario          uuid [not null, ref: > usuarios.id]
  id_materia       uuid [ref: > materias.id]
  nombre_evento            varchar(120) [not null]
  fecha_hora_inicio       timestamptz [not null]
  fecha_hora_fin         timestamptz [not null]
  prioridad         int //Definir prioridades
  }




Table tareas {
  id               uuid [pk, default: `gen_random_uuid()`]
  id_usuario          uuid [not null, ref: > usuarios.id]
  id_materia      uuid [ref: > materias.id]
  nombre_tarea            varchar(120) [not null]
  descripcion_tarea        varchar(280)
  prioridad         int // Definir prioridades
  fecha_vencimiento           timestamptz  //limite de tiempo
  es_recurrente     boolean [not null, default: false]
  recurrencia            text // iCalendar
  estado_tarea           varchar(12) // 'Por realizar' | 'Realizando' | 'Realizada'
  creacion_tarea       timestamptz [not null, default: `now()`]
  completada_en     timestamptz
  indexes {
    id_usuario
    (id_usuario, estado_tarea)
    (id_usuario, fecha_vencimiento)
  }
}


Table chats {
  id               uuid [pk, default: `gen_random_uuid()`]
  id_actividad      uuid [not null, unique, ref: > actividades.id]
  id_emisor        uuid [not null, ref: > usuarios.id]
  contenido          text [not null]
  hora_creacion       timestamptz [not null, default: `now()`]
  }
