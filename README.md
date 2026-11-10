# Tulipkite Medical Dictionary

放射線科・IVRの文章入力に使う、無料の日本語変換辞書です。Tulipkiteの無償の専門ツールとして、DMiMEを基に選定した基本1000語と、文中変換を補う登録を提供します。

**現在の辞書は2026-10-21版・1153登録の試用版（Pre-release）です。版は辞書の内容を確定した日付で表します。管理アプリはまだ実装していません。** 辞書、編集用ソース、再生成スクリプト、手順、検証結果をGPL-2.0で提供します。課金・広告・アカウント登録はありません。DMiME、Google、日本医師会ORCA管理機構の公式製品ではありません。

## 使うファイル

対象はMac版Google日本語入力です。

**辞書は[Releaseのページ](https://github.com/tulipkite/medical-dictionary/releases)からダウンロードします。** 最新版の「Assets」にある `tulipkite-medical-dictionary-2026-10-21.txt`（ファイル名の末尾は版の日付）をクリックして保存してください。初めて導入する場合は、このファイルだけを取り込みます。Google日本語入力用のUTF-8・LF・タブ区切り3列です。

同じファイルはリポジトリの[dictionary/google/tulipkite-medical-dictionary.txt](dictionary/google/tulipkite-medical-dictionary.txt)にもあります。こちらから取る場合は「Download raw file」等の機能でTXTそのものを保存してください。HTMLページを保存したファイルは使えません。

**先に[導入手順](docs/install-google-mac.md)を読み、既存の個人辞書へ混ぜず、新規の専用辞書へ取り込んでください。** 重ね取り込みはしません。

- [導入手順](docs/install-google-mac.md)
- [元の状態へ戻す手順](docs/restore.md)
- [確認済みの範囲と既知の問題](docs/verification.md)
- [出典とライセンス](NOTICE.md)
- [改善の提案方法](CONTRIBUTING.md)

## 収録内容

基本1000語に、基本語の優先指定37登録と文中変換用116登録を加えた計1153登録です。異なる表記・語句は1115種類あります。同じ語に品詞の異なる登録があるため、1153語という意味ではありません。

例として「仮性瘤を認めます」「多房性の嚢胞性病変」「腎杯の拡張」「塊状の病変」などを扱います。一般語との同音語競合があり、どの文章でも先頭候補になる保証はありません。

## 動作確認の範囲

2026年10月21日、Apple Silicon Mac・macOS 26.6.2・Google日本語入力3.34.6260.1で確認しました。

| 試験 | 結果 |
| --- | --- |
| 学習参照なしの変換エンジン回帰試験 | 医療文143/143例がスペース1回で一致。調整に使った用例を含み、未知文の正解率ではありません |
| 基本1000語 | 999語が先頭候補。全1000語が文節拡張なしで候補に存在 |
| TextEditでのローマ字実入力 | 学習参照・新規学習を無効にし、「仮性瘤を認めます」「多房性の嚢胞性病変」の2例がスペース1回で一致 |
| 一般文32例 | 30例が一致。同音語への影響は検証記録を参照 |

**公式辞書ツールからのTXT取り込み、別のMac、Windows、Android版Gboard、遠隔接続先のレポート画面では未検証です。** 手順は小規模な試用向けに用意しています。現在の辞書を保持したまま、専用辞書で確認してください。本リポジトリのスクリプトはIMEへ接続せず、設定や学習履歴を変更しません。

## 開発と再生成

Python 3.9以降の標準ライブラリだけで使えます。外部パッケージのインストールは不要です。

```sh
python3 scripts/build.py --output build
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

`build/tulipkite-medical-dictionary.txt`が配布用TXTと同一になることを確認できます。[編集用ソース](source/README.md)と[配布とReleaseの方針](docs/github-publishing.md)も参照してください。

## ライセンスと保守

GPL-2.0。全文は[LICENSE](LICENSE)、元の著作権表示と変更内容は[NOTICE.md](NOTICE.md)に記載しています。無償公開は、商用利用を禁止する条件ではありません。ライセンスの範囲で改変・再配布できます。

改善はGitHub IssuesとPull Requestsで受け付ける方針です。患者情報や実レポートを投稿せず、架空の例文を使ってください。対応は可能な範囲で行い、回答期限や特定環境での動作を約束するサポートは設けません。[今後の方針](docs/roadmap.md)に、辞書を先に公開し、必要な管理機能を育てる計画を記載しています。

## 運営・お問い合わせ

運営: **Tulipkite** / メンテナー: **[@d25037](https://github.com/d25037)**。

誤変換・読みの改善・導入時の不具合は、本リポジトリ公開後にGitHub Issuesへお寄せください。その他のお問い合わせは **[support@tulipkite.com](mailto:support@tulipkite.com)** へご連絡ください。患者情報・実際の読影レポート・個人辞書や学習履歴は送らず、架空の短い用例でご説明ください。保守は可能な範囲で行い、回答期限は設けていません。

[連絡先と報告方法](CONTACT.md)、[Tulipkite製品としての位置づけ](docs/product-positioning.md)を参照してください。
