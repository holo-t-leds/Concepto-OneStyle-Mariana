Algoritmo ValidacionStock
    Definir stockDisponible, cantidadPedida Como Entero
    
    stockDisponible <- 50 
    
    Escribir "=== CONTROL DE INVENTARIO ==="
    Escribir "Stock actual disponible: ", stockDisponible
    
    Escribir "Ingrese la cantidad que desea procesar:"
    Leer cantidadPedida
    
    Mientras cantidadPedida <= 0 O cantidadPedida > stockDisponible Hacer
        Si cantidadPedida <= 0 Entonces
            Escribir "Error: La cantidad debe ser un número positivo mayor a 0."
        Sino
            Escribir "Error: Stock insuficiente. Solo hay ", stockDisponible, " unidades disponibles."
        FinSi
        
        Escribir "Intente de nuevo. Ingrese una cantidad válida:"
        Leer cantidadPedida
    FinMientras
    
    stockDisponible <- stockDisponible - cantidadPedida
    Escribir "------------------------------------"
    Escribir "¡Operación realizada con éxito!"
    Escribir "Unidades procesadas: ", cantidadPedida
    Escribir "Nuevo stock disponible: ", stockDisponible
FinAlgoritmo