"""
main.py

Programa principal de Accessible Text Helper.
"""

from __future__ import annotations

from simplifier import simplify_text, get_simplification_summary
from text_to_speech import create_tts


def read_text_from_file(file_path: str) -> str:
    """Lee texto desde un archivo .txt."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""


def ask_text_input(tts) -> str:
    """Permite elegir entre escribir texto o cargar un archivo."""
    tts.accessible_message(
        "Elige cómo quieres ingresar el texto. "
        "Opción 1: escribir texto. "
        "Opción 2: leer un archivo."
    )

    option = input("\nEscribe 1 o 2: ").strip()

    if option == "1":
        tts.accessible_message("Escribe o pega tu texto y luego presiona Enter.", read_aloud=True)
        return input("\nTexto: ").strip()

    if option == "2":
        tts.accessible_message("Escribe la ruta del archivo de texto.", read_aloud=True)
        file_path = input("\nRuta del archivo: ").strip()
        text = read_text_from_file(file_path)

        if not text:
            tts.accessible_message("No pude abrir el archivo.", read_aloud=True)
            return ""

        tts.accessible_message("Archivo cargado correctamente.", read_aloud=True)
        return text

    tts.accessible_message("Opción no válida.", read_aloud=True)
    return ""


def show_text_on_screen(title: str, text: str) -> None:
    """Muestra texto en pantalla de forma clara."""
    print(f"\n{'=' * 60}")
    print(title)
    print(f"{'=' * 60}\n")
    print(text)
    print(f"\n{'=' * 60}\n")


def configure_voice(tts) -> None:
    """Permite cambiar velocidad, volumen e idioma preferido."""
    tts.accessible_message(
        "Configuración de voz. Puedes cambiar velocidad, volumen e idioma."
    )

    try:
        rate_input = input("Velocidad actual aproximada 145. Escribe una nueva velocidad o presiona Enter: ").strip()
        volume_input = input("Volumen entre 0.0 y 1.0. Escribe un valor o presiona Enter: ").strip()
        language_input = input("Idioma preferido. Ejemplo es o en. Presiona Enter para dejarlo igual: ").strip()

        kwargs = {}

        if rate_input:
            kwargs["rate"] = int(rate_input)

        if volume_input:
            kwargs["volume"] = float(volume_input)

        if language_input:
            kwargs["preferred_language"] = language_input

        if kwargs:
            tts.update_settings(**kwargs)
            tts.accessible_message("Configuración actualizada correctamente.")
        else:
            tts.accessible_message("No hiciste cambios en la configuración.")

    except ValueError:
        tts.accessible_message("Ingresaste un valor no válido.")
    except Exception:
        tts.accessible_message("Ocurrió un error al actualizar la configuración.")


def option_read_text(tts) -> None:
    text = ask_text_input(tts)

    if not text:
        tts.accessible_message("No hay texto para leer.")
        return

    show_text_on_screen("TEXTO INGRESADO", text)
    tts.accessible_message("Voy a leer el texto.")
    tts.speak_text(text)


def option_simplify_text(tts) -> None:
    text = ask_text_input(tts)

    if not text:
        tts.accessible_message("No hay texto para simplificar.")
        return

    result = simplify_text(text)
    summary = get_simplification_summary(result)

    show_text_on_screen("TEXTO SIMPLIFICADO", result.simplified_text)
    print(summary)

    tts.accessible_message("El texto simplificado está listo.", read_aloud=True)


def option_simplify_and_read(tts) -> None:
    text = ask_text_input(tts)

    if not text:
        tts.accessible_message("No hay texto para simplificar y leer.")
        return

    result = simplify_text(text)
    summary = get_simplification_summary(result)

    show_text_on_screen("TEXTO SIMPLIFICADO", result.simplified_text)
    print(summary)

    tts.accessible_message("Voy a leer el texto simplificado.")
    tts.speak_text(result.simplified_text)


def option_list_voices(tts) -> None:
    tts.accessible_message("Mostrando voces disponibles en pantalla.", read_aloud=True)
    tts.print_available_voices()


def show_menu(tts) -> None:
    """Menú principal accesible."""
    while True:
        tts.accessible_message(
            "Menú principal. "
            "Opción 1: leer texto. "
            "Opción 2: simplificar texto. "
            "Opción 3: simplificar y leer. "
            "Opción 4: mostrar voces disponibles. "
            "Opción 5: configurar voz. "
            "Opción 6: salir."
        )

        choice = input("\nEscribe una opción: ").strip()

        if choice == "1":
            option_read_text(tts)

        elif choice == "2":
            option_simplify_text(tts)

        elif choice == "3":
            option_simplify_and_read(tts)

        elif choice == "4":
            option_list_voices(tts)

        elif choice == "5":
            configure_voice(tts)

        elif choice == "6":
            tts.accessible_message("Cerrando el programa. Hasta luego.")
            break

        else:
            tts.accessible_message("Opción no válida. Intenta de nuevo.")


def main() -> None:
    tts = create_tts(
        rate=145,
        volume=1.0,
        preferred_language="es",
        read_screen_messages=True,
        announce_actions=True,
    )

    tts.accessible_message(
        "Bienvenida a Accessible Text Helper. "
        "Esta herramienta puede leer texto, simplificarlo y ayudar a su comprensión."
    )

    show_menu(tts)


if __name__ == "__main__":
    main()
def show_menu() -> None:
    """Muestra el menú principal."""
    while True:
        print("\n=== ACCESSIBLE TEXT HELPER ===")
        print("1. Leer texto en voz alta")
        print("2. Simplificar texto")
        print("3. Simplificar y leer en voz alta")
        print("4. Salir")

        choice = input("Elige una opción: ").strip()

        if choice == "1":
            text = get_text()
            if text:
                print("\nLeyendo texto...")
                speak_text(text)

        elif choice == "2":
            text = get_text()
            if text:
                simplified = simplify_text(text)
                print("\nTexto simplificado:\n")
                print(simplified)

        elif choice == "3":
            text = get_text()
            if text:
                simplified = simplify_text(text)
                print("\nTexto simplificado:\n")
                print(simplified)
                print("\nLeyendo texto simplificado...")
                speak_text(simplified)

        elif choice == "4":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    show_menu()
