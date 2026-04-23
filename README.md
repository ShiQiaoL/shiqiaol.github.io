# shiqiaol.github.io

Xiaoqing Liu 的个人学术主页 — 纯静态 HTML + CSS，部署在 GitHub Pages。

## 本地预览

```sh
python -m http.server 8000
# 访问 http://localhost:8000
```

## 文件结构

| 路径 | 用途 |
|---|---|
| `index.html` | 首页（个人介绍、联系方式、研究兴趣） |
| `research.html` | 研究方向 |
| `publications.html` | 论文列表（自动同步 Google Scholar） |
| `style.css` | 唯一样式表，含深色模式 |
| `assets/` | 头像、CV、favicon |
| `scripts/update_scholar.py` | 抓取并生成 publications 块 |
| `.github/workflows/update_scholar.yml` | 每周六自动同步 |
| `robots.txt`, `sitemap.xml` | SEO |

## 论文同步

```sh
pip install "scholarly==1.7.11"
SCHOLAR_ID=<id> python scripts/update_scholar.py
```

Windows PowerShell：`$env:SCHOLAR_ID = "<id>"` 然后运行。

CI 在 GitHub Actions 中每周六（UTC 0:00）自动跑，使用仓库 secret `SCHOLAR_ID`。失败时会自动开 issue 通知。

## Google 搜索可发现性 — 部署后清单

代码层面已做：
- [x] JSON-LD `Person` schema（首页）
- [x] JSON-LD `ScholarlyArticle` schema（每条论文，下次 Scholar 同步生效）
- [x] `<link rel="canonical">`、Open Graph、Twitter Card
- [x] `robots.txt` + `sitemap.xml`

**需要手动做**：
1. 登录 [Google Search Console](https://search.google.com/search-console) → 添加 `https://shiqiaol.github.io/` → 提交 `sitemap.xml`
2. 在 ORCID profile 和 Google Scholar profile 中把 `https://shiqiaol.github.io/` 填为 personal homepage（建立反向链接）
3. 用 [Rich Results Test](https://search.google.com/test/rich-results) 输入站点 URL 验证 Person / ScholarlyArticle schema 被识别
4. 用 [PageSpeed Insights](https://pagespeed.web.dev/) 跑 Lighthouse，目标 SEO/Accessibility ≥95

## 待办：图片压缩（手动）

`assets/xiaoqing-liu-portrait.jpg` 当前 166 KB，含 EXIF 元数据。建议：
- 用 [Squoosh](https://squoosh.app/) 或 `mozjpeg` 压到 ≤60 KB
- 尺寸建议 800×1000，移除 EXIF
- HTML 中已设置 `width="800" height="1000"`，请按此尺寸输出

## 项目约定

- `publications.html` 中 `<!-- AUTO-GENERATED:START -->` 和 `<!-- AUTO-GENERATED:END -->` 之间的内容只能由 `scripts/update_scholar.py` 写，不要手改
- CSS 设计 token 都定义在 `:root` / 深色模式 `:root` 中，不要硬编码颜色
- 所有页面共用 header / footer / nav，保持一致
- 不使用构建工具，不引入 JavaScript 框架
