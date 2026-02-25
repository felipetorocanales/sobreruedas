import asyncio
from playwright.async_api import async_playwright

# --- CONFIGURACIÓN ---
PORTAL_URL = "https://ejemplo-portal.com/login"  # CAMBIAR POR LA URL REAL
USERNAME = "tu_usuario"
PASSWORD = "tu_password"

# --- SELECTORES (CAMBIAR SEGÚN EL SITIO WEB) ---
# Puedes encontrar estos inspeccionando el elemento en el navegador (Click derecho -> Inspeccionar)
SELECTOR_USERNAME = "input[name='username']"  # Ejemplo: id='user', class='login-field', etc.
SELECTOR_PASSWORD = "input[name='password']"
SELECTOR_LOGIN_BTN = "button[type='submit']"

# Selectores para crear el post
SELECTOR_NEW_POST_BTN = "a#new-post"         # Botón para ir a crear post
SELECTOR_POST_TITLE = "input#post-title"     # Campo de título
SELECTOR_POST_CONTENT = "textarea#post-body" # Campo de contenido
SELECTOR_PUBLISH_BTN = "button#publish"      # Botón de publicar

async def run():
    async with async_playwright() as p:
        # Lanzamos el navegador en modo visible (headless=False) para ver qué hace
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print(f"Navegando a {PORTAL_URL}...")
        await page.goto(PORTAL_URL)

        # --- INICIO DE SESIÓN ---
        print("Iniciando sesión...")
        try:
            # Esperar a que el campo de usuario esté visible
            await page.wait_for_selector(SELECTOR_USERNAME, timeout=5000)
            
            await page.fill(SELECTOR_USERNAME, USERNAME)
            await page.fill(SELECTOR_PASSWORD, PASSWORD)
            await page.click(SELECTOR_LOGIN_BTN)
            
            # Esperar a que la navegación se complete o aparezca un elemento de la home
            await page.wait_for_load_state('networkidle')
            print("Login enviado.")
        except Exception as e:
            print(f"Error en el login: {e}")
            await browser.close()
            return

        # --- PUBLICAR POST ---
        print("Intentando publicar un post...")
        try:
            # Navegar a la página de nuevo post (si es necesario hacer clic en un botón)
            await page.click(SELECTOR_NEW_POST_BTN)
            await page.wait_for_selector(SELECTOR_POST_TITLE)

            await page.fill(SELECTOR_POST_TITLE, "Título Automático desde Python")
            await page.fill(SELECTOR_POST_CONTENT, "Este es un contenido de prueba generado automáticamente por un script de Playwright.")
            
            # Hacer clic en publicar
            await page.click(SELECTOR_PUBLISH_BTN)
            
            # Esperar confirmación visual o navegación
            await page.wait_for_load_state('networkidle')
            print("Post publicado exitosamente (teóricamente).")
            
            # Captura de pantalla para verificar
            await page.screenshot(path="screenshot_final.png")
            print("Captura de pantalla guardada como 'screenshot_final.png'.")

        except Exception as e:
            print(f"Error al publicar el post: {e}")

        # Pausa breve para ver el resultado antes de cerrar
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
