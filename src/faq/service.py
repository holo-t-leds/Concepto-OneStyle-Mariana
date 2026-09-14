# src/faq/service.py
import urllib.parse
from datetime import datetime
from typing import List, Dict, Optional

class FAQService:
    def __init__(self):
        # Emulación de tablas de base de datos
        self.categorias = {
            1: {"id_categoria": 1, "nombre": "Envíos y Entregas", "estado": "activo"},
            2: {"id_categoria": 2, "nombre": "Medios de Pago", "estado": "activo"},
            3: {"id_categoria": 3, "nombre": "Cambios y Devoluciones", "estado": "activo"},
        }
        self.faqs = {}  # id_faq: dict con datos de la pregunta
        self.faq_id_counter = 1

        # Configuración del canal oficial de soporte (RF-FAQ-011)
        self.config_soporte = {
            "tipo": "WhatsApp",
            "telefono": "573001234567",
            "mensaje_predeterminado": "Hola, tengo una consulta sobre OneStyle Mariana que no encontré en las preguntas frecuentes.",
            "estado": "activo"
        }

    # -------------------------------------------------------------------------
    # Flujo Público (RF-FAQ-001, RF-FAQ-002, RF-FAQ-003, RF-FAQ-004)
    # -------------------------------------------------------------------------

    def obtener_faqs_publicas(self) -> List[Dict]:
        """
        Retorna únicamente preguntas con estado 'activo' agrupadas por orden y categoría.
        RF-FAQ-001, RF-FAQ-002.
        """
        resultado = []
        for faq in self.faqs.values():
            cat = self.categorias.get(faq["id_categoria"])
            if faq["estado"] == "activo" and cat and cat["estado"] == "activo":
                resultado.append({
                    "id_faq": faq["id_faq"],
                    "pregunta": faq["pregunta"],
                    "respuesta": faq["respuesta"],
                    "categoria": cat["nombre"],
                    "orden": faq["orden"]
                })
        # Ordenar por orden configurado (RF-FAQ-010)
        return sorted(resultado, key=lambda x: x["orden"])

    def buscar_faqs(self, termino: str) -> List[Dict]:
        """
        Búsqueda por palabra clave insensible a mayúsculas/minúsculas.
        Filtra sobre pregunta y respuesta (RF-FAQ-004).
        """
        if not termino or not termino.strip():
            return self.obtener_faqs_publicas()

        t_clean = termino.strip().lower()
        publicas = self.obtener_faqs_publicas()

        coincidencias = [
            faq for faq in publicas
            if t_clean in faq["pregunta"].lower() or t_clean in faq["respuesta"].lower()
        ]
        return coincidencias

    def generar_enlace_soporte_whatsapp(self, mensaje_personalizado: Optional[str] = None) -> str:
        """
        Genera la URL del Click-to-Chat hacia el canal oficial de soporte.
        RF-FAQ-011.
        """
        if self.config_soporte.get("estado") != "activo":
            raise ValueError("El canal de soporte no está disponible actualmente.")

        tel = self.config_soporte["telefono"]
        msg = mensaje_personalizado or self.config_soporte["mensaje_predeterminado"]
        msg_encoded = urllib.parse.quote(msg)

        return f"https://api.whatsapp.com/send?phone={tel}&text={msg_encoded}"

    # -------------------------------------------------------------------------
    # Flujo Administrativo (RF-FAQ-005, RF-FAQ-006, RF-FAQ-007, RF-FAQ-008, 009, 010)
    # -------------------------------------------------------------------------

    def crear_faq(self, pregunta: str, respuesta: str, id_categoria: int, orden: int, usuario_creador: str) -> int:
        """
        Registra una nueva pregunta frecuente validando categoría y orden único.
        RF-FAQ-005, RF-FAQ-010.
        """
        if not pregunta.strip() or not respuesta.strip():
            raise ValueError("La pregunta y la respuesta no pueden estar vacías.")

        if id_categoria not in self.categorias:
            raise ValueError("La categoría temática especificada no existe.")

        if orden <= 0:
            raise ValueError("El orden debe ser un número entero positivo.")

        # Validar orden único dentro de la misma categoría temática
        for faq in self.faqs.values():
            if faq["id_categoria"] == id_categoria and faq["orden"] == orden:
                raise ValueError(f"Ya existe una pregunta con el orden {orden} en esta categoría.")

        faq_id = self.faq_id_counter
        self.faqs[faq_id] = {
            "id_faq": faq_id,
            "pregunta": pregunta.strip(),
            "respuesta": respuesta.strip(),
            "id_categoria": id_categoria,
            "orden": orden,
            "estado": "activo",
            "fecha_creacion": datetime.now(),
            "usuario_creacion": usuario_creador,
            "fecha_actualizacion": datetime.now(),
            "usuario_actualizacion": usuario_creador
        }
        self.faq_id_counter += 1
        return faq_id

    def actualizar_faq(self, id_faq: int, pregunta: str, respuesta: str, id_categoria: int, orden: int, usuario_editor: str) -> bool:
        """
        Modifica el contenido, categoría y orden de una pregunta existente.
        RF-FAQ-007.
        """
        if id_faq not in self.faqs:
            raise ValueError("La pregunta frecuente no existe.")

        if not pregunta.strip() or not respuesta.strip():
            raise ValueError("La pregunta y respuesta son obligatorias.")

        if id_categoria not in self.categorias:
            raise ValueError("Categoría inválida.")

        # Validar colisión de orden con otra pregunta de la misma categoría
        for fid, faq in self.faqs.items():
            if fid != id_faq and faq["id_categoria"] == id_categoria and faq["orden"] == orden:
                raise ValueError(f"El orden {orden} ya está ocupado por otra pregunta en esta categoría.")

        item = self.faqs[id_faq]
        item.update({
            "pregunta": pregunta.strip(),
            "respuesta": respuesta.strip(),
            "id_categoria": id_categoria,
            "orden": orden,
            "fecha_actualizacion": datetime.now(),
            "usuario_actualizacion": usuario_editor
        })
        return True

    def cambiar_estado(self, id_faq: int, nuevo_estado: str, usuario_editor: str) -> bool:
        """
        Implementa la baja lógica ('inactivo') y la reactivación ('activo').
        RF-FAQ-008, RF-FAQ-009.
        """
        if id_faq not in self.faqs:
            raise ValueError("La pregunta frecuente no existe.")

        if nuevo_estado not in ["activo", "inactivo"]:
            raise ValueError("Estado no válido. Use 'activo' o 'inactivo'.")

        self.faqs[id_faq]["estado"] = nuevo_estado
        self.faqs[id_faq]["fecha_actualizacion"] = datetime.now()
        self.faqs[id_faq]["usuario_actualizacion"] = usuario_editor
        return True

    def listar_todas_admin(self) -> List[Dict]:
        """
        Lista preguntas activas e inactivas para el panel de administración.
        RF-FAQ-006.
        """
        return list(self.faqs.values())