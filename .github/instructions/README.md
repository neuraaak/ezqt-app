# ezqt_app - Guide de Projet

Guide de référence pour comprendre, maintenir et faire évoluer la bibliothèque **ezqt_app**.
Ce document décrit la structure du projet, ses conventions et les pratiques à suivre pour contribuer au développement de cette architecture stabilisée.

---

## Vue d'ensemble

**ezqt_app** est une bibliothèque Python modulaire pour créer des applications desktop modernes avec PySide6.
Elle propose une gestion intégrée des ressources, thèmes, widgets réutilisables et outils CLI, adaptée à un environnement corporate (proxy, Windows).

Le projet a finalisé sa migration vers l'architecture v5, offrant une structure robuste, testable et évolutive.

| Donnée        | Valeur                                     |
| ------------- | ------------------------------------------ |
| Python        | >= 3.11                                    |
| Framework Qt  | PySide6 >= 6.7.3, < 7.0.0                  |
| Build backend | setuptools (PEP 517) — `src/` layout       |
| Licence       | MIT                                        |
| Statut        | Production/Stable (v5)                     |
| Configuration | `pyproject.toml` (source unique de vérité) |

---

## Architecture Hexagonale Stabilisée

Le projet suit une **architecture hexagonale complète** (Ports & Adapters).
Ce modèle place le **domaine** (logique métier et contrats) au centre, isolant les détails techniques et les frameworks (comme Qt) dans des adaptateurs interchangeables.

### Principe de l'Architecture

```text
┌──────────────────────────────────────────────────────────┐
│  PRESENTATION (widgets/)                                 │
│    Composants Qt, UI uniquement, aucune logique métier   │
│                        │                                 │
│              appelle via ports                           │
│                        ↓                                 │
│  APPLICATION (services/)                                 │
│    Implémentations concrètes des ports (Adapters)        │
│    Orchestration et cas d'usage                          │
│                        │                                 │
│              implémente                                  │
│                        ↓                                 │
│  DOMAINE (domain/)   ← CENTRE ─────────────────────────  │
│    domain/ports/   : Protocoles abstraits (les "Ports")  │
│    domain/models/  : Dataclasses, structures de données  │
└──────────────────────────────────────────────────────────┘
         shared/   : types transverses multi-couches
         utils/    : helpers techniques purs (sans domaine)
```

### Règle de dépendance fondamentale

> **Le domaine ne dépend de rien. Tout dépend du domaine.**

- `domain/ports/` et `domain/models/` → aucune dépendance externe (ni Qt, ni services).
- `services/` → implémente les ports du domaine, gère l'orchestration technique.
- `widgets/` → couche de présentation pure, appelle les services uniquement via les ports.

---

## Structure du projet (`src/` layout)

```text
src/
  ezqt_app/
    domain/               ← DOMAINE (centre architectural)
      ports/              ← Contrats abstraits (Protocols Python)
      models/             ← Dataclasses et structures de données
      errors/             ← Exceptions métier spécifiques
      results/            ← Types de retour standardisés
    services/             ← ADAPTERS (implémentations des ports)
      config/             ← Gestion de la configuration persistante
      runtime/            ← État d'exécution de l'application
      settings/           ← Paramètres utilisateur et applicatifs
      translation/        ← Moteur de traduction et i18n
      ui/                 ← Orchestration des fonctions UI
    shared/               ← Types et utilitaires partagés entre couches
    utils/                ← Helpers techniques (logger, diagnostics, paths)
    widgets/              ← PRÉSENTATION (Composants Qt)
    cli/                  ← Interface en ligne de commande (utils, assets)
    resources/            ← Ressources statiques (themes, fonts, icons)
tests/                    ← Tests unitaires, intégration et robustesse
pyproject.toml            ← Configuration centrale du projet
```

### Pourquoi `src/` layout ?

Le package source est dans `src/ezqt_app/` (PEP 517). Cela empêche les imports accidentels depuis la racine et garantit que les tests s'exécutent contre le package installé.

---

## Responsabilités par couche

| Couche           | Chemin           | Rôle                                | Dépendances autorisées            |
| ---------------- | ---------------- | ----------------------------------- | --------------------------------- |
| Domaine — Ports  | `domain/ports/`  | Contrats abstraits (`Protocol`)     | Aucune                            |
| Domaine — Models | `domain/models/` | Structures de données pures         | stdlib uniquement                 |
| Services         | `services/*/`    | Implémentations concrètes des ports | `domain/`, `shared/`, `utils/`    |
| Shared           | `shared/`        | Types transverses                   | stdlib, PySide6 minimal           |
| Utils            | `utils/`         | Helpers techniques                  | stdlib, PySide6                   |
| Widgets          | `widgets/`       | Composants Qt (UI)                  | `services/`, `shared/`, `utils/`  |
| CLI              | `cli/`           | Outils ligne de commande            | `services/`, `domain/`, `shared/` |

---

## Fonctionnement des Ports & Adapters

### 1. Port (Contrat)

Défini dans `domain/ports/` comme un `Protocol`. Il décrit **ce que** le système fait.

```python
# domain/ports/settings_service.py
class SettingsServiceProtocol(Protocol):
    def set_theme(self, theme: str) -> None: ...
```

### 2. Adapter (Implémentation)

Défini dans `services/`. Il implémente le contrat de manière concrète.

```python
# services/settings/settings_service.py
class SettingsService(SettingsServiceProtocol):
    def set_theme(self, theme: str) -> None:
        self._state.gui.THEME = theme.lower()
```

### 3. Consommateur (Usage)

Utilisé dans `widgets/` via le port pour garantir le découplage.

```python
# widgets/core/settings_panel.py
from ezqt_app.domain.ports import SettingsServiceProtocol
```

---

## Stratégie d'imports et API Publique

Le contrat public stable est défini uniquement par `src/ezqt_app/__init__.py`.

### Rôle des `__init__.py`

- `ezqt_app/__init__.py` : **Seul point d'entrée public** (utilisé par le client de la lib).
- `domain/__init__.py` : Agrège les ports et modèles pour usage interne.
- `services/__init__.py` : Agrège les accès aux services pour les widgets et la CLI.

### Principe de Masquage

Si un utilisateur doit importer un fichier profond (ex: `ezqt_app.services.config.config_service`), l'encapsulation est brisée. Seule l'API exposée dans `ezqt_app/__init__.py` via `__all__` doit être utilisée par les consommateurs externes.

---

## Principes de Qualité (v5)

1. **Source unique de vérité** : Tout est dans `pyproject.toml`.
2. **Architecture Hexagonale** : Respect strict du flux de dépendances vers le domaine.
3. **Type Hints Obligatoires** : Code 100% typé pour une meilleure maintenabilité.
4. **Docstrings Google (EN)** : Documentation technique obligatoirement en anglais.
5. **Formatage Strict** : Utilisation de `ruff` pour le linting et le formatage.
6. **Tests Systématiques** : Utilisation de `pytest` (unitaires et intégration).
7. **Atomic Commits** : Messages de commit suivant la convention `conventional commits`.
8. **Environnement Corporate** : Gestion robuste des proxys et dépendances locales (Windows).

---

## Hiérarchie des instructions

1. **Ce fichier** (`README.md`) - Contexte projet et architecture
2. `core/advanced-cognitive-conduct.instructions.md` - Principes de raisonnement
3. `core/hexagonal-architecture-standards.instructions.md` - Standards d'architecture
4. `languages/python/python-development-standards.instructions.md` - Standards Python
5. `languages/python/python-formatting-standards.instructions.md` - Formatage et sections

---

## Standards de code obligatoires

### Langue

- **Docstrings** : Anglais uniquement.
- **Commentaires techniques** : Anglais uniquement.
- **Messages Utilisateurs** : Français/Anglais selon le contexte de déploiement.

### Qt / PySide6

- Utiliser exclusivement les enums Qt6 typés (`Qt.WindowType`, `Qt.MouseButton`, etc.).
- Éviter les accès legacy (`QtCore.Qt.LeftButton`).

### Gestion d'erreurs

- Utiliser les exceptions définies dans `domain/errors/`.
- Interdiction des exceptions silencieuses (`except: pass`).

---

## Critères d'acceptation d'un changement

Un changement est considéré conforme si :

- Il respecte l'architecture hexagonale (port → adapter → présentation).
- Il ne contient aucune dépendance cyclique.
- Il est entièrement typé et documenté (Google Style).
- Il passe les tests existants et inclut de nouveaux tests si nécessaire.
- Il n'ajoute pas de dette technique ou de code legacy.

---

_Document de référence à appliquer avant toute action de génération, refactor ou évolution._
