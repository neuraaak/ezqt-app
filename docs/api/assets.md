# Asset catalog

Lookup reference for embedded Qt assets exposed by EzQt App.

## 📋 Embedded assets table

The catalog below is generated from resource registries and includes:

- File name
- Qt resource path
- Python accessor symbol
- Visual preview

<div id="assets-catalog-search" style="margin: 0.5rem 0 1rem;">
    <input
        id="assets-catalog-search-input"
        type="search"
        placeholder="Filter assets (file, Qt path, accessor...)"
        aria-label="Filter assets table"
        style="width: min(100%, 520px); padding: 0.55rem 0.7rem; border-radius: 0.5rem; border: 1px solid var(--md-default-fg-color--lightest);"
    />
    <p id="assets-catalog-search-stats" style="margin: 0.4rem 0 0; font-size: 0.85rem; opacity: 0.8;"></p>
</div>

--8<-- "api/assets.generated.md"

<script>
(() => {
    const input = document.getElementById("assets-catalog-search-input");
    const stats = document.getElementById("assets-catalog-search-stats");
    if (!input) {
        return;
    }

    const allRows = Array.from(
        document.querySelectorAll("article table tbody tr"),
    );

    const setStats = (visible, total, query) => {
        if (!stats) {
            return;
        }
        if (!query) {
            stats.textContent = `${total} assets`;
            return;
        }
        stats.textContent = `${visible} / ${total} assets match \"${query}\"`;
    };

    const filterRows = () => {
        const query = input.value.trim().toLowerCase();
        let visible = 0;
        for (const row of allRows) {
            const text = row.textContent?.toLowerCase() ?? "";
            const keep = !query || text.includes(query);
            row.style.display = keep ? "" : "none";
            if (keep) {
                visible += 1;
            }
        }
        setStats(visible, allRows.length, query);
    };

    input.addEventListener("input", filterRows);
    input.addEventListener("search", filterRows);
    setStats(allRows.length, allRows.length, "");
})();
</script>

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
