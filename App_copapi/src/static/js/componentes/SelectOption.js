class SelectOption {
    constructor({ urlDatos, idSelect, placeholder }) {
        this.urlDatos = urlDatos;
        this.idSelect = idSelect;
        this.placeholder = placeholder;

        this.init();
    }

    async obtenerDatos() {
        try {
            const response = await fetch(this.urlDatos);
            const data = await response.json();
            if (data.registros) {
                this.renderSelect(data.registros);
            } else {
                console.error('No se encontraron registros');
            }
        } catch (error) {
            console.error('Error al obtener los datos:', error);
        }
    }

    renderSelect(datos) {
        const select = document.getElementById(this.idSelect);
        if (!select) {
            console.error('No se encontró el select con id:', this.idSelect);
            return;
        }

        select.innerHTML = '';

        // Crear la opción por defecto
        const optionDefault = document.createElement('option');
        optionDefault.value = '';
        optionDefault.textContent = this.placeholder || 'Seleccione una opción';
        select.appendChild(optionDefault);

        // Llenar el select con los datos obtenidos
        datos.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.nombre;
            select.appendChild(option);
        });
    }

    init() {
        this.obtenerDatos();
    }
}

export default SelectOption;