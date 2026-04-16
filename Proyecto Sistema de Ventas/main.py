from clientes import agregar_cliente
from productos import agregar_producto
from ventas import crear_venta, agregar_detalle, imprimir_boleta
from consultas import ver_clientes, ver_productos, ver_ventas, ventas_por_cliente, productos_mas_vendidos, ingreso_total, promedio_venta, mejor_cliente, producto_estrella
from graficos import grafico_ventas_por_cliente, grafico_productos

while True:
    print("\n===== SISTEMA DE VENTAS =====")
    print("1. Agregar cliente")
    print("2. Agregar producto")
    print("3. Crear venta")
    print("4. Salir")
    print("5. Ver clientes")
    print("6. Ver productos")
    print("7. Ver ventas")
    print("8. Ventas por cliente")
    print("9. Productos más vendidos")
    print("10. Gráfico ventas por cliente")
    print("11. Gráfico productos más vendidos")
    print("12. Imprimir boleta")
    print("13. Ingreso total")
    print("14. Promedio por venta")
    print("15. Mejor cliente")
    print("16. Producto estrella")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        nombre = input("Nombre cliente: ")
        ciudad = input("Ciudad: ")
        agregar_cliente(nombre, ciudad)

    elif opcion == "2":
        nombre = input("Nombre producto: ")
        precio = float(input("Precio: "))
        agregar_producto(nombre, precio)

    elif opcion == "3":
        cliente_id = int(input("ID cliente: "))
        fecha = input("Fecha (YYYY-MM-DD): ")

        venta_id = crear_venta(cliente_id, fecha)

        while True:
            producto_id = int(input("ID producto (0 para terminar): "))
            if producto_id == 0:
                break
            cantidad = int(input("Cantidad: "))
            agregar_detalle(venta_id, producto_id, cantidad)

        from ventas import obtener_total_venta
        total = obtener_total_venta(venta_id)

        print("\n🧾 Venta registrada completa ✅")
        print(f"💰 Total de la venta: {total}")

    elif opcion == "4":
        print("Saliendo...")
        break

    elif opcion == "5":
        ver_clientes()

    elif opcion == "6":
        ver_productos()

    elif opcion == "7":
        ver_ventas()

    elif opcion == "8":
        ventas_por_cliente()

    elif opcion == "9":
        productos_mas_vendidos()

    elif opcion == "10":
        grafico_ventas_por_cliente()

    elif opcion == "11":
        grafico_productos()

    elif opcion == "12":
        venta_id = int(input("ID de la venta: "))
        imprimir_boleta(venta_id)

    elif opcion == "13":
        print("💰 Ingreso total:", ingreso_total())

    elif opcion == "14":
        print("📈 Promedio por venta:", promedio_venta())

    elif opcion == "15":
        cliente = mejor_cliente()
        print(f"🏆 Mejor cliente: {cliente[0]} -> {cliente[1]}")

    elif opcion == "16":
        producto = producto_estrella()
        print(f"📦 Producto estrella: {producto[0]} -> {producto[1]}")

    else:
        print("Opción inválida")

