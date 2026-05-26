# シフトレフト開発演習リポジトリ

このリポジトリは、電卓Webアプリを題材にしたシフトレフト開発演習のためのものです。
テストを最後のテスト工程で実施するのではなく、開発と並行して前倒しで実施するシフトレフト開発の考え方を演習を通じて学ぶことを目的としています。

| スプリント期間 | 開発工程 | テスト工程              |
| -------------- | -------- | ----------------------- |
| 前半           | 要件定義 | 要件レビュー テスト分析 |
| 前半〜中盤     | 設計     | 設計レビュー テスト設計 |
| 中盤           | 実装     | テスト実装              |
| 後半           | テスト   | 探索的テスト            |

まずこの README に沿って [環境構築](#環境構築) と [動作確認](#動作確認) を行い、その後に [演習の進め方](#演習の進め方) に進んでください。

## 環境構築

Codespaces またはローカル環境でリポジトリを開き、次のコマンドを実行してください。

```bash
./scripts/setup.sh
./scripts/install-vscode-extensions.sh
```

各スクリプトでは次の処理を行います。

- `scripts/setup.sh`: `uv` が未インストールの場合は公式インストーラで導入し、`uv sync --all-groups` で依存関係を準備します。
- `scripts/install-vscode-extensions.sh`: `.vscode/extensions.json` の `recommendations` に定義された VS Code 拡張を、利用できる `code` / `code-insiders` / `code-server` コマンドで導入します。

## 動作確認

環境構築が正常に完了したことを確認するため、次のコマンドを実行してください。

```bash
./scripts/check.sh
```

このスクリプトでは、テスト、lint、型チェックをまとめて実行します。

電卓Webアプリの起動を確認する場合は、次のコマンドを実行してください。

```bash
./scripts/run-calculator-app.sh
```

起動後、ブラウザで `http://localhost:8080` を開き、電卓が表示されることを確認してください。
確認が終わったら、アプリを起動しているターミナルで `Ctrl+C` を押して終了してください。

スクリプトを使わずに直接起動する場合は、次のコマンドでも確認できます。

```bash
PYTHONPATH=src uv run python -m training.app
```

## 演習の進め方

演習は [GitHub Pages](https://brainpad-whiterabbit.github.io/test-training/) に掲載されたドキュメントに沿って進めてください。

## 備考

### VS Code Tasks

VS Code / Codespaces では、コマンドパレットから `Tasks: Run Task` を選択すると `.vscode/tasks.json` に定義されたタスクを実行できます。

- `Check`: テスト、lint、型チェックをまとめて実行します。
- `Test`: pytest のテストを実行します。
- `Run Calculator App`: 電卓Webアプリを起動します。終了する場合は、ターミナルで `Ctrl+C` を押すか、コマンドパレットから `Tasks: Terminate Task` を実行してください。
- `Doc Serve`: 演習ドキュメントサイトをローカルで起動します。

### CI/CD と GitHub Pages

以下の表に従ってGithub ActionsのCI/CDが動作します。

| イベント     | ブランチ条件 | check    | test     | build-pages | deploy-pages |
| ------------ | ------------ | -------- | -------- | ----------- | ------------ |
| push         | main         | 動く     | 動く     | 動く        | 動く         |
| push         | main 以外    | 動かない | 動かない | 動かない    | 動かない     |
| pull_request | すべて       | 動く     | 動く     | 動かない    | 動かない     |

### このリポジトリに含まれるもの

- `docs/`: シフトレフト演習の手順、スプリント、付録テンプレート
- `src/training/`: 演習で使う Python パッケージ
- `tests/`: pytest のテスト
- `zensical.toml`: 演習ドキュメントサイトの設定。目次は `docs/` の Markdown ファイルから自動生成します。
- `scripts/`: セットアップ、VS Code 拡張導入、チェック実行の補助スクリプト
- `.github/workflows/ci.yml`: GitHub Actions でのチェック、ドキュメントビルド、Pages デプロイ
- `.vscode/`: VS Code / Codespaces 向けの推奨設定とタスク
