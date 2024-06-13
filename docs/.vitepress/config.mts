import {defineConfig} from 'vitepress'
import {withMermaid} from "vitepress-plugin-mermaid";
import timeline from "vitepress-markdown-timeline";
import {version} from "../../package.json"

// https://vitepress.dev/reference/site-config
export default withMermaid(
    defineConfig({
        base: process.env.VITE_BASE,
        lang: 'zh-CN',
        title: "YouQu3 | 下一代Linux自动化测试框架",
        description: "使用简单且功能强大的自动化测试框架",
        head: [
            ['meta', {name: 'referrer', content: 'no-referrer-when-downgrade'}],
            ['link', {rel: 'icon', href: `${process.env.VITE_BASE || '/'}favicon.ico`}],
        ],
        vite: {
            publicDir: "assets",
        },
        markdown: {
            config: (md) => {
                md.use(timeline)
            }
        },

        themeConfig: {
            // https://vitepress.dev/reference/default-theme-config
            siteTitle: "YouQu3",
            nav: [
                {text: '首页', link: '/index'},
                {text: '简介', link: '/快速开始'},
                {text: '设计', link: '/设计/YouQu3架构设计规划'},
            ],

            sidebar: {
                "/设计/": [
                    {
                        text: "框架设计",
                        collapsed: false,
                        items: [
                            {text: "YouQu3架构设计规划", link: "/设计/YouQu3架构设计规划"},
                            {text: "UOS系统测试套件", link: "/设计/UOS系统测试套件"},
                        ]
                    },
                ],
            },
            search: {
                provider: 'local'
            },
            ignoreDeadLinks: true,
            // =========================================================
            logo: {src: '/logo.png', width: 26, height: 30},
            socialLinks: [
                {icon: 'github', link: 'https://github.com/funny-dream/youqu3'}
            ],
            footer: {
                copyright: `版权所有 © 2024-${new Date().getFullYear()} 统信软件`
            },
            //大纲显示2-3级标题
            outline: [2, 4],
            //大纲顶部标题
            outlineTitle: '当前页大纲',

            docFooter: {
                prev: '上一页',
                next: '下一页'
            },

            lastUpdated: {
                text: '最后更新于',
                formatOptions: {
                    dateStyle: 'short',
                    timeStyle: 'medium'
                }
            },

            langMenuLabel: '多语言',
            returnToTopLabel: '回到顶部',
            sidebarMenuLabel: '菜单',
            darkModeSwitchLabel: '主题',
            lightModeSwitchTitle: '切换到浅色模式',
            darkModeSwitchTitle: '切换到深色模式'
        },
    })
);
