import * as dotenv from "dotenv";
dotenv.config();

import algoliasearch from "algoliasearch";
const client = algoliasearch("MAQ5PM67UH", "771264cbf861502927cc145614c2b2d1");

import fs from "fs";
import path from "path";
import matter from "gray-matter";
import removeMd from "remove-markdown";

function readFilesRecursively(directory) {
  const filenames = fs.readdirSync(directory);
  const data = [];

  filenames.forEach((filename) => {
    const filePath = path.join(directory, filename);
    const isDirectory = fs.statSync(filePath).isDirectory();

    if (isDirectory) {
      const subdirectoryData = readFilesRecursively(filePath);
      data.push(...subdirectoryData);
    } else {
      try {
        const markdownWithMeta = fs.readFileSync(filePath, "utf-8");
        const { data: frontmatter, content } = matter(markdownWithMeta);
        if (frontmatter.auth) {
          return;
        }
        data.push({
          objectID: frontmatter.title,
          title: frontmatter.title,
          url: "https://blog.malanxi.top/note/" + frontmatter.slug,
          content: removeMd(content).replace(/\n/g, ""),
        });
      } catch (e) {
        console.error(`Error processing file ${filePath}: ${e.message}`);
      }
    }
  });

  return data;
}

const directoryPath = "D:\\mxz\\mxz_back\\src\\content\\note";
const data = readFilesRecursively(directoryPath);

client
  .initIndex("dev_blog")
  .saveObjects(JSON.parse(JSON.stringify(data)))
  .then((res) => console.log(res))
  .catch((e) => console.log(e));
