# Import aktualnych skilli

Stan początkowy skopiowano 2026-10-28 z lokalnego katalogu `~/.codex/skills/`:

- `game-reverse-engineering-repo`
- `ghidra-re-investigation`
- `binary-patch-engineering`

Zachowano treść `SKILL.md`, wszystkie referencje i szablony. Oryginalne
`agents/openai.yaml` przeniesiono bez zmian do
`adapters/codex/skills/<skill-id>/openai.yaml`; build umieszcza je ponownie
w `skills/<skill-id>/agents/openai.yaml` w wynikowym pluginie.

Import nie obejmuje ogólnych skilli do programowania, zarządzania skillami ani
integracji z innymi usługami. Te trzy skille nie wymagają ich do załadowania.
Odwołania między skillami RE zachowują dotychczasowe identyfikatory.

Od tej chwili źródłem zmian dla tego pakietu jest repozytorium. Zmiany w globalnie
zainstalowanych skillach nie synchronizują się automatycznie. Aktualizacje z tych
kopii należy porównać, przenieść wraz z zasobami i zweryfikować. Zastępowanie
istniejących globalnych instalacji nie jest częścią budowania pluginu.
