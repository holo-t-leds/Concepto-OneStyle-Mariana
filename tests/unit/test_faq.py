# tests/unit/test_faq.py
import pytest
from src.faq.service import FAQService

def test_creacion_y_listado_publico_faq():
    service = FAQService()
    fid = service.crear_faq("¿Cómo compro?", "Selecciona prendas y confirma por WhatsApp.", 1, 1, "admin")
    
    publicas = service.obtener_faqs_publicas()
    assert len(publicas) == 1
    assert publicas[0]["pregunta"] == "¿Cómo compro?"
    assert publicas[0]["categoria"] == "Envíos y Entregas"

def test_baja_logica_oculta_de_vista_publica():
    service = FAQService()
    fid = service.crear_faq("¿Puedo pagar con Nequi?", "Sí, aceptamos Nequi.", 2, 1, "admin")
    
    # Desactivar pregunta (RF-FAQ-008)
    service.cambiar_estado(fid, "inactivo", "admin")
    
    # En vista pública no debe aparecer
    assert len(service.obtener_faqs_publicas()) == 0
    # En panel administrativo sí debe existir
    assert len(service.listar_todas_admin()) == 1

def test_busqueda_dinamica_palabra_clave():
    service = FAQService()
    service.crear_faq("Tiempos de entrega", "Tardamos entre 2 y 4 días hábiles.", 1, 1, "admin")
    service.crear_faq("Costos de envío", "El envío cuesta $10.000.", 1, 2, "admin")

    coincidencias = service.buscar_faqs("hábiles")
    assert len(coincidencias) == 1
    assert coincidencias[0]["pregunta"] == "Tiempos de entrega"

def test_enlace_soporte_whatsapp():
    service = FAQService()
    url = service.generar_enlace_soporte_whatsapp()
    assert "https://api.whatsapp.com/send?phone=" in url
    assert "OneStyle" in url