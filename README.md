# Python Training

Python 開発演習用のリポジトリです。Python 環境と依存関係は `uv` で管理します。
Python は `.python-version` で 3.12 系に固定しています。

## Codespaces で始める

このリポジトリには `devcontainer` を置いていません。Codespaces では GitHub の既定イメージで開き、次のコマンドで環境を作成します。

```bash
./scripts/setup.sh
```

VS Code / Codespaces のコマンドパレットから `Tasks: Run Task` を開き、`Setup Python environment` を実行しても同じです。

## ローカルで始める

```bash
./scripts/setup.sh
```

`uv` が未インストールの場合、セットアップスクリプトが公式インストーラで導入します。

## よく使うコマンド

```bash
uv run pytest
uv run ruff check .
uv run mypy
```

まとめて確認する場合:

```bash
./scripts/check.sh
```

## 構成

- `src/training/`: 演習用の Python パッケージ
- `tests/`: pytest のテスト
- `scripts/setup.sh`: `uv` と依存関係のセットアップ
- `scripts/check.sh`: テスト、lint、型チェック
- `.vscode/`: Codespaces / VS Code 向けの推奨設定とタスク
- `.github/workflows/ci.yml`: GitHub Actions での検証

## 最初の演習

[src/training/calculator.py](src/training/calculator.py) の関数を変更し、[tests/test_calculator.py](tests/test_calculator.py) が通ることを確認してください。
