# src/auditoria/service.py
from datetime import datetime

class AuditoriaService:
    def __init__(self):
        self.logs = []
        self.log_id_counter = 1

    def registrar_traza_auditoria(self, usuario_id: int, tipo_accion: str, tabla_afectada: str,
                                  registro_id: int, valor_anterior: str = None, valor_nuevo: str = None):
        log = {
            'id': self.log_id_counter,
            'usuario_id': usuario_id,
            'tipo_accion': tipo_accion,
            'tabla_afectada': tabla_afectada,
            'registro_id': registro_id,
            'valor_anterior': valor_anterior,
            'valor_nuevo': valor_nuevo,
            'fecha': datetime.now()
        }
        self.logs.append(log)
        self.log_id_counter += 1
        return log['id']
