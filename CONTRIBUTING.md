# Конвенція комітів (Conventional Commits)

Проєкт використовує [Conventional Commits](https://www.conventionalcommits.org/) для історії комітів.

## Формат

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

## Типи (type)

- **feat** — нова функціональність
- **fix** — виправлення помилки
- **docs** — зміни в документації
- **style** — форматування, відступи (не зміна коду)
- **refactor** — рефакторинг без зміни поведінки
- **test** — додавання або зміна тестів
- **chore** — зміни в збірці, залежностях, конфігурації

## Приклади

```bash
feat(api): add endpoint for session history
fix(ui): show error when API key is missing
docs: update README with new project structure
refactor(services): move config to app.config
chore(deps): add pydantic-settings
```

## Scope (опційно)

- `api` — маршрути та ендпоінти
- `ui` / `frontend` — інтерфейс
- `config` — конфігурація, .env
- `db` — база даних, моделі

Коміти краще робити дрібними логічними кроками — так історія стане зрозумілою для підтримки.
