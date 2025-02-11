/* ================================= Funciones clave del Menú ================================= */

document.addEventListener("DOMContentLoaded", () => {
  // ---------------- Modo Oscuro ----------------
  const btnDarkMode = document.getElementById("btn-darkmode");
  const body = document.body;
  const darkModeIcon = document.querySelector("#btn-darkmode i");

  // Cargar preferencia de modo oscuro desde localStorage
  const isDarkMode = localStorage.getItem("darkMode") === "true";
  body.classList.toggle("dark", isDarkMode);
  darkModeIcon.classList.toggle("bx-sun", isDarkMode);
  darkModeIcon.classList.toggle("bx-moon", !isDarkMode);

  btnDarkMode?.addEventListener("click", () => {
    const darkModeEnabled = body.classList.toggle("dark");
    localStorage.setItem("darkMode", darkModeEnabled);
    darkModeIcon.classList.toggle("bx-sun", darkModeEnabled);
    darkModeIcon.classList.toggle("bx-moon", !darkModeEnabled);
  });

  // ------------------ Menú Lateral ------------------
  const btnAsideMenu = document.getElementById("btn-aside-menu");
  const asideMenu = document.querySelector(".aside-menu");

  if (btnAsideMenu && asideMenu) {
    const menuState = localStorage.getItem("asideMenuState") || "open";
    setAsideMenuState(menuState);

    btnAsideMenu.addEventListener("click", () => {
      const newState = asideMenu.classList.toggle("open") ? "open" : "close";
      localStorage.setItem("asideMenuState", newState);
      setAsideMenuState(newState);
    });
  }

  function setAsideMenuState(state) {
    asideMenu.classList.toggle("open", state === "open");
    asideMenu.classList.toggle("close", state === "close");
    btnAsideMenu.innerHTML =
      state === "open"
        ? "<i class='bx bx-menu-alt-left'></i>"
        : "<i class='bx bx-menu'></i>";
  }

  // ------------------ Menú Desplegable ------------------
  document.querySelectorAll(".aside-agrupador > ul > li").forEach((item) => {
    item.addEventListener("click", function () {
      document
        .querySelectorAll(".aside-agrupador > ul > li.active")
        .forEach((sibling) => {
          if (sibling !== this) sibling.classList.remove("active");
          sibling.querySelector("ul")?.style.setProperty("display", "none");
        });

      this.classList.toggle("active");
      const subMenu = this.querySelector("ul");
      if (subMenu)
        subMenu.style.display =
          subMenu.style.display === "block" ? "none" : "block";
    });
  });

  // ------------------ Botón de Usuario ------------------
  const btnUsuario = document.getElementById("btn-usuario");
  const userSubMenu = btnUsuario
    ?.closest("li")
    ?.querySelector(".header-sub-opcion");

  btnUsuario?.addEventListener("click", (event) => {
    event.stopPropagation();
    userSubMenu?.classList.toggle("open");
    userSubMenu?.classList.toggle("close");
  });

  document.addEventListener("click", (event) => {
    if (
      !btnUsuario?.contains(event.target) &&
      !userSubMenu?.contains(event.target)
    ) {
      userSubMenu?.classList.remove("open");
      userSubMenu?.classList.add("close");
    }
  });

  // ------------------ Asegurar Renderizado ------------------
  document.body.style.display = "block";
});
