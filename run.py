from flask import Flask, jsonify, render_template, request, redirect, url_for
import pymysql
from app.database import get_db_connection

app = Flask(__name__)

# RUTA 1: La página web visual para la tienda
@app.route("/tienda")
def ver_tienda():
    conn = get_db_connection()
    mensaje = request.args.get("msg", None)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.id_producto, p.nombre_producto, p.precio_detallista, c.nombre_categoria
                FROM producto p
                INNER JOIN categorias c ON p.fk_id_categoria = c.id_categoria
                WHERE p.estado_visibilidad = TRUE;
            """
            cursor.execute(sql)
            productos = cursor.fetchall()
        return render_template("tienda.html", productos=productos, mensaje=mensaje)
    finally:
        conn.close()

# RUTA 2: Acción de comprar (aquí se pone a prueba el Trigger)
@app.route("/comprar", methods=["POST"])
def procesar_compra():
    id_variante = int(request.form.get("id_variante", 1))
    cantidad = int(request.form.get("cantidad", 1))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Crear una cabecera de pedido rápido para la clienta (usuario 1)
            cursor.execute("INSERT INTO pedido (fk_id_usuario, total_pedido) VALUES (1, %s);", (cantidad * 120000.00,))
            id_pedido = cursor.lastrowid
            
            # 2. Insertar detalle (Aquí el trigger actúa: descuenta stock o revienta si no hay)
            cursor.execute("""
                INSERT INTO detalle_pedido (fk_id_pedido, fk_id_variante, cantidad, precio)
                VALUES (%s, %s, %s, %s);
            """, (id_pedido, id_variante, cantidad, 120000.00))
            
        conn.commit()
        return redirect(url_for('ver_tienda', msg=f"¡Compra confirmada! Pedido #{id_pedido} registrado con éxito."))
        
    except pymysql.MySQLError as e:
        conn.rollback()
        # Si el trigger bloqueó la venta:
        return redirect(url_for('ver_tienda', msg=f"Error al procesar: {e.args[1]}"))
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)