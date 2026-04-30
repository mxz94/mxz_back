import MarkdownIt from "markdown-it";
import sanitizeHtml from "sanitize-html";

const parser = new MarkdownIt({ html: false, linkify: false });
const SUMMARY_LENGTH = 110;

const hiddenContentPatterns = [
  /```[\s\S]*?```/g,
  /~~~[\s\S]*?~~~/g,
  /<!--[\s\S]*?-->/g,
  /<script\b[\s\S]*?<\/script>/gi,
  /<style\b[\s\S]*?<\/style>/gi,
  /<iframe\b[\s\S]*?<\/iframe>/gi,
  /<video\b[\s\S]*?<\/video>/gi,
  /<picture\b[\s\S]*?<\/picture>/gi,
  /<svg\b[\s\S]*?<\/svg>/gi,
  /!\[[^\]]*]\([^)]*\)/g,
  /!\[[^\]]*]\[[^\]]*]/g,
  /<img\b[^>]*>/gi,
  /<source\b[^>]*>/gi,
];

const htmlEntities: Record<string, string> = {
  amp: "&",
  gt: ">",
  lt: "<",
  nbsp: " ",
  quot: '"',
  apos: "'",
};

function decodeHtmlEntities(value: string) {
  return value
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([\da-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)))
    .replace(/&([a-z]+);/gi, (match, name) => htmlEntities[name.toLowerCase()] ?? match);
}

function stripHiddenContent(value: string) {
  return hiddenContentPatterns.reduce((text, pattern) => text.replace(pattern, " "), value);
}

function normalizeText(value: string) {
  return decodeHtmlEntities(value)
    .replace(/<[^>]+>/g, " ")
    .replace(/\[[^\]]+]:\s+\S+(?:\s+["'][^"']+["'])?/g, " ")
    .replace(/https?:\/\/\S+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function toPlainText(value = "") {
  const withoutHiddenContent = stripHiddenContent(decodeHtmlEntities(value));
  const html = parser.render(withoutHiddenContent);
  const text = sanitizeHtml(html, {
    allowedAttributes: {},
    allowedTags: [],
  });

  return normalizeText(text);
}

const suppDesc = (desc?: string | null, content = "") => {
  const text = toPlainText(desc || content);
  return text.length > SUMMARY_LENGTH ? `${text.slice(0, SUMMARY_LENGTH).trim()}...` : text;
};

export default suppDesc;
