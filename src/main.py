"""
オフモール（ハードオフ公式通販）スクレイパー エントリポイント。

キーワード検索またはカテゴリ指定で全国800店舗以上が出店する
ハードオフグループ公式総合中古通販サイトから商品データを収集します。
"""

from __future__ import annotations

import asyncio
import datetime
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from apify import Actor
except ImportError:
    Actor = None

from sources.offmall import CATEGORIES, search_offmall


def _norm_key(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


async def run(actor_input: dict) -> list[dict]:
    stats_mode = actor_input.get("statsMode", False)
    keyword = str(actor_input.get("searchKeyword", "")).strip()
    category = str(actor_input.get("category", "")).strip()
    max_items = int(actor_input.get("maxItems", 100))
    max_pages = int(actor_input.get("maxPages", 2))

    # プロキシ設定（Apify環境では使用、ローカルでは無視）
    proxy_url = None
    if Actor is not None:
        try:
            proxy_config = await Actor.create_proxy_configuration(
                actor_proxy_input=actor_input.get("proxyConfiguration")
            )
            if proxy_config:
                proxy_url = await proxy_config.new_url()
        except Exception as e:
            print(f"Proxy config skipped: {e}")

    import httpx

    async with httpx.AsyncClient(
        proxy=proxy_url,
        timeout=30.0,
        follow_redirects=True,
    ) as client:
        results = await search_offmall(
            client,
            keyword=keyword,
            category=category,
            max_pages=max_pages,
            max_items=max_items,
        )

    if stats_mode:
        stats_keyword = actor_input.get("statsKeyword", "")
        keyword_norm = _norm_key(stats_keyword) if stats_keyword else None
        prices = []
        sample_items = []
        for item in results:
            if keyword_norm:
                title = _norm_key(str(item.get("title", "")))
                if keyword_norm not in title:
                    continue
            try:
                price = int(item.get("price"))
            except (TypeError, ValueError):
                continue
            if len(sample_items) < 3:
                sample_items.append({
                    "title": item.get("title"),
                    "price": price,
                    "detailUrl": item.get("detailUrl"),
                    "shop": item.get("shop"),
                })
            prices.append(price)

        if prices:
            prices_sorted = sorted(prices)
            count = len(prices)
            price_min = prices_sorted[0]
            price_max = prices_sorted[-1]
            price_avg = int(sum(prices) / count)
            if count % 2 == 1:
                median = prices_sorted[count // 2]
            else:
                median = (prices_sorted[count // 2 - 1] + prices_sorted[count // 2]) // 2
            stats_result = {
                "statsType": "japan-offmall-price",
                "keyword": stats_keyword,
                "count": count,
                "priceMin": price_min,
                "priceMax": price_max,
                "priceAvg": price_avg,
                "priceMedian": median,
                "sampleItems": sample_items,
                "collectedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            if Actor is not None:
                await Actor.push_data(stats_result)
            else:
                print(json.dumps(stats_result, ensure_ascii=False))
        return []

    if Actor is not None:
        for item in results:
            await Actor.push_data(item)
        print(f"Collected {len(results)} items from OffMall")
    return results


async def main() -> None:
    if Actor is not None:
        async with Actor:
            actor_input = await Actor.get_input() or {}
            await run(actor_input)
    else:
        # ローカル実行: stdinからJSON入力を受け取る
        raw = sys.stdin.read().strip()
        if raw:
            actor_input = json.loads(raw)
        else:
            actor_input = {}
        results = await run(actor_input)
        for item in results:
            print(json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
