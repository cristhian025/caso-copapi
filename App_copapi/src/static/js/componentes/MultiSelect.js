class MultiSelect {
    constructor({ idContenedor, name, urlDatos }) {
        this.idContenedor = idContenedor;
        this.name = name;
        this.urlDatos = urlDatos;
        this.selectedCount = 0;
        this.datos = [];
        this.init();
    }

    async obtenerDatos() {
        try {
            const response = await fetch(this.urlDatos);
            const data = await response.json();
            if (data.registros) {
                this.datos = data.registros;
                this.render();
            } else {
                console.error("No se encontraron registros");
            }
        } catch (error) {
            console.error("Error al obtener los datos:", error);
        }
    }

    render() {
        const contenedor = document.getElementById(this.idContenedor);
        if (!contenedor) {
            console.error("No se encontró el contenedor");
            return;
        }

        // Generar HTML dinámicamente
        contenedor.innerHTML = `
            <div class="select-box">0 seleccionados ▼</div>
            <div class="checkbox-list hidden">
                <input type="search" class="search-input" placeholder="Buscar...">
                <label class="select-all">
                    <input type="checkbox" class="select-all-checkbox"> (Seleccionar todo)
                </label>
                <div class="checkbox-container"></div>
            </div>
        `;

        this.agregarEventos();
        this.renderCheckboxes();
    }

    renderCheckboxes() {
        const contenedorCheckboxes = document.querySelector(`#${this.idContenedor} .checkbox-container`);
        if (!contenedorCheckboxes) return;

        contenedorCheckboxes.innerHTML = this.datos.map(item => `
            <label>
                <input type="checkbox" value="${item.id}" name="${this.name}"> ${item.nombre}
            </label>
        `).join('');
    }

    agregarEventos() {
        const contenedor = document.getElementById(this.idContenedor);
        const selectBox = contenedor.querySelector(".select-box");
        const checkboxList = contenedor.querySelector(".checkbox-list");
        const searchInput = contenedor.querySelector(".search-input");
        const selectAllCheckbox = contenedor.querySelector(".select-all-checkbox");

        // Mostrar/Ocultar lista de opciones
        selectBox.addEventListener("click", () => checkboxList.classList.toggle("hidden"));

        // Buscar elementos en la lista
        searchInput.addEventListener("input", () => {
            const filter = searchInput.value.toLowerCase();
            document.querySelectorAll(`#${this.idContenedor} .checkbox-container label`).forEach(label => {
                label.style.display = label.innerText.toLowerCase().includes(filter) ? "block" : "none";
            });
        });

        // Seleccionar/deseleccionar todos
        selectAllCheckbox.addEventListener("change", () => {
            const checkboxes = document.querySelectorAll(`#${this.idContenedor} .checkbox-container input[type="checkbox"]`);
            checkboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
            this.actualizarSeleccionados();
        });

        // Evento para actualizar la cantidad de seleccionados
        contenedor.addEventListener("change", (e) => {
            if (e.target.type === "checkbox" && !e.target.classList.contains("select-all-checkbox")) {
                this.actualizarSeleccionados();
            }
        });
    }

    actualizarSeleccionados() {
        const checkboxes = document.querySelectorAll(`#${this.idContenedor} .checkbox-container input[type="checkbox"]:checked`);
        this.selectedCount = checkboxes.length;
        document.querySelector(`#${this.idContenedor} .select-box`).textContent = `${this.selectedCount} seleccionados ▼`;
    }

    init() {
        this.obtenerDatos();
    }
}

export default MultiSelect;