# 配布とReleaseの方針

公開リポジトリは `tulipkite/medical-dictionary` です。作業用フォルダや非公開のTulipkite HQリポジトリの履歴は含めません。

## 公開するもの

README、LICENSE、NOTICE、CHANGELOG、CONTRIBUTING、辞書TXT、現在の編集用ソース、由来、匿名の架空用例による検証記録、文書、ビルド・検査スクリプト、テスト、Issueテンプレートを含めます。原典の全4万語は含めません。

辞書DB、学習履歴、個人辞書とバックアップ、秘密鍵、作業用ログ、端末の絶対パス、患者情報は含めません。`.gitignore`だけに頼らず、追加するファイルを確認します。

## 変更前後の確認

```sh
python3 scripts/build.py --output build
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

これらはネット接続、外部パッケージ、IMEの操作権限を必要としません。結果はファイルの再現性と保存済み記録の整合性の確認です。コミット前の作者設定は[公開窓口とGit作者の設定](contact-and-git.md)に従います。

## Release

版は1つだけで、辞書の内容を確定した日付（例: `2026-10-21`）で表します。Releaseのタグも同じ日付にします。辞書の内容を変えない文書だけの修正では、版もReleaseも増やしません。READMEに未検証と書かれている範囲が残る間は、GitHub ReleaseをPre-releaseとして扱い、安定版や遠隔読影対応済みを名乗りません。概要には登録数、対象のIME、確認済みの範囲と未検証の範囲を記載します。

Releaseには辞書TXTを `tulipkite-medical-dictionary-<版の日付>.txt` という名前で単体でも添付し（リポジトリ内のファイル名は変えません）、GitHubのソース一式（README・手順・LICENSE・NOTICE・編集用ソース）と併せて利用できるようにして、GPLの条件を守れる構成にします。内容の照合には `dictionary/google/manifest.json` のSHA256を用います。チェックサムを配布者の署名と説明しません。

公開後はGitHub上でREADMEの相対リンク、画像、TXTのダウンロード、Issueテンプレートの表示を確認します。
