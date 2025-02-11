class DataTable {
    constructor({ contenedor, idTabla, columnas, datos, filtros = {} }) {
        this.contenedor = document.getElementById(contenedor);
        if (!this.contenedor) {
            console.error('No se encontró el contenedor:', contenedor);
            return;
        }

        this.idTabla = idTabla;
        this.columnas = columnas;
        this.datos = datos;
        this.filtros = filtros; // Almacenar filtros iniciales

        this.init();
    }

    aplicarFiltros(datos) {
        return datos.filter(fila => {
            return Object.entries(this.filtros).every(([clave, valor]) => {
                if (valor === '' || valor === null || valor === undefined) {
                    return true; // No aplicar filtro si está vacío
                }

                // Convertir valores a string y aplicar filtro (insensible a mayúsculas/minúsculas)
                const datoFila = String(fila[clave] || '').toLowerCase();
                const valorFiltro = String(valor).toLowerCase();

                return datoFila.includes(valorFiltro);
            });
        });
    }

    actualizarFiltros(nuevosFiltros) {
        this.filtros = { ...this.filtros, ...nuevosFiltros };
        this.renderTabla(); // Recargar los datos aplicando los nuevos filtros
    }

    renderTabla() {
        const tbody = this.tabla.querySelector('tbody');
        tbody.innerHTML = '';

        const datosFiltrados = this.aplicarFiltros(this.datos);

        if (datosFiltrados.length > 0) {
            datosFiltrados.forEach((fila) => {
                const tr = document.createElement('tr');
                tr.innerHTML = this.columnas.map(col => {
                    let contenido = (fila[col.campo] !== undefined && fila[col.campo] !== null) ? fila[col.campo] : '';
                    if (col.render) {
                        contenido = col.render(fila);
                    }
                    return `<td data-label="${col.titulo}: ">${contenido}</td>`;
                }).join('');
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = `<tr><td colspan="${this.columnas.length}" style="text-align: center;">No se encontraron datos.</td></tr>`;
        }
    }

    render() {
        this.contenedor.innerHTML = `
            <div class="dataTable">
                <table id="${this.idTabla}">
                    <thead>
                        <tr>
                            ${this.columnas.map(col => `<th>${col.titulo}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        `;

        // Asignar elementos internos
        this.tabla = document.querySelector(`#${this.idTabla}`);
        this.renderTabla();
    }

    init() {
        this.render();
    }
}

export default DataTable;
