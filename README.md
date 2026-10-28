# RE Skills

Repozytorium naszych skilli do reverse engineeringu. Obecnie obsługuje **Codexa**;
wspólne instrukcje są oddzielone od adaptera agenta.

| Skill | Zastosowanie |
| --- | --- |
| [game-reverse-engineering-repo](skills/game-reverse-engineering-repo/SKILL.md) | Zakładanie i organizowanie repozytoriów RE gier |
| [ghidra-re-investigation](skills/ghidra-re-investigation/SKILL.md) | Badanie binariów i dokumentowanie potwierdzonych ustaleń w Ghidrze |
| [binary-patch-engineering](skills/binary-patch-engineering/SKILL.md) | Odwracalne patche, eksperymenty, walidacja i pakowanie |

## Przygotowanie i budowanie

Wymagania: Python 3.11+ i Git. Narzędzia działają z dowolnego katalogu roboczego;
poniższe polecenia zakładają uruchomienie w katalogu repozytorium.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python scripts/re_skills.py validate
.venv/Scripts/python -m unittest discover -s tests -v
.venv/Scripts/python scripts/re_skills.py build --agent codex
```

Na Linux/macOS użyj `.venv/bin/python` zamiast `.venv/Scripts/python`.

Powstaje `dist/codex/`: plugin `re-skills/` z manifestem `plugin.json`, kompletem
skilli i metadanymi OpenAI oraz lokalny katalog pluginów
`.agents/plugins/marketplace.json`. Kolejny build wymaga usunięcia poprzedniego
wyniku albo jawnego `build --agent codex --replace`; zastępowanie dotyczy wyłącznie
katalogu tego adaptera w `dist/`.

## Użycie w Codexie

Po zbudowaniu dodaj wygenerowany marketplace:

```powershell
codex plugin marketplace add ./dist/codex
```

Uruchom ponownie aplikację desktopową, wybierz źródło **re-skills-local** w katalogu
pluginów i zainstaluj **RE Skills**. Rozpocznij nowy czat. Po zmianach w źródłach
przebuduj pakiet, odśwież marketplace i instalację pluginu, a następnie rozpocznij
nowy czat. Aplikacja ładuje zainstalowaną kopię, więc samo edytowanie repozytorium
nie aktualizuje aktywnego skilla.

Format pakietu i sposób rejestrowania lokalnego marketplace są opisane w
[oficjalnej dokumentacji OpenAI](https://developers.openai.com/plugins/build/plugins).
Build przygotowuje pliki; nie instaluje pluginu ani nie zmienia konfiguracji agenta.

Przykładowe wywołanie po instalacji:

```text
Użyj $ghidra-re-investigation, żeby zbadać przyczynę tego zachowania binarki
i zapisać potwierdzone nazwy, typy oraz komentarze w projekcie Ghidry.
```

Skill Ghidry wymaga osobno działającej Ghidry i zgodnego serwera MCP udostępniającego
odkrywanie instancji, wybór programu, analizę oraz zapis dokumentacji. Pakiet zawiera
instrukcje, nie serwer MCP. Nie dostarcza gotowego adresu ani konfiguracji połączenia;
są one lokalne dla konkretnego projektu.

## Rozwój

- `skills/` — pojedyncze źródło instrukcji, referencji i szablonów.
- `adapters/codex/` — manifest pakietu i metadane UI dla Codexa.
- `re-skills.json` — tożsamość, wersja i lista publikowanych skilli.
- `scripts/` — wspólna walidacja, składanie i rejestr adapterów.
- `tests/` — testy pakowania, zachowania zasobów i ochrony źródeł.
- `dist/` — ignorowane wyniki budowania.

Kontrakt adapterów i procedura dodania kolejnego agenta:
[architektura](docs/architecture.md). Pochodzenie aktualnej zawartości:
[import skilli](docs/import.md).

Repozytorium jest przygotowane lokalnie. Publikacja do zdalnego repozytorium i
wybór licencji pozostają odrębnymi decyzjami; pakiet nie deklaruje wymyślonej
licencji ani adresu zdalnego repozytorium.
