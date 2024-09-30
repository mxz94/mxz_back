import * as dotenv from "dotenv";
dotenv.config();

import algoliasearch from "algoliasearch";
const client = algoliasearch("MAQ5PM67UH", "771264cbf861502927cc145614c2b2d1");

// 1. Build a dataset
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import removeMd from "remove-markdown";
// const filenames = fs.readdirSync(path.join("./src/content/blog"))
// const data = filenames.map(filename => {
//     try {
//
//         const markdownWithMeta = fs.readFileSync("./src/content/blog" + filename)
//         const { data: frontmatter, content } = matter(markdownWithMeta)
//         return {
//             id: frontmatter.slug,
//             title: frontmatter.title,
//             content: removeMd(content).replace(/\n/g, ""),
//         }
//     } catch (e) {
//         // console.log(e.message)
//     }
// })
function readFilesRecursively(directory) {
  const filenames = fs.readdirSync(directory);
  const data = [];

  filenames.forEach(filename => {
    const filePath = path.join(directory, filename);
    const isDirectory = fs.statSync(filePath).isDirectory();

    if (isDirectory) {
      // 如果是文件夹，则递归调用 readFilesRecursively
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
// 2. Send the dataset in JSON format
client
  .initIndex("dev_blog")
  .saveObjects(JSON.parse(JSON.stringify(data)))
  .then(res => console.log(res))
  .catch(e => console.log(e));
