# シフトレフト演習リポジトリ

このリポジトリは、電卓Webアプリを題材にしたシフトレフト演習のためのものです。
テストをテストフェーズだけでなく、前倒しで行うシフトレフト開発の考え方を演習を通じて学ぶことを目的としています。

| スプリント期間 | 開発工程 | テスト工程 |
|---|---|---|
| 前半 | 要件定義フェーズ | 要件レビュー テスト分析 |
| 前半〜中盤 | 設計フェーズ | 設計レビュー テスト設計 |
| 中盤 | 実装フェーズ | テスト実装 |
| 後半 | テストフェーズ | 探索的テスト |

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

スクリプトを使わずに直接起動する場合は、次のコマンドでも確認できます。

```bash
PYTHONPATH=src uv run python -m training.app
```

## 演習の進め方

演習は [GitHub Pages](https://brainpad-whiterabbit.github.io/test-training/) に掲載されたドキュメントに沿って進めてください。

## 備考

### CI/CD と GitHub Pages

Pull Request または `main` / `develop` ブランチへの push で CI が実行されます。
CI では、テスト、lint、型チェック、ドキュメントビルドを確認します。

`main` ブランチへの push では、CI 成功後に GitHub Pages へ演習ドキュメントをデプロイします。

### このリポジトリに含まれるもの

- `docs/`: シフトレフト演習の手順、スプリント、付録テンプレート
- `src/training/`: 演習で使う Python パッケージ
- `tests/`: pytest のテスト
- `zensical.toml`: 演習ドキュメントサイトの設定
- `scripts/`: セットアップ、VS Code 拡張導入、チェック実行の補助スクリプト
- `.github/workflows/ci.yml`: GitHub Actions でのチェック、ドキュメントビルド、Pages デプロイ
- `.vscode/`: VS Code / Codespaces 向けの推奨設定とタスク
