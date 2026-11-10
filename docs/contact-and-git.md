# 公開窓口とGit作者の設定

運営と問い合わせの正本は[CONTACT.md](../CONTACT.md)です。問い合わせ先はsupport@tulipkite.com、メンテナーは@d25037とします。公開リポジトリはGitHub Organization `tulipkite` に置きます。

## メンテナーのローカル設定

このプロジェクトのリポジトリ内で、コミット前に次を設定します。`--local`でこのリポジトリだけに適用し、他のプロジェクトやグローバル設定を変更しません。一般のコントリビューターは自分のGitHubアカウントとnoreplyアドレスを使ってください。

```sh
git config --local user.name d25037
git config --local user.email 99938271+d25037@users.noreply.github.com
git config --local user.useConfigOnly true
git config --local --get user.name
git config --local --get user.email
git var GIT_AUTHOR_IDENT
```

2026年10月25日にGitHub接続で確認したアカウントはd25037、IDは99938271です。アドレスはGitHubが案内するID付きnoreply形式に基づきます。GitHub Web側のメールプライバシー設定は別管理で、このローカル設定によって変更されません。Webでコミットする前にはGitHub Settings → Emailsで設定を確認してください。

新しいcheckoutでは`.git/config`が引き継がれないため、上記を再設定します。シェル環境の`GIT_AUTHOR_EMAIL`や`GIT_COMMITTER_EMAIL`がある場合は、ローカル設定より優先される可能性があります。最初のコミット後、push前にも実際の記録を確認します。

```sh
git log -1 --format='author=%an <%ae>%ncommitter=%cn <%ce>'
```

作者設定の変更は、過去に作成したコミットのメールを書き換える操作ではありません。初回公開時は本プロジェクトの公開用ファイルだけで独立した履歴を作り、作業用フォルダやHQの履歴を引き継ぎません。

参考: [GitHubのnoreply形式](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference#your-noreply-email-address)、[リポジトリ単位の作者メール設定](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address#setting-your-email-address-for-a-single-repository)。
