#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const rootDir = path.resolve(__dirname, '..');
const commandsDir = path.join(rootDir, '.agents', 'commands');
const skillsDir = path.join(rootDir, '.agents', 'skills');
const hooksDir = path.join(rootDir, 'hooks');

const readFile = (filePath) => fs.readFileSync(filePath, 'utf8');

const stripBullet = (line) => line.replace(/^[-*]\s+/, '');

const normalizeWhitespace = (value) => value.replace(/\s+/g, ' ').trim();

const extractSectionLine = (content, heading) => {
  const target = `## ${heading}`.toLowerCase();
  const lines = content.split(/\r?\n/);
  for (let i = 0; i < lines.length; i += 1) {
    if (lines[i].trim().toLowerCase() === target) {
      for (let j = i + 1; j < lines.length; j += 1) {
        const line = lines[j].trim();
        if (!line) continue;
        return stripBullet(line);
      }
    }
  }
  return '';
};

const parseFrontmatter = (content) => {
  const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*/);
  if (!match) return { name: '', description: '' };

  const lines = match[1].split(/\r?\n/);
  const data = {};

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) continue;

    const key = m[1];
    let value = (m[2] ?? '').trim();

    // Handle YAML block scalars (e.g. `description: >` / `description: |`).
    if (value === '>' || value === '>-' || value === '|' || value === '|-') {
      const fold = value.startsWith('>');
      const block = [];

      for (let j = i + 1; j < lines.length; j += 1) {
        const next = lines[j];
        if (/^[A-Za-z0-9_-]+:\s*/.test(next)) {
          // Outer loop should process this key.
          i = j - 1;
          break;
        }
        block.push(next.replace(/^\s+/, ''));
        i = j;
      }

      const joined = fold ? block.join(' ') : block.join('\n');
      data[key] = normalizeWhitespace(joined);
      continue;
    }

    value = value.replace(/^['\"]/, '').replace(/['\"]$/, '').trim();
    data[key] = value;
  }

  return {
    name: data.name || '',
    description: data.description || '',
  };
};

const listFiles = (dir, filterFn) => {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((entry) => filterFn(path.join(dir, entry))).sort();
};

const listHookFiles = (dir, baseDir) => {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...listHookFiles(fullPath, baseDir));
    } else if (entry.isSymbolicLink()) {
      try {
        const stats = fs.statSync(fullPath);
        if (stats.isDirectory()) {
          results.push(...listHookFiles(fullPath, baseDir));
        } else if (stats.isFile()) {
          results.push(path.relative(baseDir, fullPath));
        }
      } catch {
        // Ignore broken symlinks.
      }
    } else if (entry.isFile()) {
      results.push(path.relative(baseDir, fullPath));
    }
  }
  return results.sort();
};

const listCommandFiles = (dir) => {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...listCommandFiles(fullPath));
    } else if (entry.isFile() && fullPath.endsWith('.md')) {
      results.push(fullPath);
    }
  }
  return results.sort();
};

const listSkillFiles = (dir) => {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...listSkillFiles(fullPath));
    } else if (entry.isFile() && entry.name === 'SKILL.md') {
      results.push(fullPath);
    }
  }
  return results.sort();
};

const commands = [];
if (fs.existsSync(commandsDir)) {
  const commandFiles = listCommandFiles(commandsDir);
  for (const filePath of commandFiles) {
    const content = readFile(filePath);
    const frontmatter = parseFrontmatter(content);
    const name = frontmatter.name || path.basename(filePath, '.md');
    const purpose = extractSectionLine(content, 'Purpose') || 'Purpose not documented.';
    const verification = extractSectionLine(content, 'Verification') || 'See command.';
    commands.push({ name, purpose, verification });
  }
}

const skillsByCategory = {};
if (fs.existsSync(skillsDir)) {
  const categories = listFiles(skillsDir, (filePath) => fs.statSync(filePath).isDirectory());
  for (const category of categories) {
    const categoryDir = path.join(skillsDir, category);
    const skillFiles = listSkillFiles(categoryDir);

    const skills = [];
    const seen = new Set();

    for (const skillFile of skillFiles) {
      const content = readFile(skillFile);
      const frontmatter = parseFrontmatter(content);
      const name = frontmatter.name || path.basename(path.dirname(skillFile));
      if (seen.has(name)) continue;
      seen.add(name);

      const description = frontmatter.description || 'Description not documented.';
      skills.push({ name, description });
    }

    skills.sort((a, b) => a.name.localeCompare(b.name));
    skillsByCategory[category] = skills;
  }
}

const hookFiles = listHookFiles(hooksDir, rootDir);

let output = '';
output += '# Cheatsheet\n\n';

output += '## Commands\n';
if (commands.length === 0) {
  output += '- None yet.\n';
} else {
  for (const command of commands) {
    output += `- \`${command.name}\`: ${command.purpose} (verify: ${command.verification})\n`;
  }
}
output += '\n';

output += '## Skills\n';
const categories = Object.keys(skillsByCategory).sort();
if (categories.length === 0) {
  output += '- None yet.\n\n';
} else {
  for (const category of categories) {
    output += `### ${category}\n`;
    const skills = skillsByCategory[category] || [];
    if (skills.length === 0) {
      output += '- None yet.\n\n';
      continue;
    }
    for (const skill of skills) {
      output += `- \`${skill.name}\`: ${skill.description}\n`;
    }
    output += '\n';
  }
}

output += '## Hooks\n';
if (hookFiles.length === 0) {
  output += '- None yet.\n\n';
} else {
  for (const hook of hookFiles) {
    output += `- \`${hook}\`\n`;
  }
  output += '\n';
}

output += '## Verification\n';
output += '- Use the `verify` skill for the pnpm ladder.\n\n';

output += '## Docs Structure\n';
output += '- See `docs/AGENTS.md` in target repos for doc locations and naming.\n';

fs.writeFileSync(path.join(rootDir, 'cheatsheet.md'), output);
console.log('cheatsheet.md updated.');

