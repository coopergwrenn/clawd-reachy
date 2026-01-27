import { writeFile } from "fs/promises";
import { mkdir } from "fs/promises";
import { resolve, dirname } from "path";
import Replicate from "replicate";

const replicate = new Replicate({
  auth: "r8_H7NpNJQwqwQDA2yQTxVFyVZsuaOWXYU3Oq5JG"
});

const prompt = "professional digital art of Mercury god of commerce and speed, modern sleek aesthetic, dynamic energy, golden accents, clever confident expression, tech-forward design, high quality, 1024x1024";

console.log("🎨 Generating Mercury avatar with Replicate (google/nano-banana)...\n");

try {
  const output = await replicate.run("google/nano-banana", {
    input: {
      prompt: prompt
    }
  });
  
  console.log("✓ Generation complete!");
  console.log(`Image URL: ${output}\n`);
  
  // Download and save
  const response = await fetch(output);
  const buffer = await response.arrayBuffer();
  
  const filePath = resolve("/home/wrenn/clawd/avatars/mercury.png");
  const dir = dirname(filePath);
  
  await mkdir(dir, { recursive: true });
  await writeFile(filePath, Buffer.from(buffer));
  
  console.log(`✓ Saved to: ${filePath}`);
  process.exit(0);
} catch (error) {
  console.error(`Error: ${error.message}`);
  console.error(error);
  process.exit(1);
}
