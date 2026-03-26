"""
simplifier.py

Módulo para simplificar texto y hacerlo más fácil de comprender.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SimplificationResult:
    original_text: str
    simplified_text: str
    replacements_made: List[Tuple[str, str]]
    sentence_count: int
    word_count: int


REPLACEMENTS: Dict[str, str] = {
    "posteriormente": "después",
    "anteriormente": "antes",
    "deberá": "debe",
    "deberán": "deben",
    "dirigirse": "ir",
    "consumir": "comer",
    "alimentos": "comida",
    "alimentación": "comida",
    "finalizar": "terminar",
    "iniciar": "empezar",
    "aproximadamente": "más o menos",
    "visualizar": "ver",
    "adicionalmente": "además",
    "requerido": "necesario",
    "requerida": "necesaria",
    "asistencia": "ayuda",
    "comunicarse": "hablar",
    "seleccionar": "elegir",
    "incorrecto": "mal",
    "correcto": "bien",
    "menor": "más pequeño",
    "mayor": "más grande",
    "realizar": "hacer",
    "solicitar": "pedir",
    "indicar": "decir",
    "observar": "mirar",
    "responder": "contestar",
    "utilizar": "usar",
    "completar": "terminar",
    "ingresar": "escribir",
    "presionar": "apretar",
    "opción": "opción",
    "procedimiento": "paso",
    "ubicación": "lugar",
    "dificultad": "problema",
    "capacidad": "habilidad",
    "información": "dato",
    "estudiante": "alumno",
    "docente": "profesor",
    "posterior": "después",
    "previo": "antes",
}


def normalize_text(text: str) -> str:
    """Limpia espacios innecesarios."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_long_sentences(text: str, max_words: int = 12) -> str:
    """
    Divide oraciones largas usando comas o grupos de palabras.
    No es perfecto, pero ayuda bastante en textos difíciles.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    processed_sentences = []

    for sentence in sentences:
        words = sentence.split()
        if len(words) <= max_words:
            processed_sentences.append(sentence)
            continue

        parts = []
        current_part = []

        for word in words:
            current_part.append(word)
            if len(current_part) >= max_words:
                parts.append(" ".join(current_part))
                current_part = []

        if current_part:
            parts.append(" ".join(current_part))

        rebuilt = ". ".join(part.strip() for part in parts if part.strip())
        if rebuilt and rebuilt[-1] not in ".!?":
            rebuilt += "."
        processed_sentences.append(rebuilt)

    return " ".join(processed_sentences)


def replace_complex_words(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Reemplaza palabras complejas por otras más simples.
    """
    replacements_made: List[Tuple[str, str]] = []
    simplified_text = text

    for complex_word, simple_word in REPLACEMENTS.items():
        pattern = rf"\b{re.escape(complex_word)}\b"

        if re.search(pattern, simplified_text, flags=re.IGNORECASE):
            matches = re.findall(pattern, simplified_text, flags=re.IGNORECASE)
            for _ in matches:
                replacements_made.append((complex_word, simple_word))

            simplified_text = re.sub(
                pattern,
                simple_word,
                simplified_text,
                flags=re.IGNORECASE,
            )

    return simplified_text, replacements_made


def simplify_text(text: str) -> SimplificationResult:
    """
    Simplifica un texto y devuelve un resultado estructurado.
    """
    original_text = text
    text = normalize_text(text)

    simplified_text, replacements_made = replace_complex_words(text)
    simplified_text = simplified_text.replace(";", ".")
    simplified_text = simplified_text.replace(":", ".")
    simplified_text = simplified_text.replace(",", ".")
    simplified_text = normalize_text(simplified_text)
    simplified_text = split_long_sentences(simplified_text, max_words=12)
    simplified_text = normalize_text(simplified_text)

    sentence_count = len([s for s in re.split(r"[.!?]+", simplified_text) if s.strip()])
    word_count = len(simplified_text.split())

    return SimplificationResult(
        original_text=original_text,
        simplified_text=simplified_text,
        replacements_made=replacements_made,
        sentence_count=sentence_count,
        word_count=word_count,
    )


def get_simplification_summary(result: SimplificationResult) -> str:
    """Genera un resumen breve del proceso de simplificación."""
    changes = len(result.replacements_made)

    if changes == 0:
        return (
            f"El texto simplificado tiene {result.word_count} palabras y "
            f"{result.sentence_count} oraciones. No se hicieron reemplazos de palabras."
        )

    return (
        f"El texto simplificado tiene {result.word_count} palabras y "
        f"{result.sentence_count} oraciones. "
        f"Se hicieron {changes} cambios para facilitar la comprensión."
    )    "requerido": "necesario",
    "requerida": "necesaria",
    "asistencia": "ayuda",
    "comunicarse": "hablar",
    "seleccionar": "elegir",
    "incorrecto": "mal",
    "correcto": "bien",
    "menor": "más pequeño",
    "mayor": "más grande",
    "realizar": "hacer",
    "solicitar": "pedir",
    "indicar": "decir",
    "observar": "mirar",
    "responder": "contestar",
    "utilizar": "usar",
    "completar": "terminar",
    "ingresar": "escribir",
    "presionar": "apretar",
    "opción": "opción",
    "procedimiento": "paso",
    "ubicación": "lugar",
    "dificultad": "problema",
    "capacidad": "habilidad",
    "información": "dato",
    "estudiante": "alumno",
    "docente": "profesor",
    "posterior": "después",
    "previo": "antes",
}


def normalize_text(text: str) -> str:
    """Limpia espacios innecesarios."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_long_sentences(text: str, max_words: int = 12) -> str:
    """
    Divide oraciones largas usando comas o grupos de palabras.
    No es perfecto, pero ayuda bastante en textos difíciles.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    processed_sentences = []

    for sentence in sentences:
        words = sentence.split()
        if len(words) <= max_words:
            processed_sentences.append(sentence)
            continue

        parts = []
        current_part = []

        for word in words:
            current_part.append(word)
            if len(current_part) >= max_words:
                parts.append(" ".join(current_part))
                current_part = []

        if current_part:
            parts.append(" ".join(current_part))

        rebuilt = ". ".join(part.strip() for part in parts if part.strip())
        if rebuilt and rebuilt[-1] not in ".!?":
            rebuilt += "."
        processed_sentences.append(rebuilt)

    return " ".join(processed_sentences)


def replace_complex_words(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Reemplaza palabras complejas por otras más simples.
    """
    replacements_made: List[Tuple[str, str]] = []
    simplified_text = text

    for complex_word, simple_word in REPLACEMENTS.items():
        pattern = rf"\b{re.escape(complex_word)}\b"

        if re.search(pattern, simplified_text, flags=re.IGNORECASE):
            matches = re.findall(pattern, simplified_text, flags=re.IGNORECASE)
            for _ in matches:
                replacements_made.append((complex_word, simple_word))

            simplified_text = re.sub(
                pattern,
                simple_word,
                simplified_text,
                flags=re.IGNORECASE,
            )

    return simplified_text, replacements_made


def simplify_text(text: str) -> SimplificationResult:
    """
    Simplifica un texto y devuelve un resultado estructurado.
    """
    original_text = text
    text = normalize_text(text)

    simplified_text, replacements_made = replace_complex_words(text)
    simplified_text = simplified_text.replace(";", ".")
    simplified_text = simplified_text.replace(":", ".")
    simplified_text = simplified_text.replace(",", ".")
    simplified_text = normalize_text(simplified_text)
    simplified_text = split_long_sentences(simplified_text, max_words=12)
    simplified_text = normalize_text(simplified_text)

    sentence_count = len([s for s in re.split(r"[.!?]+", simplified_text) if s.strip()])
    word_count = len(simplified_text.split())

    return SimplificationResult(
        original_text=original_text,
        simplified_text=simplified_text,
        replacements_made=replacements_made,
        sentence_count=sentence_count,
        word_count=word_count,
    )


def get_simplification_summary(result: SimplificationResult) -> str:
    """Genera un resumen breve del proceso de simplificación."""
    changes = len(result.replacements_made)

    if changes == 0:
        return (
            f"El texto simplificado tiene {result.word_count} palabras y "
            f"{result.sentence_count} oraciones. No se hicieron reemplazos de palabras."
        )

    return (
        f"El texto simplificado tiene {result.word_count} palabras y "
        f"{result.sentence_count} oraciones. "
        f"Se hicieron {changes} cambios para facilitar la comprensión."
    )
