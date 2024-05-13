from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pynput.mouse import Listener as MouseListener
import keyboard
import sys

# Configuración inicial de Selenium
driver = webdriver.Chrome()
driver.get('https://tu-pagina-web.com')

# Lista para almacenar los XPATHs generados
xpath_list = []

# Función para obtener el XPATH de un elemento dado su posición x, y
def get_xpath_by_position(x, y):
    element = driver.execute_script("""
        function getElementXPath(elt){
            var path = '';
            for (; elt && elt.nodeType == 1; elt = elt.parentNode){
                idx = getElementIdx(elt);
                xname = elt.tagName;
                if (idx > 1) xname += '[' + idx + ']';
                path = '/' + xname + path;
            }
            return path;
        }
        function getElementIdx(elt){
            var count = 1;
            for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){
                if(sib.nodeType == 1 && sib.tagName == elt.tagName) count++;
            }
            return count;
        }
        var elem = document.elementFromPoint(arguments[0], arguments[1]);
        if (elem) {
            return getElementXPath(elem);
        }
        return null;
    """, x, y)
    return element

# Función para manejar los eventos de clic del mouse
def on_click(x, y, button, pressed):
    if pressed:
        xpath = get_xpath_by_position(x, y)
        if xpath:
            xpath_list.append(xpath)
            print(f"Se hizo clic en el elemento con XPATH: {xpath}")
        else:
            print("No se encontró ningún elemento en la posición dada.")

# Iniciar el listener del mouse
listener = MouseListener(on_click=on_click)
listener.start()

# Bucle para mantener el programa en ejecución hasta que se presione Escape
try:
    while True:
        if keyboard.is_pressed('esc'):
            print("\nSe presionó Escape, finalizando el programa...")
            print("\nXPATHs generados:")
            for i, xpath in enumerate(xpath_list, start=1):
                print(f"Paso {i}: {xpath}")
            driver.quit()
            sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
finally:
    listener.stop()
    driver.quit()
