const ARTICLE_IMAGE_SIZES =
  "(max-width: 767px) calc(100vw - 2rem), (max-width: 1023px) 92vw, (max-width: 1439px) calc(100vw - 22rem), 1280px";

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
      properties.sizes ??= ARTICLE_IMAGE_SIZES;
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
