# Japan OffMall Used Goods Market — Hard Off Official Scraper

[![Apify Store](https://img.shields.io/badge/Apify-Store-blue)](https://apify.com/fruitful_quintessence/japan-offmall-market-scraper)

**Scrape used goods prices from OffMall (オフモール), the official online store of Hard Off (ハードオフ) — Japan's largest reuse chain with 800+ participating stores nationwide.**

One dataset covering Japan's biggest second-hand ecosystem: cameras, watches, musical instruments, luxury brands, smartphones, game consoles, audio gear, and more.

## Why this is useful

- **800+ stores in one place** — OffMall aggregates listings from Hard Off stores across Japan (毎日更新)
- **One-item-only used goods** — every listing is a unique physical item with a condition rank (S/A/B/C)
- **Total market scan** — search by keyword or scan entire categories (13 categories)
- **Cross-shop arbitrage** — compare OffMall prices against Kitamura/Fujiya/Jackroad via the Japan Market family of actors

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `searchKeyword` | string | `iPhone` | Keyword to search (e.g. iPhone, ロレックス, ニンテンドー) |
| `category` | select | `` | Category to scan when keyword is empty (カメラ/時計/楽器/ブランド品 等13種) |
| `maxItems` | integer | 100 | Max items to collect |
| `maxPages` | integer | 2 | Max pages per source (30 items/page) |

## Output fields

| Field | Description |
|---|---|
| `productId` | Product ID |
| `title` | Product title |
| `brand` | Brand (e.g. APPLE, Canon, Rolex) |
| `modelCode` | Model code (e.g. MWLX2J/A) |
| `price` | Price in JPY |
| `rank` | Condition rank (S/A/B/C) |
| `imageUrl` | Product image URL |
| `productUrl` | Product page URL |
| `shop` | `OffMall` |
| `source` | `offmall` |
| `category` | Category label |
| `scrapedAt` | Scrape timestamp |

## Output sample

```json
{
  "productId": "6426181",
  "title": "iPhone 11",
  "brand": "APPLE",
  "modelCode": "MWLX2J/A",
  "price": 27500,
  "rank": "B",
  "imageUrl": "https://p1-d9ebd2ee.imageflux.jp/c!/w=231,h=182,a=0,u=0,q=75/201328/2026_08_10_18_26_49.jpg",
  "productUrl": "https://netmall.hardoff.co.jp/product/6426181/",
  "shop": "OffMall",
  "source": "offmall",
  "category": "検索:iPhone",
  "scrapedAt": "2026-08-10T10:10:00Z"
}
```

## Pricing

Pay per event — $0.00005/run + $0.002/item.

## Data source notes

- **OffMall (netmall.hardoff.co.jp)**: official Hard Off online store, 800+ participating stores
- Server-side rendered search pages, robots.txt allows crawling (only /api/, /users/, /statics/ etc. disallowed)
- Only factual product information (name, price, brand, condition rank) is collected
