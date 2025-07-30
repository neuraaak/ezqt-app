# 📚 Documentation - EzQt_App

## 📋 **Overview**

This directory contains all the documentation for the EzQt_App project, organized by category to facilitate navigation and understanding of the framework.

## 🎯 **About EzQt_App**

EzQt_App is a Python framework designed to facilitate the creation of modern Qt applications, based on a template by Wanderson M. Pimenta. It automates resource management, generates all required files, and offers a rapid project bootstrap experience with a CLI command.



## 🚀 **Main Features**

### **Automatic Generation**
- Asset folders and files (icons, images, themes, etc.)
- Complete project structure
- YAML configuration files

### **User Interface**
- Dynamic themes (light/dark) with integrated switching
- Global translation system with multi-language support
- Automatic translation system with multi-provider support
- Custom widgets with animations and themes
- Advanced resource manager with automatic detection

### **Development Tools**
- `ezqt_init` CLI command to quickly initialize a new project
- Ready-to-use `main.py` example generated automatically
- Modular and extensible structure
- Standardized logging system with consistent formatting

### **Kernel Architecture**
- **Modular Design**: Refactored into specialized packages
- **Helper Functions**: Simplified API for common operations
- **Resource Management**: Centralized asset and configuration handling
- **Translation System**: Complete internationalization support with automatic translation
- **Auto-Translation**: Multi-provider support (LibreTranslate, MyMemory, Google)
- **String Collection**: Automatic string collection for translations
- **Standardized Logging**: Consistent message formatting across all components

## 📖 **Documentation by Category**

### **📋 General Documentation**
- [**CHANGELOG.md**](../CHANGELOG.md) - Version history and changes

### **🔧 API Documentation**
- [**api/README.md**](./api/README.md) - API overview
- [**api/API_DOCUMENTATION.md**](./api/API_DOCUMENTATION.md) - Complete documentation of all components
- [**api/STYLE_GUIDE.md**](./api/STYLE_GUIDE.md) - Style guide and QSS customization
- [**api/LOGGING_SYSTEM.md**](./api/LOGGING_SYSTEM.md) - Standardized logging system documentation

### **🖥️ CLI Documentation**
- [**cli/README.md**](./cli/README.md) - Command line interface and utilities

### **🧪 Test Documentation**
- [**tests/README.md**](./tests/README.md) - Test overview
- [**tests/QUICK_START_TESTS.md**](./tests/QUICK_START_TESTS.md) - Quick start guide
- [**tests/TESTS_DOCUMENTATION.md**](./tests/TESTS_DOCUMENTATION.md) - Complete test documentation

## 🚀 **Installation and Usage**

### **Installation**
```bash
# Via pip (recommended)
pip install ezqt_app

# Or locally
git clone https://github.com/neuraaak/EzQt-App.git
cd ezqt_app
pip install .
```

### **Project Initialization**
```bash
# Initialize a new project in an empty folder
ezqt_init
```

### **Minimal Usage**
```python
import ezqt_app.main as ezqt
from ezqt_app.app import EzQt_App, EzApplication
import sys

ezqt.init()
app = EzApplication(sys.argv)
window = EzQt_App(themeFileName="main_theme.qss")
window.show()
app.exec()
```

### **Using Helper Functions**
```python
from ezqt_app.kernel import (
    get_setting, set_setting, load_fonts,
    maximize_window, apply_theme, tr
)

# Configuration
theme = get_setting("app", "theme", "dark")
set_setting("ui", "window.width", 1200)

# Resources
load_fonts()

# UI Operations
maximize_window(main_window)
apply_theme(widget, theme_content)

# Translation
translated_text = tr("Hello")
```

## 📦 **Dépendances**

- **PySide6==6.9.1** - Framework Qt moderne
- **PyYaml==6.0.2** - Gestion des fichiers YAML
- **colorama==0.4.6** - Couleurs de terminal
- **requests==2.32.3** - Requêtes HTTP
- **ezqt-widgets>=2.0.0** - Widgets personnalisés

## 🧪 **Testing and Quality**

### **Running Tests**
```bash
# From project root
python tests/run_tests.py --type unit

# Or directly
python -m pytest tests/unit/ -v

# Tests with coverage
python tests/run_tests.py --type unit --coverage
```

### **Statistiques des tests**
- **Tests unitaires** : 225+ tests
- **Tests d'intégration** : 15+ tests
- **Total** : 240+ tests
- **Couverture de code** : > 90%

### **Répartition par module**
- **Kernel** : 80+ tests (TranslationManager, Settings, Helper.Maker, AppFunctions)
- **Widgets Core** : 100+ tests (EzApplication, Header, Menu, PageContainer, SettingsPanel)
- **Widgets Étendus** : 30+ tests (SettingWidgets)
- **Utilitaires** : 15+ tests (CLI)

## 🌍 **Système de traduction**

Le framework inclut un système de traduction complet avec traduction automatique :

```python
from ezqt_app.kernel.translation_manager import get_translation_manager

# Obtenir le gestionnaire de traduction
tm = get_translation_manager()

# Changer la langue
tm.load_language_by_code("fr")

# Traduire du texte
translated_text = tm.translate("Hello World")

# Traduction automatique (quand activée)
from ezqt_app.kernel.translation.auto_translator import AutoTranslator
translator = AutoTranslator()
auto_translated = translator.translate_sync("Hello World", "fr")
```

**Langues supportées :** English, Français, Español, Deutsch  
**Fournisseurs de traduction :** LibreTranslate, MyMemory, Google Translate  
**Note :** Le système de traduction automatique est temporairement désactivé pour le développement

## 🔧 **Structure du projet**

```
ezqt_app/
├── kernel/                    # Composants fondamentaux
│   ├── translation_manager.py # Gestionnaire de traduction
│   ├── app_settings.py        # Paramètres de l'application
│   ├── common.py              # Variables communes (APP_PATH, etc.)
│   ├── globals.py             # Variables globales (GLOBAL_STATE, etc.)
│   ├── ui_functions/          # Fonctions UI modulaires
│   │   ├── __init__.py        # Interface principale
│   │   ├── window_manager.py  # Gestion de la fenêtre
│   │   ├── panel_manager.py   # Gestion des panneaux
│   │   ├── menu_manager.py    # Gestion des menus
│   │   ├── theme_manager.py   # Gestion des thèmes
│   │   ├── ui_definitions.py  # Définitions UI
│   │   └── ui_functions.py    # Classe principale
│   ├── app_functions/         # Fonctions utilitaires modulaires
│   │   ├── __init__.py        # Interface principale
│   │   ├── assets_manager.py  # Gestion des assets
│   │   ├── config_manager.py  # Gestion de la configuration
│   │   ├── resource_manager.py # Gestion des ressources
│   │   ├── settings_manager.py # Gestion des paramètres
│   │   └── kernel.py          # Classe principale
│   └── main.py                # Module d'initialisation principal
├── widgets/                   # Composants d'interface
│   ├── core/                  # Widgets principaux
│   └── extended/              # Widgets étendus
├── utils/                     # Utilitaires
│   ├── cli.py                 # Interface en ligne de commande
│   └── qmessage_logger.py     # Logger Qt
└── resources/                 # Ressources (icônes, thèmes, etc.)
```

## 📊 **Métriques de qualité**

### **Couverture par module**
- **TranslationManager** : 95%
- **Settings** : 90%
- **Helper.Maker** : 85%
- **AppFunctions** : 90%
- **Widgets Core** : 95%
- **Widgets Étendus** : 90%
- **Utilitaires** : 85%
- **Intégration** : 80%

## 🎯 **Objectifs du framework**

### **Fonctionnels**
- Simplifier la création d'applications Qt
- Automatiser la gestion des ressources
- Fournir une base solide et extensible
- Supporter le développement multi-langues

### **Qualité**
- Maintenir une couverture de tests élevée
- Assurer la stabilité et la performance
- Faciliter la maintenance et l'évolution

## 📚 **Navigation**

- **README principal** : [../README.md](../README.md)
- **Code source** : [../ezqt_app/](../ezqt_app/)
- **Tests** : [../tests/](../tests/)
- **Changelog** : [../CHANGELOG.md](../CHANGELOG.md)

---

**État global :** 🟢 **OPÉRATIONNEL** (240+ tests, couverture > 90%) 