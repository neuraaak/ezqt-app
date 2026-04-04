# Makefile pour EzQt App
# Usage: make <target>

.PHONY: help install install-dev format lint test test-cov clean pre-commit setup-hooks docs docs-assets docs-build docs-deploy

# Configuration
PYTHON := python
PIP := pip
PACKAGE := ezqt_app

# Couleurs pour l'affichage
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Aide par défaut
help:
	@echo "$(BLUE)EzQt App - Commandes de développement$(RESET)"
	@echo ""
	@echo "$(GREEN)Installation:$(RESET)"
	@echo "  install      - Installer le package"
	@echo "  install-dev  - Installer les dépendances de développement"
	@echo ""
	@echo "$(GREEN)Formatage et qualité:$(RESET)"
	@echo "  format       - Formater le code (ruff format)"
	@echo "  lint         - Vérifier la qualité du code"
	@echo "  fix          - Corriger automatiquement les problèmes"
	@echo ""
	@echo "$(GREEN)Tests:$(RESET)"
	@echo "  test         - Lancer les tests unitaires"
	@echo "  test-cov     - Tests avec couverture"
	@echo "  test-fast    - Tests rapides (sans les lents)"
	@echo ""
	@echo "$(GREEN)Hooks et outils:$(RESET)"
	@echo "  setup-hooks  - Installer les hooks pre-commit"
	@echo "  pre-commit   - Lancer les vérifications pre-commit"
	@echo ""
	@echo "$(GREEN)Documentation:$(RESET)"
	@echo "  docs         - Lancer le serveur de documentation (hot-reload)"
	@echo "  docs-assets  - Generer le catalogue des assets embarques"
	@echo "  docs-build   - Build statique de la documentation"
	@echo "  docs-deploy  - Deployer sur GitHub Pages"
	@echo ""
	@echo "$(GREEN)Nettoyage:$(RESET)"
	@echo "  clean        - Nettoyer les fichiers temporaires"

# Installation
install:
	@echo "$(BLUE)Installation du package...$(RESET)"
	$(PIP) install -e .

install-dev:
	@echo "$(BLUE)Installation des dépendances de développement...$(RESET)"
	$(PIP) install -e ".[dev]"
	$(PIP) install pre-commit

# Formatage automatique
format:
	@echo "$(BLUE)Formatage du code avec Ruff...$(RESET)"
	ruff format src/$(PACKAGE) tests

# Correction automatique
fix: format
	@echo "$(GREEN)Code formaté automatiquement !$(RESET)"

# Linting
lint:
	@echo "$(BLUE)Vérification de la qualité du code...$(RESET)"
	ruff check src/$(PACKAGE) tests
	pyright src/$(PACKAGE)

# Tests
test:
	@echo "$(BLUE)Lancement des tests unitaires...$(RESET)"
	$(PYTHON) tests/run_tests.py --type unit

test-cov:
	@echo "$(BLUE)Tests avec couverture...$(RESET)"
	$(PYTHON) tests/run_tests.py --coverage

test-fast:
	@echo "$(BLUE)Tests rapides...$(RESET)"
	$(PYTHON) tests/run_tests.py --fast

# Hooks pre-commit
setup-hooks:
	@echo "$(BLUE)Installation des hooks pre-commit...$(RESET)"
	pre-commit install
	@echo "$(GREEN)Hooks pre-commit installés !$(RESET)"

pre-commit:
	@echo "$(BLUE)Lancement des vérifications pre-commit...$(RESET)"
	pre-commit run --all-files

# Documentation
docs:
	@echo "$(BLUE)Lancement du serveur de documentation...$(RESET)"
	mkdocs serve

docs-assets:
	@echo "$(BLUE)Generation du catalogue des assets...$(RESET)"
	$(PYTHON) .scripts/dev/generate_assets_catalog.py

docs-build:
	@echo "$(BLUE)Build de la documentation...$(RESET)"
	mkdocs build --strict

docs-deploy:
	@echo "$(BLUE)Deploiement sur GitHub Pages...$(RESET)"
	mkdocs gh-deploy --force

# Nettoyage
clean:
	@echo "$(BLUE)Nettoyage des fichiers temporaires...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ 2>/dev/null || true
	@echo "$(GREEN)Nettoyage terminé !$(RESET)"

# Commande complète de vérification
check: format lint test
	@echo "$(GREEN)Toutes les vérifications sont terminées !$(RESET)"

# Préparation pour un commit
prepare: format lint test-fast
	@echo "$(GREEN)Code prêt pour le commit !$(RESET)"
