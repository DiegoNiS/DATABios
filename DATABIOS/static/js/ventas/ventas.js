document.getElementById('crear-excel').addEventListener('click', () => {
    $('#detalleVentaModal').modal('show');
});

document.getElementById('crear-excel').addEventListener('click', () => {
    const primeraVentaId = document.querySelector('#ventas-table-body tr:first-child .ver-detalle').getAttribute('data-venta-id');
    
    fetch(`/ventas/detalle/${primeraVentaId}/`)
        .then(response => response.json())
        .then(data => {
            // Mostrar datos en el modal de detalle de venta
            document.getElementById('ventaId').textContent = data.venta.id;
            document.getElementById('fechaCreacion').textContent = data.venta.fecha_creacion;
            document.getElementById('nombreVendedor').textContent = data.venta.vendedor.username;

            // Mostrar detalles de productos
            const detalleProductosBody = document.getElementById('detalleProductosBody');
            detalleProductosBody.innerHTML = '';
            data.productos.forEach((producto, index) => {
                const row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.precio_unitario}</td>
                        <td>${producto.unidades}</td>
                        <td>${producto.importe}</td>
                    </tr>
                `;
                detalleProductosBody.innerHTML += row;
            });

            // Mostrar importe total
            document.getElementById('importeTotal').textContent = data.total;

            // Mostrar modal de detalle de venta
            $('#detalleVentaModal').modal('show');

            // Manejo de descarga de Excel dentro del modal de detalles
            document.getElementById('descargar-excel').addEventListener('click', () => {
                fetch('/ventas/crear_excel/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'ventas.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert('Archivo Excel creado con éxito.');
                })
                .catch(() => alert('Error al crear el archivo Excel.'));
            });
        });
});



// Filtrado de ventas
document.getElementById('filtrar').addEventListener('click', () => {
    const fecha = document.getElementById('fecha-filtro').value;
    const vendedorId = document.getElementById('vendedor-filtro').value;
    const url = new URL(window.location.href);
    url.searchParams.set('fecha', fecha);
    url.searchParams.set('vendedor', vendedorId);
    window.location.href = url.href;
});

// Agregar venta
document.getElementById('agregar-venta').addEventListener('click', () => {
    $('#agregarVentaModal').modal('show');
});

document.getElementById('agregar-producto').addEventListener('click', () => {
    const productoId = document.getElementById('producto-select').value;
    const unidades = document.getElementById('unidades-input').value;

    fetch('/ventas/agregar/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            producto_id: productoId,
            unidades: unidades,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Venta agregada con éxito.');
            window.location.reload();
        } else {
            alert('Error al agregar la venta.');
        }
    });
});

// Eliminación de venta
document.querySelectorAll('.eliminar-venta').forEach(button => {
    button.addEventListener('click', () => {
        const ventaId = button.getAttribute('data-venta-id');
        $('#confirmarEliminacionModal').modal('show');

        document.getElementById('confirmar-eliminacion').addEventListener('click', () => {
            const reabastecer = document.getElementById('reabastecerStock').checked;

            fetch(`/ventas/eliminar/${ventaId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    reabastecer: reabastecer,
                }),
            })
            .then(response => {
                if (response.ok) {
                    alert('Venta eliminada con éxito.');
                    window.location.reload();
                } else {
                    alert('Error al eliminar la venta.');
                }
            });
        });
    });
});

// Obtener CSRF token de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
