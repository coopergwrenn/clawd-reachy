import { writeFile } from "fs/promises";
import { mkdir } from "fs/promises";
import { resolve, dirname } from "path";
import Replicate from "replicate";

const replicate = new Replicate({
  auth: "r8_H7NpNJQwqwQDA2yQTxVFyVZsuaOWXYU3Oq5JG"
});

const prompt = "pixel art Mercury god of commerce and speed, 8-bit retro style, sharp angular design, bold colors, confident expression, wings on heels, dark background, clean pixel art, 256x256";

console.log("🎨 Generating Mercury pixel art...\n");

try {
  const output = await replicate.run("google/nano-banana", {
    input: {
      prompt: prompt
    }
  });
  
  console.log("✓ Generated!");
  console.log(`URL: ${output}\n`);
  
  const response = await fetch(output);
  const buffer = await response.arrayBuffer();
  
  const filePath = resolve("/home/wrenn/clawd/avatars/mercury.png");
  const dir = dirname(filePath);
  
  await mkdir(dir, { recursive: true });
  await writeFile(filePath, Buffer.from(buffer));
  
  console.log(`✓ Saved`);
  process.exit(0);
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
