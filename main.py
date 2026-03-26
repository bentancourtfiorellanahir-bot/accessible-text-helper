from simplifier import simplify_text
from text_to_speech import speak_text


def read_text_from_file(file_path: str) -> str:
    """Lee texto desde un archivo .txt."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""
    except Exception as error:
        print(f"Error al leer el archivo: {error}")
        return ""


def get_text() -> str:
    """Permite al usuario escribir texto o cargarlo desde un archivo."""
    print("\n¿Cómo quieres ingresar el texto?")
    print("1. Escribir texto manualmente")
    print("2. Leer texto desde un archivo .txt")

    option = input("Elige una opción (1 o 2): ").strip()

    if option == "1":
        return input("\nEscribe tu texto:\n")
    elif option == "2":
        file_path = input("\nEscribe la ruta del archivo .txt: ").strip()
        text = read_text_from_file(file_path)
        if not text:
            print("No se pudo leer el archivo.")
        return text
    else:
        print("Opción no válida.")
        return ""


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