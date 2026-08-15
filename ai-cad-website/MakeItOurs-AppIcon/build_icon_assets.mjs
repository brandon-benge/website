import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const sharp = require("sharp");

const root = dirname(fileURLToPath(import.meta.url));
const source = join(root, "IconComposer-Source");
const appicon = join(root, "AppIcon.appiconset");
await mkdir(appicon, { recursive: true });

const layerNames = [
  "00-background.svg",
  "01-blueprint.svg",
  "02-finished-house.svg",
  "03-house-details.svg",
];
const layers = await Promise.all(layerNames.map(async (name) => ({
  input: await sharp(await readFile(join(source, name))).png().toBuffer(),
  left: 0,
  top: 0,
})));

const transparentCanvas = {
  create: { width: 1024, height: 1024, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } },
};
const master = await sharp(transparentCanvas).composite(layers).removeAlpha().png().toBuffer();

await writeFile(join(root, "MakeItOurs-AppIcon-Master-1024.png"), master);
await writeFile(join(root, "MakeItOurs-AppIcon-Flattened-1024.png"), master);

const targets = new Map([
  ["icon-16.png", 16], ["icon-16@2x.png", 32],
  ["icon-32.png", 32], ["icon-32@2x.png", 64],
  ["icon-128.png", 128], ["icon-128@2x.png", 256],
  ["icon-256.png", 256], ["icon-256@2x.png", 512],
  ["icon-512.png", 512], ["icon-512@2x.png", 1024],
  ["AppIcon-1024.png", 1024],
]);
for (const [name, size] of targets) {
  await sharp(master).resize(size, size).png().toFile(join(appicon, name));
}

const mac = [];
for (const size of [16, 32, 128, 256, 512]) {
  for (const scale of [1, 2]) {
    mac.push({
      filename: scale === 1 ? `icon-${size}.png` : `icon-${size}@2x.png`,
      idiom: "mac",
      scale: `${scale}x`,
      size: `${size}x${size}`,
    });
  }
}
await writeFile(join(appicon, "Contents.json"), JSON.stringify({
  images: [{ filename: "AppIcon-1024.png", idiom: "universal", platform: "ios", size: "1024x1024" }, ...mac],
  info: { author: "xcode", version: 1 },
}, null, 2) + "\n");
