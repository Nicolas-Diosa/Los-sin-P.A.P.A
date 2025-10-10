CREATE TABLE "usuarios" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "nombre_usuario" varchar(30) UNIQUE NOT NULL,
  "email" varchar(255) UNIQUE NOT NULL,
  "contrasena" varchar(255) NOT NULL,
  "nombre" varchar(100),
  "bio" varchar(280),
  "foto_perfil" text
);

CREATE TABLE "actividades" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "id_creador" uuid NOT NULL,
  "nombre_actividad" varchar(120) NOT NULL,
  "descripcion" text,
  "categoria" varchar(40),
  "ubicacion" varchar(200),
  "lat" decimal(9,6),
  "lng" decimal(9,6),
  "fecha_hora_inicio" timestamptz NOT NULL,
  "fecha_hora_fin" timestamptz,
  "cupos" int,
  "foto_actividad" text,
  "estado" varchar(20),
  "fecha_hora_creacion" timestamptz NOT NULL DEFAULT (now()),
  "fecha_hora_actualizacion" timestamptz NOT NULL DEFAULT (now())
);

CREATE TABLE "participantes_actividad" (
  "id_actividad" uuid NOT NULL,
  "id_usuario" uuid NOT NULL,
  "hora_llegada" timestamptz,
  "hora_salida" timestamptz,
  "estado_participante" varchar(20)
);

CREATE TABLE "materias" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "id_usuario" uuid NOT NULL,
  "nombre_materia" varchar(80) NOT NULL,
  "semestre" int,
  "horario_materia" text,
  "prioridad" int,
  "estado_materia" varchar(12)
);

CREATE TABLE "eventos_calendario" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "id_usuario" uuid NOT NULL,
  "id_materia" uuid,
  "nombre_evento" varchar(120) NOT NULL,
  "fecha_hora_inicio" timestamptz NOT NULL,
  "fecha_hora_fin" timestamptz NOT NULL,
  "prioridad" int
);

CREATE TABLE "tareas" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "id_usuario" uuid NOT NULL,
  "id_materia" uuid,
  "nombre_tarea" varchar(120) NOT NULL,
  "descripcion_tarea" varchar(280),
  "prioridad" int,
  "fecha_vencimiento" timestamptz,
  "es_recurrente" boolean NOT NULL DEFAULT false,
  "recurrencia" text,
  "estado_tarea" varchar(12),
  "creacion_tarea" timestamptz NOT NULL DEFAULT (now()),
  "completada_en" timestamptz
);

CREATE TABLE "chats" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "id_actividad" uuid UNIQUE NOT NULL,
  "id_emisor" uuid NOT NULL,
  "contenido" text NOT NULL,
  "hora_creacion" timestamptz NOT NULL DEFAULT (now())
);

CREATE UNIQUE INDEX ON "participantes_actividad" ("id_actividad", "id_usuario");

CREATE INDEX ON "tareas" ("id_usuario");

CREATE INDEX ON "tareas" ("id_usuario", "estado_tarea");

CREATE INDEX ON "tareas" ("id_usuario", "fecha_vencimiento");

ALTER TABLE "actividades" ADD FOREIGN KEY ("id_creador") REFERENCES "usuarios" ("id");

ALTER TABLE "participantes_actividad" ADD FOREIGN KEY ("id_actividad") REFERENCES "actividades" ("id");

ALTER TABLE "participantes_actividad" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id");

ALTER TABLE "materias" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id");

ALTER TABLE "eventos_calendario" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id");

ALTER TABLE "eventos_calendario" ADD FOREIGN KEY ("id_materia") REFERENCES "materias" ("id");

ALTER TABLE "tareas" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id");

ALTER TABLE "tareas" ADD FOREIGN KEY ("id_materia") REFERENCES "materias" ("id");

ALTER TABLE "chats" ADD FOREIGN KEY ("id_actividad") REFERENCES "actividades" ("id");

ALTER TABLE "chats" ADD FOREIGN KEY ("id_emisor") REFERENCES "usuarios" ("id");
