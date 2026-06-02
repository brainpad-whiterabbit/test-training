# 演習スプリント 2

## スプリント概要

このスプリントでは、エラー表示、表示桁数制限、計算結果桁数制限の機能を追加することを目指します。

## 要件レビュー

チュートリアルスプリント同様の手順でレビューを実施し、要件定義書にレビュー内容を記載してください。記載内容はcommit & pushしてください。

## テスト設計

チュートリアルスプリント同様の手順でテストケースを作成してください。テストケース表の変更内容はcommit & pushしてください。

| テスト観点 | テストケース                   | 入力                                       | 期待値                                            |
| ---------- | ------------------------------ | ------------------------------------------ | ------------------------------------------------- |
| TV-019     | 0除算時はエラー表示            | left=5, operator=÷, right=0                | display="DivisionByZeroError", expression=""      |
| TV-020     | Error後にCで正常復帰           | 0除算エラー発生後にC押下                   | display="0", left=None, operator=None             |
| TV-020     | Error後にCEで正常復帰          | 0除算エラー発生後にCE押下                  | display="0", left=None, operator=None             |
| TV-021     | Overflow時はエラー表示         | left=999999.9999, operator=+, right=0.0001 | display="CalculationOverflowError", expression="" |
| TV-022     | Overflow後にCで正常復帰        | Overflowエラー発生後にC押下                | display="0", left=None, operator=None             |
| TV-022     | Overflow後にCEで正常復帰       | Overflowエラー発生後にCE押下               | display="0", left=None, operator=None             |
| TV-023     | 整数部が6桁まで入力可能        | display="99999" に digit="9" を入力        | display="999999"                                  |
| TV-024     | 小数部が4桁まで入力可能        | display="1.999" に digit="9" を入力        | display="1.9999"                                  |
| TV-025     | 上限超過時は入力値を維持       | display="999999" に digit="9" を入力       | display="999999"                                  |
| TV-026     | 計算結果上限超過でOverflow表示 | left=999999.9999, operator=+, right=0.0001 | display="CalculationOverflowError"                |
| TV-027     | 小数部が4桁超えた結果を丸め    | left=1, operator=÷, right=3                | display="0.333"                                   |

## 実装, テスト実装

チュートリアルスプリント同様の手順で実装とテスト実装を行ってください。実装内容はcommit & pushしてください。

## 探索的テスト

チュートリアルスプリント同様の手順で探索的テストを実施してください。変更内容はcommit & pushしてください。
