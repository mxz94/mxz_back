// 正文图片：补上懒加载与异步解码。
// 没再加 sizes —— 没有 srcset 时 sizes 不起作用，只会让标签变长。

type HastNode = {
  type?: string;
  tagName?: string;
  properties?: Record<string, unknown>;
  children?: HastNode[];
};

function visit(node: HastNode) {
  if (!node) return;

  if (node.type === "element" && node.tagName === "img") {
    const properties = node.properties || {};
    const src = typeof properties.src === "string" ? properties.src : "";

    if (src && !src.startsWith("data:")) {
      properties.loading ??= "lazy";
      properties.decoding ??= "async";
      node.properties = properties;
    }
  }

  node.children?.forEach(visit);
}

export function rehypeResponsiveImages() {
  return (tree: HastNode) => {
    visit(tree);
  };
}
