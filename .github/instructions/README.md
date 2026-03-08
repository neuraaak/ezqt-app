# ezqt_app - Guide de Projet

Guide de référence pour comprendre, maintenir et faire évoluer la bibliothèque **ezqt_app**.
Ce document décrit la structure du projet, ses conventions et les pratiques à suivre pour contribuer dans la continuité de l'existant.

---

## Vue d'ensemble

**ezqt_app** est une bibliothèque Python modulaire pour créer des applications desktop modernes avec PySide6.
Elle propose une gestion intégrée des ressources, thèmes, widgets réutilisables et outils CLI, adaptée à un environnement corporate (proxy, Windows).

| Donnée        | Valeur                                     |
| ------------- | ------------------------------------------ |
| Python        | >= 3.10                                    |
| Framework Qt  | PySide6 >= 6.7.3, < 7.0.0                  |
| Build backend | setuptools (PEP 517) — `src/` layout       |
| Licence       | MIT                                        |
| Statut        | Production/Stable                          |
| Configuration | `pyproject.toml` (source unique de vérité) |

---

## Objectif de migration v5

La v5 impose une architecture explicite, stable et maintenable dans le temps.

Le modèle retenu est une **architecture hexagonale adaptée** (Ports & Adapters), appliquée à une bibliothèque Qt.
Ce choix résout le problème central de la v4 : le `kernel` monolithique était le centre de gravité réel, rendant impossible le test unitaire et le remplacement des composants.

En hexagonale, c'est le **domaine** (contrats purs) qui est au centre, pas l'infrastructure.

---

## Architecture hexagonale — principe

```text
┌──────────────────────────────────────────────────────────┐
│  PRESENTATION (widgets/)                                 │
│    Qt widgets, UI uniquement, aucune logique métier      │
│                        │                                 │
│              appelle via ports                           │
│                        ↓                                 │
│  APPLICATION (services/)                                 │
│    Implémentations concrètes des ports (Adapters)        │
│    Orchestration, cas d'usage                            │
│                        │                                 │
│              implémente                                  │
│                        ↓                                 │
│  DOMAINE (domain/)   ← CENTRE ─────────────────────────  │
│    domain/ports/   : Protocoles abstraits (les "Ports")  │
│    domain/models/  : Dataclasses, TypedDicts (à venir)   │
│                        ↑                                 │
│              dépend de                                   │
│                        │                                 │
│  INFRASTRUCTURE (kernel/)                                │
│    Adaptateurs techniques, façade legacy transitoire     │
└──────────────────────────────────────────────────────────┘
         shared/   : types transverses multi-couches
         utils/    : helpers techniques purs (sans domaine)
```

### Règle de dépendance fondamentale

> **Le domaine ne dépend de rien. Tout dépend du domaine.**

- `domain/ports/` → aucune dépendance externe (ni Qt, ni kernel)
- `services/` → implémente les ports, peut dépendre de `kernel/` (phase transitoire)
- `widgets/` → appelle les services via les ports, ne dépend jamais de `kernel/` directement
- `kernel/` → couche résiduelle legacy, doit être progressivement vidée

---

## Structure du projet (`src/` layout)

```text
src/
  ezqt_app/
    domain/               ← DOMAINE (centre architectural)
      ports/              ← Contrats abstraits (Protocols Python)
      models/             ← Dataclasses, structures de données (à venir)
    services/             ← ADAPTERS (implémentations des ports)
      config/
      runtime/
      settings/
      translation/
      ui/
      protocols/          ← Shim de compat (re-export depuis domain.ports)
    shared/               ← Types transverses (migration vers domain/models/ prévue)
    utils/                ← Helpers techniques réutilisables
    kernel/               ← Infrastructure legacy (façade transitoire)
    widgets/              ← Couche présentation Qt
    cli/                  ← Interface ligne de commande
    resources/            ← Ressources statiques (themes, fonts, icons)
tests/
pyproject.toml
```

### Pourquoi `src/` layout ?

Le package source est dans `src/ezqt_app/` (PEP 517 best practice).
Cela empêche les imports accidentels depuis la racine et force l'installation explicite du package :

```bash
pip install -e .   # développement
pip install .      # production
```

---

## Responsabilités par couche

| Couche           | Chemin           | Rôle                                | Dépendances autorisées                                  |
| ---------------- | ---------------- | ----------------------------------- | ------------------------------------------------------- |
| Domaine — Ports  | `domain/ports/`  | Contrats abstraits (`Protocol`)     | Aucune                                                  |
| Domaine — Models | `domain/models/` | Dataclasses, TypedDicts             | stdlib uniquement                                       |
| Services         | `services/*/`    | Implémentations concrètes des ports | `domain/`, `shared/`, `utils/`, `kernel/` (transitoire) |
| Shared           | `shared/`        | Structures de données transverses   | stdlib, PySide6 minimal                                 |
| Utils            | `utils/`         | Helpers techniques purs             | stdlib, PySide6                                         |
| Kernel           | `kernel/`        | Façade legacy, bootstrap            | Tout (couche d'infrastructure)                          |
| Widgets          | `widgets/`       | Composants Qt (présentation)        | `services/`, `shared/`, `utils/`                        |
| CLI              | `cli/`           | Interface commandes                 | `services/`, `kernel/`                                  |

---

## Ports & Adapters — comment ça fonctionne

### Port (contrat abstrait)

Un port est un `Protocol` Python dans `domain/ports/`. Il définit le **quoi**, pas le **comment**.

```python
# domain/ports/config_service.py
class ConfigServiceProtocol(Protocol):
    def load_config(self, config_name: str) -> dict[str, Any]: ...
    def save_config(self, config_name: str, data: dict[str, Any]) -> bool: ...
```

### Adapter (implémentation concrète)

Un adapter dans `services/` implémente le port via duck typing (structural subtyping).

```python
# services/config/config_service.py
class ConfigService:  # satisfait ConfigServiceProtocol implicitement
    def load_config(self, config_name: str) -> dict[str, Any]:
        return get_config_manager().load_config(config_name)
```

### Consommateur (widget ou service)

Le consommateur dépend du **port**, pas de l'adapter. Il est découplé de l'infrastructure.

```python
# widgets/core/some_widget.py
from ezqt_app.services.config import get_config_service
# ou, typé via le port :
from ezqt_app.domain.ports import ConfigServiceProtocol
```

---

## Règles de dépendances (enforceable)

```text
domain/      →  rien
utils/       →  stdlib, PySide6
shared/      →  stdlib, PySide6 minimal
services/    →  domain/, shared/, utils/, kernel/ (transitoire)
widgets/     →  services/, shared/, utils/
cli/         →  services/, kernel/ (CLI tools)
kernel/      →  tout (couche infrastructure)
```

**Interdictions explicites :**

- `domain/` ne doit jamais importer depuis `services/`, `kernel/`, `widgets/`
- `widgets/` ne doit jamais importer directement depuis `kernel/`
- `shared/` ne doit pas importer depuis `kernel/`
- Aucun wildcard import (`from x import *`) en dehors de `kernel/` legacy

---

## Stratégie d'imports — contrat public vs relais internes

La structure interne du package est un **détail d'implémentation**. L'utilisateur ne doit jamais en dépendre directement.

### Rôle de chaque `__init__.py`

```text
domain/__init__.py          → agrège pour que services/ importe proprement
services/__init__.py        → agrège pour les consommateurs internes (widgets, cli)
kernel/__init__.py          → intentionnellement minimal (façade legacy uniquement)
ezqt_app/__init__.py        → SEUL fichier que l'utilisateur connaît, avec __all__
```

**Principe clé** : si l'utilisateur peut écrire `from ezqt_app.services.config.config_service import ConfigService` et que ça fonctionne, la stratégie d'exports est cassée. Les chemins internes doivent être des détails opaques.

### Test de cohérence

> Si on renomme un fichier interne et que le code utilisateur casse, la stratégie d'exports est mal faite.

Seul `ezqt_app/__init__.py` (et ce qu'il expose via `__all__`) constitue le contrat public stable.

### Trois outils complémentaires

| Outil                                          | Rôle                                                                            | Exemple                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `__all__` dans `ezqt_app/__init__.py`          | Documentation machine-readable de l'API publique                                | `__all__ = ["EzQt_App", "EzApplication"]`                 |
| Préfixe `_` sur les classes/fonctions internes | Signal "privé" sans interdiction technique                                      | `_config_service = ConfigService()`                       |
| `if TYPE_CHECKING:`                            | Imports uniquement pour annotations, évite les circulaires et allège le runtime | `from ezqt_app.domain.ports import ConfigServiceProtocol` |

### Application dans ce projet

```python
# ezqt_app/__init__.py — seul contrat public
from .app import EzQt_App
from .widgets.core.ez_app import EzApplication
# ...
__all__ = ["EzQt_App", "EzApplication", "init"]

# domain/__init__.py — agrégat interne pour services/
from .ports import ConfigServiceProtocol, SettingsServiceProtocol
# ...

# services/__init__.py — agrégat interne pour widgets/ et cli/
from .config import get_config_service
from .settings import get_settings_service
# ...
```

---

## Shims de compatibilité

Les shims permettent aux imports legacy de continuer à fonctionner sans modification
pendant la migration progressive vers la nouvelle architecture.

| Shim                                     | Pointe vers                         | État  |
| ---------------------------------------- | ----------------------------------- | ----- |
| `kernel/app_functions/config_manager.py` | `services/config/config_service.py` | actif |
| `shared/runtime/specs.py`                | `domain/models/runtime.py`          | actif |
| `shared/ui/specs.py`                     | `domain/models/ui.py`               | actif |

> `services/protocols/` a été **supprimé** — tous les consommateurs importent désormais directement depuis `domain.ports`.

---

## Principes fondamentaux v5 (qualité)

1. **Source unique de vérité** : Toute configuration centralisée dans `pyproject.toml`.
2. **Architecture hexagonale** : Les ports définissent les contrats, les adapters les implémentent.
3. **Type hints obligatoires** : Tous les modules et fonctions doivent être typés.
4. **Docstrings Google** : Style Google pour toute documentation de fonction/classe.
5. **Formatage strict** : PEP 8, ruff, black, isort.
6. **Tests systématiques** : Toute nouvelle fonctionnalité couverte par des tests pytest.
7. **Atomic commits** : Un commit = une modification logique, message structuré.
8. **CI/CD** : Validation lint, tests et couverture via GitHub Actions.
9. **Gestion des dépendances** : Wheels locales, pas de dépendances non vérifiées.
10. **Sécurité** : Jamais de credentials ou données sensibles dans le code.
11. **Documentation vivante** : Toute évolution documentée dans ce README et les docstrings.
12. **Instructions hiérarchisées** : En cas de conflit, suivre la priorité ci-dessous.
13. **Proxy/Environnement** : Code adapté à l'environnement corporate (proxy, Windows).
14. **Revue de code** : Toute PR relue et validée avant merge.

---

## Hiérarchie des instructions

1. **Ce fichier** (`README.md`) - Contexte projet et architecture
2. `core/advanced-cognitive-conduct.instructions.md` - Principes de raisonnement
3. `languages/python/python-development-standards.instructions.md` - Standards Python
4. `languages/python/python-formatting-standards.instructions.md` - Formatage et sections
5. `languages/python/pyproject-standards.instructions.md` - Standards pyproject.toml
6. `CLAUDE.md` (racine) - Préférences spécifiques à Claude
7. `AGENTS.md` (racine) - Instructions générales pour agents IA

En cas de conflit, le fichier le plus haut dans cette liste prévaut.

---

## Standards de code obligatoires

### Langue

- Tous les **docstrings** doivent être en anglais.
- Tous les **commentaires techniques** doivent être en anglais.
- Les messages utilisateurs peuvent suivre la langue du contexte produit.

### Structure des modules Python

Ordre recommandé :

1. Header section du module
2. Module docstring
3. `from __future__ import annotations`
4. Sections d'imports (`standard`, `third-party`, `local`)
5. Sections de code (`CLASSES`, `FUNCTIONS`, `PUBLIC API`, etc.)

Exigences :

- Utiliser les séparateurs de sections standard du projet.
- Éviter les sections vides inutiles.
- Maintenir un style homogène avec les modules v5 déjà créés.

### Qt / PySide6

- Préférer les enums Qt6 typés (`QEvent.Type`, `Qt.WindowType`, `Qt.WidgetAttribute`, `Qt.MouseButton`, `Qt.Edge`, etc.).
- Éviter les accès legacy susceptibles de casser les vérifications statiques.

### Gestion d'erreurs

- Éviter `except: pass`.
- Utiliser des mécanismes explicites (`warnings`, logging structuré, ou remontée d'exception selon le contexte).
- Les exceptions silencieuses sont interdites.

---

## Méthode de migration recommandée

Pour tout refactor architectural :

1. **Cartographier** les usages et dépendances.
2. **Écrire le port** dans `domain/ports/` si absent.
3. **Migrer** l'implémentation dans `services/`.
4. **Basculer** les consommateurs vers le service.
5. **Supprimer** le code legacy devenu inutilisé.
6. **Nettoyer** les exports publics et la documentation.

Règle clé : ne pas laisser une architecture hybride durable.
Chaque migration doit réduire le couplage vers `kernel/`.

---

## Critères d'acceptation d'un changement

Un changement est considéré conforme si :

- Il respecte la hiérarchie des instructions.
- Il respecte l'architecture hexagonale (ports → adapters → présentation).
- Il n'ajoute pas de dépendance directe vers `kernel/` depuis `widgets/` ou `domain/`.
- Il suit les conventions de formatage du projet.
- Il n'introduit pas de nouvelle dette legacy.
- Il passe les vérifications statiques/lint/tests applicables.

---

## Cycle de vie projet

- Toute évolution doit respecter cette charte.
- Les incohérences ou conflits doivent être remontés et résolus selon la hiérarchie ci-dessus.
- Les standards sont évolutifs mais toute modification doit être validée en équipe.

---

_Document de référence à appliquer avant toute action de génération, refactor ou migration._
