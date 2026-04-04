# Asset catalog

Lookup reference for embedded Qt assets exposed by EzQt App.

## 📋 Embedded assets table

The catalog below is generated from resource registries and includes:

- File name
- Qt resource path
- Python accessor symbol
- Visual preview

--8<-- "api/assets.generated.md"

## 🧩 Runtime generated assets (AppIcons/AppImages)

Source of truth after `init()`: generated files in `bin/app_icons.py` and `bin/app_images.py`.

```python
from ezqt_app import init
from ezqt_app.shared import resources

init()

# Runtime assets from your project bin/icons and bin/images
icon_path = resources.AppIcons.my_custom_icon
image_path = resources.AppImages.my_custom_image
```

!!! note "Import timing"
    `AppIcons` and `AppImages` are populated by `init()`. For reliability,
    access them through the module object (`resources.AppIcons`) after bootstrap.

## 🔗 Related

- [Qt resources pipeline](../guides/resources.md)
- [Examples](../examples/index.md)
