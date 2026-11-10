# 開発ガイド

このリポジトリはTulipkite Medical Dictionaryの辞書、手順、再生成・照合ツールを管理します。HQ配下のcheckoutで`../AGENTS.md`が存在する場合は、作業前に読みます。単独checkoutでもこのガイドとREADMEから検証できる状態を保ちます。

- 製品の位置づけは`docs/product-positioning.md`、窓口は`CONTACT.md`、ライセンスと来歴は`LICENSE`・`NOTICE.md`が正本です。
- `source/`を編集してから生成物を更新します。既存の実測記録を書き換えて、新しい試験を実施したように扱いません。
- 辞書DB、個人辞書、学習履歴、患者情報、端末バックアップ、秘密情報を入れません。IMEや端末設定への書き込みを同梱スクリプトへ追加しません。
- 通常の検査は`python3 scripts/check.py`と`python3 -m unittest discover -s tests -v`です。Python 3.9以降の標準ライブラリを使います。
- 公開前のGit作者設定は`docs/contact-and-git.md`に従います。グローバルなGit設定や他のrepoの作者を変更しません。
- この製品は無料・広告なし・日本語辞書を先行します。未検証のIME・OS・遠隔入力を対応済みと表示しません。
- 公開や外部送信はユーザーから依頼された範囲で行います。
