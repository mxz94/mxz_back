import { visit } from 'unist-util-visit';

export function livePhotoPlugin() {
    return (tree) => {
        try {
            visit(tree, 'image', (node) => {
                const { url } = node;
                // 验证 URL 是否有效
                if (!url || typeof url !== 'string') {
                    console.warn('Invalid image URL, skipping:', node);
                    return;
                }
                const d = url.split('?v=');
                // 确保是 LivePhoto 格式
                if (d.length !== 2 || !d[0] || !d[1]) {
                    console.warn('Non-LivePhoto URL, treating as regular image:', url);
                    return; // 保留原图片节点
                }
                node.type = 'html';
                node.value = `
          <div class="live-photo-container min_width_1280"
               data-live-photo
               data-effect-type="live"
               data-playback-style="full"
               data-proactively-loads-video="true"
               data-role="default"
               data-photo-src="${d[0]}"
               data-video-src="${d[1]}"></div>`;
            });
        } catch (error) {
            console.warn('livePhotoPlugin error, ignored:', error.message);
        }
    };
}