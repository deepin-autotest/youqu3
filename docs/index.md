---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: YouQu3
  text: "下一代 Linux 自动化测试框架"
  tagline: 让 Linux 自动化测试变得更简单
  actions:
    - theme: brand
      text: GitHub
      link: "https://github.com/funny-dream/youqu3"
    - theme: alt
      text: Issues
      link: "https://github.com/funny-dream/youqu3/issues"
  image:
    src: /logo.png
    alt: YouQu3

features:
  - icon: 💪
    title: 新架构
    details: 全新的架构设计，插件化、模块化改造，底层全面重写，优化框架接口调用机制。
  - icon: 💥
    title: 新玩法
    details: 继承YouQu2诸多亮点功能的同时解决其遇到的问题，各方面全面优化，更多玩法姿势等你来解锁。
  - icon: 🛀
    title: 新体验
    details: 更加简单易用、更加纯粹、扩展性和兼容性更好，一秒入魂。

---

<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const members = [
  {
    avatar: 'https://www.github.com/mikigo.png',
    name: 'mikigo',
    title: 'Creator',
    org: 'YouQu3',
    orgLink: 'https://github.com/funny-dream/youqu3',
    links: [
      { icon: 'github', link: 'https://github.com/mikigo' },
      { icon: 'x', link: 'https://twitter.com/mikigo_' },
    ]
  },
  // {
  //   avatar: 'https://www.github.com/DarkLii.png',
  //   name: 'DarkLii',
  //   title: 'Developer',
  //   links: [
  //     { icon: 'github', link: 'https://github.com/DarkLii' },
  //   ]
  // },
]

</script>


<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>
      Contributors
    </template>
    <template #lead>
      感谢以下所有人的贡献与参与
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="members"
  />
</VPTeamPage>
