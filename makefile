.PHONY: up down reset logs simulate bridge test lint
up:        ; docker compose up -d
down:      ; docker compose down
reset:     ; docker compose down -v
logs:      ; docker compose logs -f
simulate:  ; python -m simulator.run
bridge:    ; python -m bridge.run
test:      ; pytest -q
lint:      ; ruff check .