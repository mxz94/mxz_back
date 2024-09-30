import { visit } from 'unist-util-visit';

// ![图片说明](https://pub-4232cd0528364004a537285f400807bf.r2.dev/2024/A001_07251216_C317-FfGABM.jpg?v=https://pub-4232cd0528364004a537285f400807bf.r2.dev/2024/A001_07251216_C317-DQ6Nj6.mp4)
export function livePhotoPlugin() {
    return (tree) => {
        visit(tree, 'image', (node) => {
            const {url } = node;
            var d = url.split('?v=')
            if (d.length > 1) {
                node.type = 'html';
                node.value = `
            <div class='live-photo-container min_width_1280'
                  data-live-photo
              data-effect-type='live'
              data-playback-style='full'
              data-proactively-loads-video='true'
                 data-photo-src='${d[0]}'
                 data-video-src='${d[1]}'></div>`;
            }
        });
    };
}
