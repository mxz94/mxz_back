import { visit } from 'unist-util-visit';

export function livePhotoPlugin() {
    return (tree) => {
        try {
            visit(tree, 'image', (node) => {
                const { url } = node;
                if (!url || typeof url !== 'string') return;

                const parts = url.split('?v=');
                if (parts.length !== 2 || !parts[0] || !parts[1]) return;

                node.type = 'html';
                node.value = `
          <div class="live-photo-container min_width_1280"
               data-live-photo
               data-effect-type="live"
               data-playback-style="full"
               data-proactively-loads-video="true"
               data-role="default"
               data-photo-src="${parts[0]}"
               data-video-src="${parts[1]}"></div>`;
            });
        } catch (error) {
            console.warn('livePhotoPlugin error, ignored:', error.message);
        }
    };
}
