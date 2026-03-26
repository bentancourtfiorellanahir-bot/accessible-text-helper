"""
text_to_speech.py

Módulo de texto a voz orientado a accesibilidad.

Funciones principales:
- speak_text(): lee texto en voz alta
- accessible_message(): muestra y lee mensajes claros para el usuario
- list_available_voices(): lista las voces del sistema
- create_tts(): crea una instancia configurable del lector
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Any
import re
import time

import pyttsx3


@dataclass
class TTSConfig:
    """Configuración del motor de texto a voz."""
    rate: int = 145
    volume: float = 1.0
    voice_index: Optional[int] = None
    voice_name_contains: Optional[str] = None
    preferred_language: Optional[str] = None
    pause_between_chunks: float = 0.15
    max_chunk_length: int = 350
    read_screen_messages: bool = True
    announce_actions: bool = True


class AccessibleTTS:
    """Lector de texto a voz configurable y orientado a accesibilidad."""

    def __init__(self, config: Optional[TTSConfig] = None) -> None:
        self.config = config or TTSConfig()
        self.engine = pyttsx3.init()
        self._apply_base_settings()

    def _apply_base_settings(self) -> None:
        """Aplica velocidad, volumen y voz."""
        self.engine.setProperty("rate", self.config.rate)
        self.engine.setProperty("volume", self._clamp_volume(self.config.volume))
        selected_voice_id = self._select_voice_id()

        if selected_voice_id:
            self.engine.setProperty("voice", selected_voice_id)

    @staticmethod
    def _clamp_volume(volume: float) -> float:
        """Asegura que el volumen esté entre 0.0 y 1.0."""
        return max(0.0, min(1.0, volume))

    def _get_voices(self) -> List[Any]:
        """Obtiene las voces disponibles del sistema."""
        return self.engine.getProperty("voices") or []

    def _normalize_language_code(self, value: str) -> str:
        """Normaliza códigos de idioma para comparación."""
        return value.strip().lower().replace("_", "-")

    def _safe_decode_language(self, language_value: Any) -> str:
        """Convierte valores de idioma a string legible."""
        try:
            if isinstance(language_value, bytes):
                return language_value.decode("utf-8", errors="ignore").lower()
            return str(language_value).lower()
        except Exception:
            return ""

    def _voice_matches_language(self, voice: Any, preferred_language: str) -> bool:
        """Comprueba si una voz coincide con un idioma preferido."""
        target = self._normalize_language_code(preferred_language)

        languages = getattr(voice, "languages", [])
        for lang in languages:
            decoded = self._safe_decode_language(lang)
            decoded = decoded.replace("\x05", "").replace("_", "-")
            if target in decoded:
                return True

        name = getattr(voice, "name", "")
        voice_id = getattr(voice, "id", "")
        combined = f"{name} {voice_id}".lower()

        if target.startswith("es") and any(k in combined for k in ["spanish", "español", "es_"]):
            return True
        if target.startswith("en") and "english" in combined:
            return True

        return False

    def _select_voice_id(self) -> Optional[str]:
        """Selecciona la mejor voz posible según la configuración."""
        voices = self._get_voices()
        if not voices:
            return None

        if self.config.voice_index is not None:
            if 0 <= self.config.voice_index < len(voices):
                return voices[self.config.voice_index].id

        if self.config.voice_name_contains:
            keyword = self.config.voice_name_contains.lower()
            for voice in voices:
                name = getattr(voice, "name", "").lower()
                voice_id = getattr(voice, "id", "").lower()
                if keyword in name or keyword in voice_id:
                    return voice.id

        if self.config.preferred_language:
            for voice in voices:
                if self._voice_matches_language(voice, self.config.preferred_language):
                    return voice.id

        return voices[0].id

    def update_settings(
        self,
        *,
        rate: Optional[int] = None,
        volume: Optional[float] = None,
        voice_index: Optional[int] = None,
        voice_name_contains: Optional[str] = None,
        preferred_language: Optional[str] = None,
    ) -> None:
        """Actualiza la configuración del motor."""
        if rate is not None:
            self.config.rate = rate
            self.engine.setProperty("rate", rate)

        if volume is not None:
            self.config.volume = self._clamp_volume(volume)
            self.engine.setProperty("volume", self.config.volume)

        if voice_index is not None:
            self.config.voice_index = voice_index

        if voice_name_contains is not None:
            self.config.voice_name_contains = voice_name_contains

        if preferred_language is not None:
            self.config.preferred_language = preferred_language

        selected_voice_id = self._select_voice_id()
        if selected_voice_id:
            self.engine.setProperty("voice", selected_voice_id)

    def list_available_voices(self) -> List[dict]:
        """Devuelve una lista detallada de voces disponibles."""
        result = []
        for i, voice in enumerate(self._get_voices()):
            languages = []
            for lang in getattr(voice, "languages", []):
                decoded = self._safe_decode_language(lang).replace("\x05", "")
                languages.append(decoded)

            result.append(
                {
                    "index": i,
                    "name": getattr(voice, "name", "Unknown"),
                    "id": getattr(voice, "id", "Unknown"),
                    "languages": languages,
                    "gender": getattr(voice, "gender", "Unknown"),
                    "age": getattr(voice, "age", "Unknown"),
                }
            )
        return result

    def print_available_voices(self) -> None:
        """Imprime las voces disponibles de forma legible."""
        voices = self.list_available_voices()
        if not voices:
            print("\nNo se encontraron voces disponibles.\n")
            return

        print("\nVoces disponibles:\n")
        for voice in voices:
            print(f"Índice: {voice['index']}")
            print(f"Nombre: {voice['name']}")
            print(f"ID: {voice['id']}")
            print(f"Idiomas: {', '.join(voice['languages']) if voice['languages'] else 'No disponible'}")
            print(f"Género: {voice['gender']}")
            print(f"Edad: {voice['age']}")
            print("-" * 50)

    def _clean_text(self, text: str) -> str:
        """Limpia espacios innecesarios antes de leer."""
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def _split_text_into_chunks(self, text: str) -> List[str]:
        """
        Divide textos largos en fragmentos más cómodos para el motor.
        Intenta cortar por signos de puntuación antes que por longitud bruta.
        """
        cleaned_text = self._clean_text(text)

        if not cleaned_text:
            return []

        max_len = max(80, self.config.max_chunk_length)

        if len(cleaned_text) <= max_len:
            return [cleaned_text]

        sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)
        chunks: List[str] = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(sentence) > max_len:
                parts = self._split_long_sentence(sentence, max_len)
                for part in parts:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                    chunks.append(part.strip())
                continue

            tentative = f"{current_chunk} {sentence}".strip()
            if len(tentative) <= max_len:
                current_chunk = tentative
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_long_sentence(self, sentence: str, max_len: int) -> List[str]:
        """Divide una oración muy larga en partes más pequeñas."""
        words = sentence.split()
        parts: List[str] = []
        current = ""

        for word in words:
            tentative = f"{current} {word}".strip()
            if len(tentative) <= max_len:
                current = tentative
            else:
                if current:
                    parts.append(current)
                current = word

        if current:
            parts.append(current)

        return parts

    def stop(self) -> None:
        """Detiene la lectura actual."""
        try:
            self.engine.stop()
        except Exception:
            pass

    def speak_text(
        self,
        text: str,
        *,
        announce_start: bool = False,
        chunked: bool = True,
    ) -> bool:
        """
        Lee un texto en voz alta.

        Devuelve True si pudo leer algo.
        Devuelve False si no había texto o hubo error.
        """
        if not text or not text.strip():
            print("\nNo hay texto para leer.\n")
            return False

        cleaned_text = self._clean_text(text)

        try:
            if announce_start and self.config.announce_actions:
                self.engine.say("Voy a leer el texto.")
                self.engine.runAndWait()

            if chunked:
                chunks = self._split_text_into_chunks(cleaned_text)
            else:
                chunks = [cleaned_text]

            for chunk in chunks:
                self.engine.say(chunk)
                self.engine.runAndWait()
                if self.config.pause_between_chunks > 0:
                    time.sleep(self.config.pause_between_chunks)

            return True

        except Exception as error:
            print(f"\nOcurrió un error al leer el texto: {error}\n")
            return False

    def accessible_message(
        self,
        message: str,
        *,
        read_aloud: Optional[bool] = None,
        add_pause: bool = False,
    ) -> None:
        """
        Muestra un mensaje claro en pantalla y opcionalmente lo lee en voz alta.
        """
        print(f"\n{message}")

        should_read = self.config.read_screen_messages if read_aloud is None else read_aloud

        if should_read:
            try:
                self.engine.say(message)
                self.engine.runAndWait()
                if add_pause:
                    time.sleep(0.2)
            except Exception as error:
                print(f"\nNo se pudo leer el mensaje en voz alta: {error}\n")


def create_tts(
    rate: int = 145,
    volume: float = 1.0,
    voice_index: Optional[int] = None,
    voice_name_contains: Optional[str] = None,
    preferred_language: Optional[str] = "es",
    pause_between_chunks: float = 0.15,
    max_chunk_length: int = 350,
    read_screen_messages: bool = True,
    announce_actions: bool = True,
) -> AccessibleTTS:
    """Crea una instancia configurable del lector."""
    config = TTSConfig(
        rate=rate,
        volume=volume,
        voice_index=voice_index,
        voice_name_contains=voice_name_contains,
        preferred_language=preferred_language,
        pause_between_chunks=pause_between_chunks,
        max_chunk_length=max_chunk_length,
        read_screen_messages=read_screen_messages,
        announce_actions=announce_actions,
    )
    return AccessibleTTS(config)


# Instancia por defecto lista para usar
_default_tts = create_tts()


def speak_text(text: str) -> bool:
    """Función simple para leer texto usando la instancia por defecto."""
    return _default_tts.speak_text(text)


def accessible_message(message: str, read_aloud: bool = True) -> None:
    """Función simple para mostrar y leer mensajes accesibles."""
    _default_tts.accessible_message(message, read_aloud=read_aloud)


def list_available_voices() -> List[dict]:
    """Devuelve las voces disponibles de la instancia por defecto."""
    return _default_tts.list_available_voices()


def print_available_voices() -> None:
    """Imprime las voces disponibles de la instancia por defecto."""
    _default_tts.print_available_voices()