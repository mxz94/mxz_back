// Place any global data in this file.
// You can import this data from anywhere in your site by using the `import` keyword.

export const SITE_DESCRIPTION = '兰汐爸爸记录的日志';

import type { Site, SocialObjects } from "./types";

export const SITE: Site = {
    website: "https://blog.malanxi.top/", // replace this with your deployed domain
    author: "兰汐",
    desc: "兰汐",
    title: "首页",
    ogImage: "astropaper-og.jpg",
    lightAndDarkMode: false,
    posts: ["blog", "note"],
    siteTime: "06/30/2022 00:06:00"
};
export const SITE_TITLE = SITE.desc;
export const LOCALE = ["zh-cn"]; // set to [] to use the environment default
export const TRANSITION_API = true
export const LOGO_IMAGE = {
    enable: false,
    svg: true,
    width: 216,
    height: 46,
};

export const SOCIALS: SocialObjects = [
    {
        name: "RSS",
        href: "/atom.xml",
        linkTitle: `RSS Feed`,
        active: true,
    },
    {
        name: "Github",
        href: "https://github.com/mxz94",
        linkTitle: ` ${SITE.title} on Github`,
        active: true,
    },
    {
        name: "Telegram",
        href: "https://t.me/ma741852",
        linkTitle: `${SITE.title} on Telegram`,
        active: true,
    },
    {
        name: "Run",
        href: "https://run.malanxi.top",
        linkTitle: `${SITE.title} on Run`,
        active: true,
    },
];