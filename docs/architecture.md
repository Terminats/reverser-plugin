# Wspólne skille i adaptery agentów

## Granice

`skills/<id>/` zawiera workflow i jego zasoby. Instrukcje opisują pracę z dowodami,
stanem projektu i odwracalnymi zmianami. Ich identyfikatory nie zależą od nazwy
agenta. Każdy pakiet otrzymuje pełne drzewo referencji i szablonów; build nie
spłaszcza ścieżek ani nie podmienia instrukcji ukrytymi zamianami tekstu.

`re-skills.json` określa wersję formatu katalogu, tożsamość pakietu, wersję wydania
i kolejność skilli. `scripts/re_skills.py` waliduje katalog, YAML i lokalne linki.
Obecny format to `1`; nieznane wersje są odrzucane.

Adapter implementuje `validate(root, catalog)` oraz
`build(root, catalog, destination)` w `scripts/adapters.py` i ma jawny wpis
w `ADAPTERS`. Wspólny builder wywołuje adapter po walidacji, a wynik tworzy najpierw
w katalogu tymczasowym. Publikacja polega na zmianie nazwy gotowego katalogu.
Przy `--replace` poprzedni wynik jest zachowany do zakończenia publikacji.
Nieznany agent kończy się błędem przed utworzeniem wyniku.

Kod adaptera oraz jego pliki konfiguracyjne są specyficzne dla hosta. Przykład
Codexa: prezentacja pluginu w `adapters/codex/plugin.json`, a metadane skilli
w `adapters/codex/skills/<id>/openai.yaml`. Wynik zawiera przenośny manifest
Agent Plugins z rozszerzeniem `com.openai` i katalog skilli. Tożsamość oraz wersja
są pobierane z katalogu, nie utrzymywane w drugiej kopii manifestu.

## Obecna granica przenośności

Tylko adapter Codexa jest zaimplementowany. Przenośny manifest nie oznacza
zweryfikowanego wsparcia innych hostów.

Referencja `ghidra-re-investigation/references/mcp-connection.md` zachowuje
dotychczasowe nazwy `mcp__ghidra__list_instances` i
`mcp__ghidra__connect_instance`. To powiązanie z aktualną integracją, którego nie
ukrywamy przez samo rozdzielenie katalogów. Wymagane możliwości to:

| Możliwość | Wymagane zachowanie |
| --- | --- |
| Odkrywanie instancji | Rozpoznanie projektu i aktywnego programu |
| Połączenie | Jawny wybór instancji oraz potwierdzenie tożsamości celu |
| Analiza | Funkcje, dekompilacja, xrefy i dane |
| Dokumentacja | Nazwy, typy, sygnatury i komentarze |
| Weryfikacja | Odczyt każdej mutacji z tego samego programu |

Serwer i dane połączenia należą do środowiska użytkownika. Nie pakujemy
przykładowego, niezweryfikowanego endpointu ani projektu Ghidry.

## Dodanie kolejnego agenta

1. Sprawdź jego rzeczywisty format skilli, sposób odkrywania i integrację MCP.
2. Dodaj dane hosta pod `adapters/<agent>/`, implementację adaptera i jawny wpis
   w rejestrze. Nie twórz oddzielnej utrzymywanej kopii wspólnych skilli.
3. Jeżeli nazwy narzędzi Ghidry są inne, wydziel wspólny kontrakt połączenia
   i dodaj referencję adaptera. Zaktualizuj linki jawnie i przetestuj wynik.
   Nie zastępuj globalnie ciągów `Codex` ani nazw narzędzi.
4. Złóż kompletny pakiet z jego metadanymi, wszystkimi referencjami i szablonami.
5. Dodaj testy pakowania oraz sprawdź wykrywanie skilli i workflow z MCP
   w rzeczywistym hoście. Dopiero wtedy opisz tego agenta jako wspieranego.

Build nie łączy się z Ghidrą i nie dowodzi poprawności narzędzi MCP ani zachowania
patchy w grze. Te rzeczy wymagają osobnego, konkretnego celu i środowiska.
