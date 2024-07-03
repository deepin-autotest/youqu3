import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    base: process.env.VITE_BASE,
    lang: 'zh-CN',
    title: "YouQu3 | 下一代Linux自动化测试框架",
    description: "使用简单且功能强大的自动化测试框架",
    head: [
        // ['meta', {name: 'referrer', content: 'no-referrer-when-downgrade'}],
        ['link', {rel: 'icon', href: `${process.env.VITE_BASE || '/'}favicon.ico`}],
    ],
    vite: {
        publicDir: "assets",
    },

    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        siteTitle: "YouQu3",
        nav: [
            {text: '🏠 YouQu3', link: '/index'},
            {text: '🧭 指南', link: '/指南/简介/YouQu3是什么'},
            {text: '🔌 插件', link: '/插件/插件列表'},
            {text: '🎵 设计', link: '/设计/YouQu3架构设计规划'},
            {text: '|', link: '/'},
            {text: '🏠 PyLinuxAuto', link: '/pylinuxauto/index'},
            {text: '🧭 指南', link: '/pylinuxauto/简介'},
        ],

        sidebar: {
             "/指南/": [
                    {
                        text: "简介",
                        items: [
                            {text: "YouQu3是什么", link: "/指南/简介/YouQu3是什么"},
                            {text: "快速开始", link: "/指南/简介/快速开始"},
                        ]
                    },
                    {
                        text: "环境管理",
                        items: [
                            {text: "虚拟环境", link: "/指南/环境管理/虚拟环境"},
                            {text: "原生环境", link: "/指南/环境管理/原生环境"},
                        ]
                    },
                    {
                        text: "开发实践",
                        items: [
                            {text: "方法编写", link: "/指南/开发实践/方法编写"},
                            {text: "用例编写", link: "/指南/开发实践/用例编写"},
                        ]
                    },
                    {
                        text: "驱动执行",
                        items: [
                            {text: "本地执行", link: "/指南/驱动执行/本地执行"},
                            {text: "远程执行", link: "/指南/驱动执行/远程执行"},
                            {text: "自定义用例集驱动", link: "/指南/驱动执行/自定义用例集驱动"},
                        ]
                    },
                    {
                        text: "与生俱来",
                        items: [
                            {text: "脚手架工具", link: "/指南/与生俱来/脚手架工具"},
                            {text: "全自动日志", link: "/指南/与生俱来/全自动日志"},
                            {text: "标签化管理", link: "/指南/与生俱来/标签化管理"},
                            {text: "远程交互控制", link: "/指南/与生俱来/远程交互控制"},
                            {text: "命令行交互", link: "/指南/与生俱来/命令行交互"},
                            {text: "断言语句", link: "/指南/与生俱来/断言语句"},
                            {text: "动态等待", link: "/指南/与生俱来/动态等待"},
                            {text: "JSON报告", link: "/指南/与生俱来/JSON报告"},
                            {text: "前后钩子", link: "/指南/与生俱来/前后钩子"},
                        ]
                    },
                    {
                        text: "可选功能",
                        items: [
                            {text: "桌面UI自动化", link: "/指南/可选功能/桌面UI自动化"},
                            {text: "WebUI自动化", link: "/指南/可选功能/WebUI自动化"},
                            {text: "DBus操控", link: "/指南/可选功能/DBus操控"},
                            {text: "用例录屏", link: "/指南/可选功能/用例录屏"},
                            {text: "HTML报告", link: "/指南/可选功能/HTML报告"},
                            {text: "其他", link: "/指南/可选功能/其他"},
                        ]
                    },
                 ],
             "/pylinuxauto/": [
                    {
                        text: "PyLinuxAuto",
                        items: [
                            {text: "简介", link: "/pylinuxauto/简介"},
                        ]
                    },
                    {
                        text: "定位方法",
                        items: [
                            {text: "属性定位", link: "/pylinuxauto/属性定位"},
                            {text: "图像识别", link: "/pylinuxauto/图像识别"},
                            {text: "OCR识别", link: "/pylinuxauto/OCR识别"},
                            {text: "相对位移定位", link: "/pylinuxauto/相对位移定位"},
                        ]
                    },
                 ],
             "/插件/": [
                    {
                        text: "插件汇总",
                        items: [
                            {text: "插件列表", link: "/插件/插件列表"},
                            {text: "测试套件", link: "/插件/测试套件"},
                        ]
                    },
                    {
                        text: "插件生态明细",
                        items: [
                            {text: "标签化管理", link: "/插件/标签化管理"},
                            {text: "日志", link: "/插件/日志"},
                            {text: "属性识别", link: "/插件/属性识别"},
                            {text: "图像识别", link: "/插件/图像识别"},
                            {text: "OCR识别", link: "/插件/OCR识别"},
                            {text: "键鼠操作", link: "/插件/键鼠操作"},
                            {text: "DBus操控", link: "/插件/DBus操控"},
                            {text: "相对位移定位", link: "/插件/相对位移定位"},
                            {text: "用例录屏", link: "/插件/用例录屏"},
                            {text: "WebUI自动化", link: "/插件/WebUI自动化"},
                            {text: "Html测试报告", link: "/插件/Html测试报告"},
                            {text: "PMS测试单驱动", link: "/插件/PMS测试单驱动"},
                        ]
                    },
                 ],
            "/设计/": [
                {
                    text: "框架设计",
                    collapsed: false,
                    items: [
                        {text: "YouQu3架构设计规划", link: "/设计/YouQu3架构设计规划"},
                        {text: "UOS自动化测试方法套件", link: "/设计/UOS自动化测试方法套件"},
                        {text: "UOS自动化测试用例", link: "/设计/UOS自动化测试用例"},
                    ]
                },
            ],
        },
        search: {
            provider: 'local'
        },
        ignoreDeadLinks: true,
        // =========================================================
        logo: {src: '/logo.png', width: 22, height: 30},
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
});
