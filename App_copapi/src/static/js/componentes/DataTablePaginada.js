class DataTablePaginada {
    constructor({ contenedor, idTabla, columnas, placeholderBusqueda, urlDatos, filtros = {} }) {
        this.contenedor = document.getElementById(contenedor);
        if (!this.contenedor) {
            console.error('No se encontró el contenedor:', contenedor);
            return;
        }

        this.idTabla = idTabla;
        this.columnas = columnas;
        this.placeholderBusqueda = placeholderBusqueda;
        this.urlDatos = urlDatos;
        this.filtros = filtros; // Almacenar filtros iniciales

        // Estado interno
        this.pagina = 1;
        this.limite = 10;
        this.busqueda = '';
        this.totalRegistros = 0;
        this.datosCompletos = []; // Para almacenar todos los datos y aplicar filtros

        this.init();
    }

    async cargarDatos() {
        try {
            const response = await fetch(`${this.urlDatos}?pagina=${this.pagina}&por_pagina=${this.limite}&busqueda=${this.busqueda}`);
            const data = await response.json();
            this.totalRegistros = data.total_registros;

            // Guardamos todos los datos sin filtrar
            this.datosCompletos = data.registros;

            // Aplicamos los filtros antes de renderizar
            const datosFiltrados = this.aplicarFiltros(this.datosCompletos);

            this.renderTabla(datosFiltrados);
            this.actualizarPaginacion();
        } catch (error) {
            console.error('Error al cargar los datos:', error);
        }
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
        this.cargarDatos(); // Recargar los datos aplicando los nuevos filtros
    }

    renderTabla(datos) {
        const tbody = this.tabla.querySelector('tbody');
        tbody.innerHTML = '';

        if (datos.length > 0) {
            datos.forEach((fila) => {
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

    // Mantiene la funcionalidad de paginación
    actualizarPaginacion() {
        const totalPaginas = Math.ceil(this.totalRegistros / this.limite);
        this.paginaSelect.innerHTML = '';

        for (let i = 1; i <= totalPaginas; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            if (i === this.pagina) option.selected = true;
            this.paginaSelect.appendChild(option);
        }

        this.btnAnterior.disabled = this.pagina === 1;
        this.btnSiguiente.disabled = this.pagina === totalPaginas || this.totalRegistros === 0;
    }

    eventos() {
        this.btnBuscar.addEventListener('click', () => {
            this.busqueda = this.inputBusqueda.value;
            this.pagina = 1;
            this.cargarDatos();
        });

        this.limiteSelect.addEventListener('change', () => {
            this.limite = parseInt(this.limiteSelect.value);
            this.pagina = 1;
            this.cargarDatos();
        });

        this.btnAnterior.addEventListener('click', () => {
            if (this.pagina > 1) {
                this.pagina--;
                this.cargarDatos();
            }
        });

        this.btnSiguiente.addEventListener('click', () => {
            const totalPaginas = Math.ceil(this.totalRegistros / this.limite);
            if (this.pagina < totalPaginas) {
                this.pagina++;
                this.cargarDatos();
            }
        });

        this.paginaSelect.addEventListener('change', () => {
            this.pagina = parseInt(this.paginaSelect.value);
            this.cargarDatos();
        });
    }

    render() {
        this.contenedor.innerHTML = `
            <div class="dataTable-filtro">
                <div class="search-filtro">
                    <input type="search" id="buscar" placeholder="${this.placeholderBusqueda}" />
                    <button id="btn-buscar"><i class="bx bx-sync"></i></button>
                </div>
            </div>
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
            <div class="dataTable-paginacion">
                <div class="paginacion-limit">
                    <span>Mostrar:</span>
                    <select id="limite">
                        <option value="10">10</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                    </select>
                </div>
                <div class="paginacion-controles">
                    <button id="btn-anterior" class="btn">Anterior</button>
                    <select id="pagina"></select>
                    <button id="btn-siguiente" class="btn">Siguiente</button>
                </div>
            </div>
        `;

        // Asignar elementos internos
        this.tabla = document.querySelector(`#${this.idTabla}`);
        this.inputBusqueda = document.getElementById('buscar');
        this.btnBuscar = document.getElementById('btn-buscar');
        this.limiteSelect = document.getElementById('limite');
        this.paginaSelect = document.getElementById('pagina');
        this.btnAnterior = document.getElementById('btn-anterior');
        this.btnSiguiente = document.getElementById('btn-siguiente');

        this.eventos();
        this.cargarDatos();
    }

    init() {
        this.render();
    }
}

export default DataTablePaginada;
