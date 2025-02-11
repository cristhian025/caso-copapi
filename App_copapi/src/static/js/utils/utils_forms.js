
// Crear Select 
function htmlSelect(datos,id_select) {
    const select = document.getElementById(id_select);
    datos.forEach(contenido => {
        const option = document.createElement('option');
        option.value = contenido.id;
        option.textContent = contenido.nombre;
        select.appendChild(option);
    });
}

// Crear Checkbox
function htmlCheckbox(data, id_checkbox, nombre_cb) {
    const contenedor_chbx = document.getElementById(id_checkbox);
    data.forEach(contenido => {
        const label = document.createElement('label');
        label.textContent = contenido.nombre;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = nombre_cb;
        checkbox.value = contenido.id;

        contenedor_chbx.appendChild(checkbox);
        contenedor_chbx.appendChild(label);
        //contenedor_chbx.appendChild(document.createElement('br'));
    });
}
