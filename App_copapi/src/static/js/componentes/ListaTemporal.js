class ListaTemporal {
    constructor({ contenedor, idLista, columnas, datos = [] }) {
        this.contenedor = document.getElementById(contenedor);
        this.idLista = idLista;
        this.columnas = columnas;
        this.datos = datos;

        this.render();
        this.agregarEventListeners();
    }

    render() {
        this.contenedor.innerHTML = `
            <table id="${this.idLista}" class="tabla-temporal">
                <thead>
                    <tr>
                        ${this.columnas.map(col => `<th>${col.titulo}</th>`).join('')}
                        <th>Cantidad</th>
                        <th>Operación</th>
                    </tr>
                </thead>
                <tbody>
                    ${this.datos.map((item, index) => this.filaHTML(item, index)).join('')}
                </tbody>
            </table>
        `;
    }

    filaHTML(item, index) {
        return `
            <tr data-index="${index}">
                ${this.columnas.map(col => `<td data-label="${col.titulo}: ">${item[col.campo] || ''}</td>`).join('')}
                <td data-label="Cantidad: ">
                    <input type="number" value="${item.cantidad || 1}" min="1" class="cantidad-input input-style" data-index="${index}">
                </td>
                <td data-label="Operación: ">
                    <button class="btn-eliminar btn-tb-opcion bg-rojo-1" data-index="${index}"><i class='bx bx-trash'></i></button>
                </td>
            </tr>
        `;
    }

    elementosSonIguales(a, b) {
        return this.columnas.every(col => a[col.campo] === b[col.campo]);
    }

    agregarElemento(nuevoElemento) {
        const indiceExistente = this.datos.findIndex(item => this.elementosSonIguales(item, nuevoElemento));

        if (indiceExistente !== -1) {
            // Si ya existe, incrementar la cantidad
            this.datos[indiceExistente].cantidad = (parseInt(this.datos[indiceExistente].cantidad) || 1) + 1;
        } else {
            // Si no existe, agregar con cantidad 1
            nuevoElemento.cantidad = 1;
            this.datos.push(nuevoElemento);
        }

        this.render();
    }

    eliminarElemento(index) {
        this.datos.splice(index, 1);
        this.render();
    }

    obtenerDatos() {
        return this.datos.map((item, index) => ({
            ...item,
            cantidad: document.querySelector(`.cantidad-input[data-index='${index}']`).value
        }));
    }

    agregarEventListeners() {
        this.contenedor.addEventListener("click", (e) => {
            if (e.target.closest(".btn-eliminar")) {  
                const index = e.target.closest(".btn-eliminar").dataset.index;
                this.eliminarElemento(index);
            }
        });

        this.contenedor.addEventListener("input", (e) => {
            if (e.target.classList.contains("cantidad-input")) {
                const index = e.target.dataset.index;
                let nuevaCantidad = parseInt(e.target.value);

                if (nuevaCantidad <= 0) {
                    this.eliminarElemento(index);
                } else {
                    this.datos[index].cantidad = nuevaCantidad;
                }
            }
        });
    }
}

export default ListaTemporal;