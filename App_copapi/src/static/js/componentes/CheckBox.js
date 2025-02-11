class Checkbox {
    constructor({ urlDatos, idCheckboxContainer, nombreCb, placeholder }) {
        this.urlDatos = urlDatos;
        this.idCheckboxContainer = idCheckboxContainer;
        this.nombreCb = nombreCb;
        this.placeholder = placeholder;

        this.init();
    }

    async obtenerDatos() {
        try {
            const response = await fetch(this.urlDatos);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            
            const data = await response.json();
            if (data.registros && Array.isArray(data.registros)) {
                this.renderCheckboxes(data.registros);
            } else {
                console.warn('No se encontraron registros válidos.');
            }
        } catch (error) {
            console.error('Error al obtener los datos:', error);
        }
    }

    renderCheckboxes(datos) {
        const contenedorChbx = document.getElementById(this.idCheckboxContainer);
        if (!contenedorChbx) {
            console.error('No se encontró el contenedor con id:', this.idCheckboxContainer);
            return;
        }

        contenedorChbx.innerHTML = ''; // Limpiar antes de agregar nuevos elementos
        const fragment = document.createDocumentFragment();

        // Agregar placeholder si se proporciona
        if (this.placeholder) {
            const placeholderText = document.createElement('span');
            placeholderText.textContent = this.placeholder;
            placeholderText.style.fontWeight = 'bold';
            placeholderText.style.display = 'block';
            placeholderText.style.marginBottom = '5px';
            fragment.appendChild(placeholderText);
        }

        // Crear checkboxes con accesibilidad mejorada
        datos.forEach(contenido => {
            const wrapper = document.createElement('div');
            wrapper.style.display = 'flex';
            wrapper.style.alignItems = 'center';
            wrapper.style.gap = '5px';
            wrapper.style.marginBottom = '5px';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.name = this.nombreCb;
            checkbox.value = contenido.id;
            checkbox.id = `${this.nombreCb}-${contenido.id}`;

            const label = document.createElement('label');
            label.textContent = contenido.nombre;
            label.htmlFor = checkbox.id;

            wrapper.appendChild(checkbox);
            wrapper.appendChild(label);
            fragment.appendChild(wrapper);
        });

        contenedorChbx.appendChild(fragment);
    }

    init() {
        this.obtenerDatos();
    }
}

export default Checkbox;
