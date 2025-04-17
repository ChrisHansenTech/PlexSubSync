"""
Functions to locate and select subtitle files matching language codes.
"""
import os
import glob
from .config import PLEX_LIBRARY_DIR

def find_matching_srt(video_file: str, sub_lang: str) -> str | None:
    """
    Find a subtitle file in the same directory as the video that matches the given
    ISO-639-1 subtitle language code (e.g., 'en', 'es').
    Falls back to ISO-639-2 code if no ISO-639-1 match is found.
    Does not match '.forced' subtitle files. If the only subtitle file detected
    has no language code, returns None to signal an error.
    """
    video_dir = os.path.join(PLEX_LIBRARY_DIR, os.path.dirname(video_file))
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    pattern = os.path.join(video_dir, f"{video_name}*.srt")
    print(f"Searching for subtitles in {video_dir} matching '{video_name}*.srt'")
    all_candidates = glob.glob(pattern)
    candidates = [c for c in all_candidates if ".forced" not in os.path.basename(c).lower()]

    if not candidates:
        return None

    def parts(path: str) -> list[str]:
        name = os.path.splitext(os.path.basename(path))[0]
        return [p.lower() for p in name.split('.')]

    iso1 = sub_lang.lower()
    iso1_matches = [c for c in candidates if iso1 in parts(c)[1:]]
    if iso1_matches:
        print(f"Found ISO-639-1 subtitle(s): {iso1_matches}")
        return iso1_matches[0]

    ISO_639_1_TO_2 = {
        "aa": "aar", "ab": "abk", "af": "afr", "ak": "aka", "sq": "sqi",
        "am": "amh", "ar": "ara", "an": "arg", "hy": "hye", "as": "asm",
        "av": "ava", "ae": "ave", "ay": "aym", "az": "aze", "ba": "bak",
        "bm": "bam", "eu": "eus", "be": "bel", "bn": "ben", "bh": "bih",
        "bi": "bis", "bo": "bod", "bs": "bos", "br": "bre", "bg": "bul",
        "my": "mya", "ca": "cat", "cs": "ces", "ce": "che", "zh": "zho",
        "cu": "chu", "cv": "chv", "kw": "cor", "co": "cos", "cr": "cre",
        "cy": "cym", "da": "dan", "de": "deu", "dv": "div", "dz": "dzo",
        "el": "ell", "en": "eng", "eo": "epo", "et": "est", "ee": "ewe",
        "fo": "fao", "fa": "fas", "fj": "fij", "fi": "fin", "fr": "fra",
        "fy": "fry", "ff": "ful", "gd": "gla", "gl": "glg", "lg": "lug",
        "ka": "kat", "gu": "guj", "ht": "hat", "ha": "hau", "he": "heb",
        "hz": "her", "hi": "hin", "ho": "hmo", "hr": "hrv", "hu": "hun",
        "ig": "ibo", "io": "ido", "ii": "iii", "iu": "iku", "ie": "ile",
        "ia": "ina", "id": "ind", "ik": "ipk", "is": "isl", "it": "ita",
        "ja": "jpn", "jv": "jav", "kn": "kan", "kr": "kau", "ks": "kas",
        "kk": "kaz", "km": "khm", "ki": "kik", "rw": "kin", "ky": "kir",
        "kv": "kom", "kg": "kon", "ko": "kor", "kj": "kua", "ku": "kur",
        "lo": "lao", "la": "lat", "lv": "lav", "li": "lim", "ln": "lin",
        "lt": "lit", "lb": "ltz", "lu": "lub", "mk": "mkd", "mh": "mah",
        "ml": "mal", "mi": "mri", "mr": "mar", "ms": "msa", "mg": "mlg",
        "mt": "mlt", "mn": "mon", "na": "nau", "nv": "nav", "nr": "nbl",
        "nd": "nde", "ng": "ndo", "ne": "nep", "nn": "nno", "nb": "nob",
        "no": "nor", "oc": "oci", "oj": "oji", "or": "ori", "om": "orm",
        "os": "oss", "pa": "pan", "pi": "pli", "pl": "pol", "pt": "por",
        "qu": "que", "rm": "roh", "ro": "ron", "rn": "run", "ru": "rus",
        "sg": "sag", "sa": "san", "si": "sin", "sk": "slk", "sl": "slv",
        "se": "sme", "sm": "smo", "sn": "sna", "sd": "snd", "so": "som",
        "st": "sot", "es": "spa", "sc": "srd", "sr": "srp", "ss": "ssw",
        "su": "sun", "sw": "swa", "sv": "swe", "ty": "tah", "ta": "tam",
        "tt": "tat", "te": "tel", "tg": "tgk", "tl": "tgl", "th": "tha",
        "ti": "tir", "to": "ton", "tn": "tsn", "ts": "tso", "tk": "tuk",
        "tr": "tur", "tw": "twi", "ug": "uig", "uk": "ukr", "ur": "urd",
        "uz": "uzb", "ve": "ven", "vi": "vie", "vo": "vol", "wa": "wln",
        "wo": "wol", "xh": "xho", "yi": "yid", "yo": "yor", "za": "zha",
        "zu": "zul"
    }
    iso2 = ISO_639_1_TO_2.get(iso1)
    if iso2:
        iso2_matches = [c for c in candidates if iso2 in parts(c)[1:]]
        if iso2_matches:
            print(f"Found ISO-639-2 subtitle(s): {iso2_matches}")
            return iso2_matches[0]

    if len(candidates) == 1 and parts(candidates[0]) == [video_name]:
        print(f"Error: Subtitle file '{candidates[0]}' has no language code.")
        return None

    return None