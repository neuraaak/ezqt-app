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
| Build backend | setuptools (PEP 517)                       |
| Licence       | MIT                                        |
| Statut        | Production/Stable                          |
| Configuration | `pyproject.toml` (source unique de vérité) |

---

## Hiérarchie des instructions

Les fichiers d'instructions du projet sont organisés par priorité décroissante :

1. **Ce fichier** (`README.md`) - Contexte projet et architecture
2. `core/advanced-cognitive-conduct.instructions.md` - Principes de raisonnement
3. `languages/python/python-development-standards.instructions.md` - Standards Python
4. `languages/python/python-formatting-standards.instructions.md` - Formatage et sections
5. `languages/python/pyproject-standards.instructions.md` - Standards pyproject.toml
6. `CLAUDE.md` (racine) - Préférences spécifiques à Claude
7. `AGENTS.md` (racine) - Instructions générales pour agents IA

En cas de conflit, le fichier le plus haut dans cette liste prévaut.

---

## Principes fondamentaux v5

1. **Source unique de vérité** : Toute configuration doit être centralisée dans `pyproject.toml`.
2. **Architecture modulaire** : Séparer clairement app, kernel, widgets, CLI, traduction.
3. **Type hints obligatoires** : Tous les modules et fonctions doivent être typés.
4. **Docstrings Google** : Utiliser le style Google pour toute documentation de fonction/classe.
5. **Formatage strict** : Respecter PEP 8, ruff, black, isort. Sections de code clairement marquées.
6. **Tests systématiques** : Toute nouvelle fonctionnalité doit être couverte par des tests pytest.
7. **Atomic commits** : Un commit = une modification logique, avec message structuré.
8. **CI/CD** : Les workflows GitHub Actions doivent valider lint, tests et couverture.
9. **Gestion des dépendances** : Utiliser des wheels locales, pas de dépendances non vérifiées.
10. **Sécurité** : Jamais de credentials ou données sensibles dans le code ou les commits.
11. **Documentation vivante** : Toute évolution doit être documentée dans le README et les docstrings.
12. **Instructions hiérarchisées** : En cas de conflit, suivre la priorité ci-dessus.
13. **Conformité licence** : Respect strict de la licence MIT et des mentions légales.
14. **Proxy/Environnement** : Adapter le code et les scripts à l’environnement corporate (proxy, Windows).
15. **Revue de code** : Toute PR doit être relue et validée avant merge.

---

## Cycle de vie projet

- Toute évolution doit respecter cette charte.
- Les incohérences ou conflits doivent être remontés et résolus selon la hiérarchie ci-dessus.
- Les standards sont évolutifs mais toute modification doit être validée en équipe.

---

_À compléter et valider avant tout refactoring architectural v5._
