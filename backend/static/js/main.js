const API_BASE = "";

document.addEventListener("DOMContentLoaded", () => {
    const header = document.getElementById("header");
    const navToggle = document.getElementById("navToggle");
    const navMenu = document.getElementById("navMenu");
    const backToTop = document.getElementById("backToTop");
    const form = document.getElementById("reservationForm");
    const formStatus = document.getElementById("formStatus");
    const dateInput = document.getElementById("fecha");
    const submitBtn = form.querySelector('button[type="submit"]');
    const yearEl = document.getElementById("year");

    const onScroll = () => {
        const scrolled = window.scrollY > 40;
        header.classList.toggle("scrolled", scrolled);
        backToTop.classList.toggle("show", window.scrollY > 500);
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    const cerrarMenu = () => {
        navMenu.classList.remove("open");
        navToggle.classList.remove("active");
        navToggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("no-scroll");
    };

    navToggle.addEventListener("click", () => {
        const isOpen = navMenu.classList.toggle("open");
        navToggle.classList.toggle("active", isOpen);
        navToggle.setAttribute("aria-expanded", String(isOpen));
        document.body.classList.toggle("no-scroll", isOpen);
    });

    document.querySelectorAll(".nav-menu a").forEach((link) => {
        link.addEventListener("click", cerrarMenu);
    });

    document.addEventListener("click", (e) => {
        if (!navMenu.classList.contains("open")) return;
        if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
            cerrarMenu();
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) cerrarMenu();
    });

    const botonesCarta = document.querySelectorAll(".carta-tab");
    if (botonesCarta.length) {
        const activarPestana = (boton) => {
            document.querySelectorAll(".carta-tab").forEach((b) => {
                b.classList.remove("active");
                b.setAttribute("aria-selected", "false");
            });
            document.querySelectorAll(".carta-panel").forEach((p) => p.classList.remove("active"));
            boton.classList.add("active");
            boton.setAttribute("aria-selected", "true");
            const panel = document.getElementById(boton.dataset.tab);
            if (panel) panel.classList.add("active");
        };

        const lista = Array.from(botonesCarta);
        lista.forEach((boton, indice) => {
            boton.addEventListener("click", () => activarPestana(boton));
            boton.addEventListener("keydown", (e) => {
                let destino = null;
                if (e.key === "ArrowRight") destino = lista[(indice + 1) % lista.length];
                if (e.key === "ArrowLeft") destino = lista[(indice - 1 + lista.length) % lista.length];
                if (destino) {
                    e.preventDefault();
                    destino.focus();
                    activarPestana(destino);
                }
            });
        });
    }

    const revealEls = document.querySelectorAll("[data-reveal]");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("revealed");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15, rootMargin: "0px 0px -60px 0px" }
        );
        revealEls.forEach((el) => observer.observe(el));
    } else {
        revealEls.forEach((el) => el.classList.add("revealed"));
    }

    if (dateInput) {
        dateInput.min = new Date().toISOString().split("T")[0];
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const setStatus = (message, type) => {
        formStatus.textContent = message;
        formStatus.className = "form-status" + (type ? ` ${type}` : "");
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = new FormData(form);
        const payload = {
            nombre: String(data.get("nombre") || "").trim(),
            correo: String(data.get("correo") || "").trim(),
            telefono: String(data.get("telefono") || "").trim(),
            fecha: data.get("fecha"),
            hora: data.get("hora"),
            comensales: data.get("comensales"),
            mensaje: String(data.get("mensaje") || "").trim(),
        };

        setStatus("", "");

        if (!payload.nombre || !payload.correo || !payload.fecha || !payload.comensales) {
            setStatus("Por favor, completa todos los campos obligatorios.", "error");
            return;
        }

        if (!emailRegex.test(payload.correo)) {
            setStatus("Introduce un correo electrónico válido.", "error");
            return;
        }

        submitBtn.disabled = true;
        setStatus("Enviando reserva...", "");

        try {
            const response = await fetch(`${API_BASE}/api/reservas/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify(payload),
            });

            let result = {};
            try {
                result = await response.json();
            } catch (parseError) {
                result = {};
            }

            if (response.ok && result.ok) {
                const hora = payload.hora ? ` a las ${payload.hora}` : "";
                setStatus(
                    `¡Gracias, ${payload.nombre}! Reserva recibida para ${payload.comensales} ` +
                        `persona(s) el ${payload.fecha}${hora}. Te contactaremos para confirmar.`,
                    "success"
                );
                form.reset();
                if (dateInput) dateInput.min = new Date().toISOString().split("T")[0];
            } else if (response.status === 400 && result.errores) {
                const primerError = Object.values(result.errores)[0];
                setStatus(primerError || "Revisa los datos del formulario.", "error");
            } else {
                setStatus("No se pudo registrar la reserva. Inténtalo de nuevo.", "error");
            }
        } catch (error) {
            setStatus(
                "No se pudo conectar con el servidor. Comprueba que el backend esté en marcha.",
                "error"
            );
        } finally {
            submitBtn.disabled = false;
        }
    });

    const asistente = document.getElementById("asistente");
    if (asistente) {
        const asistenteToggle = document.getElementById("asistenteToggle");
        const asistentePanel = document.getElementById("asistentePanel");
        const asistenteCerrar = document.getElementById("asistenteCerrar");
        const asistenteForm = document.getElementById("asistenteForm");
        const asistenteInput = document.getElementById("asistenteInput");
        const asistenteMensajes = document.getElementById("asistenteMensajes");
        const historialAsistente = [];

        const abrirAsistente = (abrir) => {
            asistente.classList.toggle("abierto", abrir);
            asistentePanel.hidden = !abrir;
            asistenteToggle.setAttribute("aria-expanded", String(abrir));
            if (abrir) asistenteInput.focus();
        };

        asistenteToggle.addEventListener("click", () => abrirAsistente(asistentePanel.hidden));
        asistenteCerrar.addEventListener("click", () => abrirAsistente(false));

        const agregarMensaje = (texto, tipo) => {
            const burbuja = document.createElement("div");
            burbuja.className = `asistente-msg ${tipo}`;
            burbuja.textContent = texto;
            asistenteMensajes.appendChild(burbuja);
            asistenteMensajes.scrollTop = asistenteMensajes.scrollHeight;
            return burbuja;
        };

        asistenteForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const texto = asistenteInput.value.trim();
            if (!texto) return;

            agregarMensaje(texto, "user");
            asistenteInput.value = "";
            historialAsistente.push({ role: "user", content: texto });

            const burbuja = agregarMensaje("…", "bot");
            const boton = asistenteForm.querySelector("button");
            boton.disabled = true;
            let acumulado = "";

            try {
                const respuesta = await fetch(`${API_BASE}/api/asistente/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    body: JSON.stringify({
                        mensaje: texto,
                        historial: historialAsistente.slice(-8),
                    }),
                });

                if (!respuesta.ok) {
                    let msg = "No pude contactar con el asistente.";
                    try {
                        const json = await respuesta.json();
                        if (json.error) msg = json.error;
                    } catch (parseError) {}
                    burbuja.textContent = msg;
                    historialAsistente.pop();
                    return;
                }

                const lector = respuesta.body.getReader();
                const decodificador = new TextDecoder();
                let buffer = "";
                while (true) {
                    const { value, done } = await lector.read();
                    if (done) break;
                    buffer += decodificador.decode(value, { stream: true });
                    const lineas = buffer.split("\n");
                    buffer = lineas.pop();
                    for (const linea of lineas) {
                        if (!linea.trim()) continue;
                        let objeto;
                        try {
                            objeto = JSON.parse(linea);
                        } catch (parseError) {
                            continue;
                        }
                        if (objeto.delta) {
                            acumulado += objeto.delta;
                            burbuja.textContent = acumulado;
                            asistenteMensajes.scrollTop = asistenteMensajes.scrollHeight;
                        } else if (objeto.error) {
                            burbuja.textContent = objeto.error;
                        }
                    }
                }

                if (!acumulado && !burbuja.textContent.trim()) {
                    burbuja.textContent = "No obtuve respuesta. Inténtalo de nuevo.";
                }
                if (acumulado) historialAsistente.push({ role: "assistant", content: acumulado });
            } catch (error) {
                burbuja.textContent =
                    "No se pudo conectar con el asistente. Comprueba que Ollama esté en marcha.";
                historialAsistente.pop();
            } finally {
                boton.disabled = false;
            }
        });
    }

    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }
});
