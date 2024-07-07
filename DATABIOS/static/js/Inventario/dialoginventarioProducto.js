document.addEventListener('DOMContentLoaded', function() {
    const editarDialog = document.getElementById('editarProductoDialog');
    const eliminarDialog = document.getElementById('eliminarProductoDialog');
    
    document.querySelectorAll('.accion_producto').forEach(select => {
        select.addEventListener('change', function(event) {
            const productoId = event.target.getAttribute('data_id');
            if (event.target.value === 'editar') {
                // Abrir diálogo de edición
                fetch(`/productos/detalle/${productoId}/`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('editarNombreProducto').value = data.nombre;
                        document.getElementById('editarStockProducto').value = data.stock;
                        document.getElementById('editarPrecioCompraProducto').value = data.precio_compra;
                        document.getElementById('editarPrecioVentaProducto').value = data.precio_venta;
                        editarDialog.showModal();
                    });
            } else if (event.target.value === 'eliminar') {
                // Abrir diálogo de eliminación
                eliminarDialog.showModal();
            }
        });
    });

    document.getElementById('cancelarEditarProducto').addEventListener('click', function() {
        editarDialog.close();
    });

    document.getElementById('cancelarEliminarProducto').addEventListener('click', function() {
        eliminarDialog.close();
    });
});
