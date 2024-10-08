import { visit } from 'unist-util-visit';

//
// !bv{<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=1300043618&bvid=BV1AT4m1S7fX&cid=1425402794&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>}
export function bilibiliPlugin() {
    return (tree) => {
        visit(tree, 'paragraph', (node) => {
            const children = node.children;
            const current = children[0];
            // text html html text
            if (children.length >=2 && current.type == 'text' && current.value == '!bv{') {
                node.type = 'html';
                //  不跳转
                var a = children[1].value.slice(0,children[1].value.length-1) + 'sandbox="allow-top-navigation allow-same-origin allow-forms allow-scripts">'
                node.value = `<div class='video-container min_width_1280'>${a + children[2].value}</div>`;
            }
        });
    };
}
