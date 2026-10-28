# Import aktualnych skilli

Stan początkowy skopiowano 2026-10-28 z lokalnego katalogu `~/.codex/skills/`:

- `game-reverse-engineering-repo`
- `ghidra-re-investigation`
- `binary-patch-engineering`
- `readable-code` — dodany po uzupełnieniu zakresu o zasady pisania kodu,
  formatowania i refaktoryzacji

Podczas importu zachowano treść `SKILL.md`, wszystkie referencje i szablony. Oryginalne
`agents/openai.yaml` przeniesiono bez zmian do
`adapters/codex/skills/<skill-id>/openai.yaml`; build umieszcza je ponownie
w `skills/<skill-id>/agents/openai.yaml` w wynikowym pluginie.

Po review skrócono `readable-code`, zachowując preferencje formatowania i ogólne
zasady refaktoryzacji. Usunięto szczegóły dotyczące runtime'ów, diagnostyki oraz
konkretnych mechanizmów testowania. Metadane OpenAI pozostały bez zmian.

Import obejmuje trzy skille RE i wspólny skill `readable-code`. Nie obejmuje skilli
do zarządzania skillami ani integracji z innymi usługami.
Odwołania między skillami RE zachowują dotychczasowe identyfikatory.

Od tej chwili źródłem zmian dla tego pakietu jest repozytorium. Zmiany w globalnie
zainstalowanych skillach nie synchronizują się automatycznie. Aktualizacje z tych
kopii należy porównać, przenieść wraz z zasobami i zweryfikować. Zastępowanie
istniejących globalnych instalacji nie jest częścią budowania pluginu.
