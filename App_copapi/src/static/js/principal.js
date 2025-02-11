// URL del backend
const URL_API = "http://127.0.0.1:5020"

// Función para crear un mensaje emergente en pantalla
function crearMensaje(titulo, mensaje, redireccion) {
    const contenedor = document.getElementById("mensaje");
    const overlay = document.getElementById("popup-overlay");

    // Si ya hay un mensaje activo, salir para evitar duplicados
    if (contenedor.firstChild) return;

    // Determinar el icono según el tipo de mensaje
    const iconos = {
        error: "<i class='bx bx-x-circle'></i>",
        exito: "<i class='bx bx-check-circle'></i>",
    };

    const icono = iconos[titulo.toLowerCase()] || "";

    // Crear elementos dinámicamente
    const popup = document.createElement("div");
    popup.classList.add("popup", titulo);

    popup.innerHTML = `
        <div class="icono-mensaje ${titulo}">${icono}</div>
        <h2>${titulo}</h2>
        <p>${mensaje}</p>
    `;

    const closeButton = document.createElement("button");
    closeButton.classList.add("close-btn");
    closeButton.textContent = "Ok";

    popup.appendChild(closeButton);
    contenedor.appendChild(popup);
    overlay.style.display = "block";

    // Evento para cerrar el mensaje
    closeButton.addEventListener("click", () => {
        contenedor.innerHTML = "";
        overlay.style.display = "none";
        if (redireccion) window.location.href = redireccion;
    });
}

// Agregar (*) a todos los inputs y selects obligatorios
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("input[required], select[required]").forEach((element) => {
        const label = document.querySelector(`label[for="${element.name}"]`);
        if (label) label.classList.add("required-label");
    });
});
