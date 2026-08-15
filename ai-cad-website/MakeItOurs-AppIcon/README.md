# MakeItOurs App Icon

Production app-icon package built from independently authored 1024×1024 SVG artwork. The vector layers contain no raster extraction, canvas mask, shadow, blur, refraction, specular highlight, or baked Liquid Glass effect.

## Deliverables

- `IconComposer-Source/` — registered, numbered SVG layers for background, blueprint, house shell, and house detail.
- `MakeItOurs.icon` — native Icon Composer document (after the one-time Icon Composer license is accepted and the document is saved).
- `MakeItOurs-AppIcon-Master-1024.png` — full-bleed RGB fallback rendered from the SVG source.
- `MakeItOurs-AppIcon-Flattened-1024.png` — marketing and legacy fallback.
- `AppIcon.appiconset/` — legacy Xcode asset catalog for iOS and macOS.
- `build_icon_assets.mjs` — deterministic fallback and asset-catalog renderer.

## Icon Composer

1. Open Icon Composer from Xcode.
2. Create a 1024×1024 document and import all files from `IconComposer-Source` together. Alphabetical filenames define back-to-front order and identical SVG view boxes preserve registration.
3. Keep the core blueprint/house silhouette consistent across Default, Dark, and Mono. Preview Mono with both Clear and Tinted options.
4. Prefer a native canvas gradient in Icon Composer. The background SVG is included as a deterministic fallback and may be hidden after recreating its blue-to-coral field on the canvas.
5. Apply Liquid Glass in Icon Composer: keep the background flat; use subtle refraction and specular highlights on the blueprint group; use restrained shadow and material depth on the house groups. Validate at small preview sizes and against light/dark imagery.
6. Save as `MakeItOurs.icon` in this directory. Add that file directly to Xcode and select it as the target's App Icon source. A native `.icon` file replaces the app-icon asset catalog for that target.

The system applies the final platform mask. Do not add rounded corners to any source layer.

## Legacy Xcode integration

Use `AppIcon.appiconset` only when retaining the previous asset-catalog workflow. Drag it into `Assets.xcassets`, select `AppIcon` as the target's App Icons Source, then archive normally.

## Rebuilding fallbacks

Run `node build_icon_assets.mjs` with `sharp` available. This composites the clean SVG files and regenerates the RGB master, flattened fallback, and complete asset catalog.
