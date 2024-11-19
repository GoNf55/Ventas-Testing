let detalles = [];
let totalVenta = 0;

document.getElementById('add-detalle-btn').addEventListener('click', function() {
    const productoSelect = document.getElementById('producto-select');
    const cantidadInput = document.getElementById('cantidad-input');

    const productoId = productoSelect.value;
    const productoNombre = productoSelect.options[productoSelect.selectedIndex].getAttribute('data-nombre');
    const productoCategoria = productoSelect.options[productoSelect.selectedIndex].getAttribute('data-categoria');
    const cantidad = parseInt(cantidadInput.value);

    // Calcula el subtotal
    const precio = parseFloat(productoSelect.options[productoSelect.selectedIndex].getAttribute('data-precio'));
    const subtotal = precio * cantidad;

    // Añade a la lista de detalles
    detalles.push({ productoId, cantidad, subtotal });
    totalVenta += subtotal;
    
    // Actualiza el HTML con el detalle
    const detallesContainer = document.getElementById('detalles-container');
    const detalleItem = document.createElement('div');
    detalleItem.classList.add('detalle-item');
    detalleItem.innerHTML = ` •
        ${productoNombre} [${productoCategoria}] x ${cantidad} - $${subtotal.toFixed(2)}
        <button type="button" class="delete-btn" data-index="${detalles.length - 1}" style="
    background-color: red;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    font-size: 12px;
    cursor: pointer;
    transition: background-color 0.3s ease;
">X</button>
    `;
    detallesContainer.appendChild(detalleItem);


    // Actualiza el total
    document.getElementById('total-venta').textContent = totalVenta.toFixed(2);

    // Añade detalles ocultos al formulario
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'detalles';
    input.value = `${productoId},${cantidad}`;
    input.id = `detalle-${detalles.length - 1}`;
    document.getElementById('venta-form').appendChild(input); 
    });

    // Función para eliminar un detalle
    document.getElementById('detalles-container').addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('delete-btn')) {
            const index = event.target.getAttribute('data-index');
            const detalle = detalles[index];
            detalles.splice(index, 1); // Elimina el detalle del array
            totalVenta -= detalle.subtotal; // Resta el subtotal del total de la venta

            // Elimina el input oculto del formulario asociado
            const input = document.getElementById(`detalle-${index}`);
            if (input) {
                input.remove();
            }


            // Actualiza el HTML
            event.target.parentElement.remove(); // Elimina el detalle visualmente
            document.getElementById('total-venta').textContent = totalVenta.toFixed(2);
        }
    });