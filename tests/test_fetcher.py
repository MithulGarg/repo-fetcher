import sys
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fetcher


def test_fetch_trending_repositories_writes_top_five() -> None:
    repositories = [
        {
            "name": f"repo-{index}",
            "html_url": f"https://github.com/example/repo-{index}",
            "description": None if index == 0 else f"Description {index}",
        }
        for index in range(6)
    ]
    response = Mock(status_code=200)
    response.json.return_value = {"items": repositories}
    output_file = mock_open()

    with (
        patch("fetcher.requests.get", return_value=response) as get,
        patch("builtins.open", output_file),
    ):
        fetcher.fetch_trending_repositories()

    get.assert_called_once()
    assert get.call_args.kwargs == {"timeout": 10}
    output_file.assert_called_once_with("trending.md", "w", encoding="utf-8")
    handle = output_file()
    assert handle.write.call_count == 5
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert "**repo-0**" in written_content
    assert "URL: https://github.com/example/repo-4" in written_content
    assert "repo-5" not in written_content
    assert "Description: None" in written_content


def test_fetch_trending_repositories_skips_file_on_api_error(capsys) -> None:
    response = Mock(status_code=500)
    output_file = mock_open()

    with (
        patch("fetcher.requests.get", return_value=response) as get,
        patch("builtins.open", output_file),
    ):
        fetcher.fetch_trending_repositories()

    get.assert_called_once()
    output_file.assert_not_called()
    assert "Error fetching data from GitHub API" in capsys.readouterr().out
