import streamlit as st
from consultas import ver_clientes, ver_productos, ingreso_total, promedio_venta, ventas_por_cliente
from clientes import agregar_cliente
from productos import agregar_producto
from ventas import crear_venta, agregar_detalle, obtener_total_venta, obtener_boleta, exportar_boleta_pdf
from graficos import grafico_ventas_por_cliente

st.title("📊 Sistema de Ventas PRO")

menu = st.sidebar.selectbox(
    "Menú",
    [
        "Dashboard",
        "Clientes",
        "Productos",
        "Ventas",
        "Boleta"
    ]
)

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.title("📊 Dashboard PRO - Sistema de Ventas")

    from consultas import ventas_hoy, top_productos, top_clientes, ultimas_ventas

    # ================= KPIs =================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Ventas hoy", ventas_hoy())

    with col2:
        st.metric("📈 Ingreso total", ingreso_total())

    with col3:
        st.metric("📊 Promedio venta", promedio_venta())

    with col4:
        st.metric("🧾 Total ventas", len(ventas_por_cliente()))

    st.divider()

    # ================= GRÁFICO =================
    st.subheader("📊 Ventas por cliente")
    grafico_ventas_por_cliente()

    st.divider()

    # ================= TOP PRODUCTOS =================
    st.subheader("📦 Top 5 productos")
    data = top_productos()
    st.table(data)

    # ================= TOP CLIENTES =================
    st.subheader("👥 Top 5 clientes")
    st.table(top_clientes())

    # ================= ÚLTIMAS VENTAS =================
    st.subheader("🧾 Últimas ventas")
    st.table(ultimas_ventas())

# ================= CLIENTES =================
elif menu == "Clientes":
    st.subheader("👥 Gestión de Clientes")

    with st.form("form_cliente"):
        nombre = st.text_input("Nombre del cliente")
        ciudad = st.text_input("Ciudad")
        enviar = st.form_submit_button("Agregar cliente")

        if enviar:
            agregar_cliente(nombre, ciudad)
            st.success("Cliente agregado correctamente ✅")

    st.dataframe(ver_clientes())

# ================= PRODUCTOS =================
elif menu == "Productos":
    st.subheader("📦 Gestión de Productos")

    with st.form("form_producto"):
        nombre = st.text_input("Nombre producto")
        precio = st.number_input("Precio", min_value=0)
        enviar = st.form_submit_button("Agregar producto")

        if enviar:
            agregar_producto(nombre, precio)
            st.success("Producto agregado correctamente ✅")

    st.dataframe(ver_clientos := ver_productos())

# ================= VENTAS =================
elif menu == "Ventas":
    st.subheader("🧾 Crear Venta (Carrito PRO)")

    clientes = ver_clientes()
    productos = ver_productos()

    # ================= CLIENTE =================
    cliente_dict = {c[1]: c[0] for c in clientes}  # nombre -> id

    cliente_nombre = st.selectbox(
        "👤 Cliente",
        list(cliente_dict.keys())
    )

    cliente_id = cliente_dict[cliente_nombre]

    # ================= CARRITO =================
    if "carrito" not in st.session_state:
        st.session_state.carrito = []

    # ================= PRODUCTO =================
    producto_dict = {p[1]: (p[0], p[2]) for p in productos}  
    # nombre -> (id, precio)

    producto_nombre = st.selectbox(
        "📦 Producto",
        list(producto_dict.keys())
    )

    producto_id, precio = producto_dict[producto_nombre]

    cantidad = st.number_input("Cantidad", min_value=1, value=1)

    fecha = st.date_input("Fecha")

    # ================= AGREGAR =================
    if st.button("➕ Agregar al carrito"):
        st.session_state.carrito.append(
            (producto_nombre, precio, cantidad, precio * cantidad)
        )
        st.success("Producto agregado al carrito")

    # ================= RESUMEN =================
    st.subheader("🛒 Carrito")

    total = 0

    for item in st.session_state.carrito:
        nombre, precio, cant, subtotal = item
        st.write(f"{nombre} x{cant} = ${subtotal}")
        total += subtotal

    st.divider()
    st.write(f"💰 TOTAL: ${total}")

    # ================= FINALIZAR =================
    if st.button("✅ Finalizar venta"):
        if len(st.session_state.carrito) == 0:
            st.warning("El carrito está vacío")
        else:
            from ventas import crear_venta, agregar_detalle

            fecha_str = fecha.strftime("%Y-%m-%d")
            venta_id = crear_venta(cliente_id, fecha_str)

            for item in st.session_state.carrito:
                nombre, precio, cant, subtotal = item
                producto_id = producto_dict[nombre][0]
                agregar_detalle(venta_id, producto_id, cant)

            st.success(f"Venta creada correctamente 💰 Total: {total}")
            st.session_state.carrito = []

# ================= BOLETA =================
elif menu == "Boleta":
    st.title("🧾 Boleta de compra")

    venta_id = st.number_input("ID de venta", min_value=1)

    if st.button("Generar boleta"):
        datos = obtener_boleta(venta_id)

        if not datos:
            st.warning("No existe esa venta")
        else:
            total = 0

            st.write("### 🧾 Detalle de compra")

            for nombre, cant, precio, subtotal in datos:
                st.write(f"{nombre} x{cant} = ${subtotal}")
                total += subtotal

            st.success(f"💰 TOTAL: ${total}")

            # 🔥 EXPORTAR PDF
            archivo = exportar_boleta_pdf(venta_id, datos, total)

            with open(archivo, "rb") as f:
                st.download_button(
                    label="📥 Descargar boleta PDF",
                    data=f,
                    file_name=archivo,
                    mime="application/pdf"
                )