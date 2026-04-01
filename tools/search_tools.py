def register_search_tools(mcp):
    def _trim_text(value: str | None, max_chars: int) -> str | None:
        if value is None:
            return None
        normalized = " ".join(value.split())
        if len(normalized) <= max_chars:
            return normalized
        return normalized[: max_chars - 3].rstrip() + "..."

    def _get_ddgs():
        try:
            from ddgs import DDGS
        except ImportError:
            return None, {
                "error": "Missing dependency: ddgs. Install it with `pip install -U ddgs`.",
            }
        return DDGS, None

    @mcp.tool()
    def search_and_extract_content(
        query: str,
        region: str = "us-en",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        max_results: int = 3,
        extract_top: int = 2,
        page: int = 1,
        backend: str = "auto",
        extract_format: str = "text_markdown",
        snippet_max_chars: int = 240,
        content_max_chars: int = 1200,
    ):
        """
        Search the web with DDGS, then extract content from the top results.

        Use this tool when the user asks for badminton-related information that is
        not available in the internal RAG knowledge base or BadmintonNet data.

        Recommended use cases
        ---------------------
        - Official badminton rules, regulations, and scoring formats
        - Tournament schedules, draw information, rankings, and recent results
        - News about badminton players, clubs, federations, or events
        - Racket, shuttlecock, shoe, string, and gear research
        - Training methods, techniques, drills, injury-prevention guidance, and coaching content
        - Court, venue, academy, or badminton community information from external websites

        Do not use this tool for
        ------------------------
        - Internal BadmintonNet entities already covered by MCP tools or RAG
        - Club/profile/event/tournament data that can be answered from the existing system first

        In short: use this as a web fallback for badminton topics missing from RAG.

        Parameters
        ----------
        query : str
            Search query.
        region : str
            Region code such as `us-en`.
        safesearch : str
            One of `on`, `moderate`, or `off`.
        timelimit : str | None
            Optional freshness filter: `d`, `w`, `m`, or `y`.
        max_results : int
            Maximum number of search results to return.
        extract_top : int
            Number of top search results to extract content from.
        page : int
            Page number to fetch.
        backend : str
            Search backend, for example `auto`, `google`, `bing`, or `duckduckgo`.
        extract_format : str
            Extraction format: `text_markdown`, `text_plain`, `text_rich`, `text`, or `content`.
        snippet_max_chars : int
            Maximum characters kept for each search snippet.
        content_max_chars : int
            Maximum characters kept for extracted page content per result.
        """

        DDGS, error = _get_ddgs()
        if error:
            return error

        try:
            ddgs = DDGS()
            results = ddgs.text(
                query=query,
                region=region,
                safesearch=safesearch,
                timelimit=timelimit,
                max_results=max_results,
                page=page,
                backend=backend,
            )

            compact_results = []
            extracted_results = []
            for index, item in enumerate(results, start=1):
                compact_results.append(
                    {
                        "rank": index,
                        "title": item.get("title"),
                        "url": item.get("href"),
                        "snippet": _trim_text(item.get("body"), snippet_max_chars),
                    }
                )

            for index, item in enumerate(results[: max(0, extract_top)], start=1):
                url = item.get("href")
                if not url:
                    extracted_results.append(
                        {
                            "rank": index,
                            "title": item.get("title"),
                            "url": None,
                            "error": "Missing href in search result.",
                        }
                    )
                    continue

                try:
                    extracted = ddgs.extract(url=url, fmt=extract_format)
                    extracted_results.append(
                        {
                            "rank": index,
                            "title": item.get("title"),
                            "url": url,
                            "snippet": _trim_text(item.get("body"), snippet_max_chars),
                            "content": _trim_text(extracted.get("content"), content_max_chars),
                        }
                    )
                except Exception as exc:
                    extracted_results.append(
                        {
                            "rank": index,
                            "title": item.get("title"),
                            "url": url,
                            "snippet": _trim_text(item.get("body"), snippet_max_chars),
                            "error": str(exc),
                        }
                    )

            return {
                "query": query,
                "search_count": len(results),
                "results": compact_results,
                "extracted_count": len(extracted_results),
                "extracted_results": extracted_results,
            }
        except Exception as exc:
            return {"error": str(exc), "query": query}
